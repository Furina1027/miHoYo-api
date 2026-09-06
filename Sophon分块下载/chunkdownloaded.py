"""按 chunk_ids.json 下载全部 chunks，并按 offset 组装成完整文件。

用法:
    python chunkdownloaded.py <chunk_ids.json> <chunk_prefix> [output_dir] [max_workers]

chunk_prefix = chunk_download.url_prefix
"""
import argparse
import hashlib
import io
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import zstandard as zstd


def md5_hex(data):
    return hashlib.md5(data).hexdigest()


def download_and_decompress_chunk(url):
    """下载并使用流式解压（兼容 raw zstd block）"""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with zstd.ZstdDecompressor().stream_reader(io.BytesIO(response.content)) as reader:
                return reader.read()
        except Exception as e:
            if attempt == 2:
                print(f"❌ 最终失败: {url} | 错误: {e}")
                return None
    return None


def download_chunk(chunk_prefix, chunk_info):
    """下载单个 chunk 并校验解压后 MD5"""
    chunk_url = f"{chunk_prefix}/{chunk_info['chunk_id']}"
    chunk_data = download_and_decompress_chunk(chunk_url)
    if chunk_data is None:
        return {'chunk_id': chunk_info['chunk_id'], 'success': False}

    expected_md5 = (chunk_info.get('uncompressed_md5') or '').lower()
    if expected_md5 and md5_hex(chunk_data) != expected_md5:
        print(f"❌ MD5 校验失败: {chunk_info['chunk_id']}")
        return {'chunk_id': chunk_info['chunk_id'], 'success': False}

    return {'offset': chunk_info['offset'], 'data': chunk_data, 'success': True}


def download_and_save_file(file_name, file_chunks, chunk_prefix, output_dir, max_workers):
    print(f"\n正在下载文件: {file_name} ({len(file_chunks)} 个 chunks)")

    downloaded_chunks = []
    failed_ids = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_chunk, chunk_prefix, chunk): chunk
            for chunk in file_chunks
        }

        completed = 0
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            if result['success']:
                downloaded_chunks.append(result)
            else:
                failed_ids.append(result['chunk_id'])
            if completed % 100 == 0 or completed == len(file_chunks):
                print(f"  进度 [{completed}/{len(file_chunks)}]")

    if failed_ids:
        print(f"  ✗ 跳过保存: 缺少 chunks ({len(downloaded_chunks)}/{len(file_chunks)})")
        return False

    total_size = max(c['offset'] + len(c['data']) for c in downloaded_chunks)
    file_buffer = bytearray(total_size)
    for chunk in downloaded_chunks:
        start = chunk['offset']
        file_buffer[start:start + len(chunk['data'])] = chunk['data']

    expected_md5 = (file_chunks[0].get('file_md5') or '').lower()
    if expected_md5 and md5_hex(file_buffer) != expected_md5:
        print(f"  ❌ 整体 MD5 校验失败（期望 {expected_md5}，实际 {md5_hex(file_buffer)}）")

    output_path = Path(output_dir) / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(file_buffer)

    print(f"  ✓ 已保存: {file_name} ({len(file_buffer)} 字节)")
    return True


def download_all_files(chunk_ids_file, chunk_prefix, output_dir, max_workers):
    with open(chunk_ids_file, 'r', encoding='utf-8') as f:
        all_chunks = json.load(f)

    files_dict = {}
    for chunk in all_chunks:
        files_dict.setdefault(chunk['file'], []).append(chunk)

    print(f"总共 {len(files_dict)} 个文件, {len(all_chunks)} 个 chunks")

    success_count = 0
    for i, (file_name, file_chunks) in enumerate(files_dict.items(), 1):
        print(f"[{i}/{len(files_dict)}]")
        if download_and_save_file(file_name, file_chunks, chunk_prefix, output_dir, max_workers):
            success_count += 1

    print(f"\n下载完成: {success_count}/{len(files_dict)} 个文件成功保存到 {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="下载 Sophon chunks 并按 offset 组装成完整文件")
    parser.add_argument("chunk_ids_file", help="Manifest.py 生成的 chunk_ids.json")
    parser.add_argument("chunk_prefix", help="chunk 下载地址前缀: chunk_download.url_prefix")
    parser.add_argument("output_dir", nargs="?", default="downloaded_files", help="输出目录 (默认 downloaded_files)")
    parser.add_argument("max_workers", nargs="?", type=int, default=10, help="并发线程数 (默认 10)")
    args = parser.parse_args()

    download_all_files(args.chunk_ids_file, args.chunk_prefix, args.output_dir, args.max_workers)
