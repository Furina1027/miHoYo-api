"""按 chunk_ids.json 下载全部 chunks，仅保存 chunk 文件（不组装）。

用法:
    python chunkdownloaded2.py <chunk_ids.json> <chunk_prefix> [output_dir] [max_workers]

chunk_prefix = chunk_download.url_prefix
"""
import argparse
import hashlib
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import zstandard as zstd


def zstd_get(url):
    """下载并解压 Zstd 压缩的数据（chunk 为无内容大小头的 zstd 流，需用流式解压）"""
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


def download_single_chunk(chunk_prefix, chunk_info, output_dir):
    """下载单个 chunk，校验 MD5 后保存为以 chunk_id 命名的文件"""
    chunk_url = f"{chunk_prefix}/{chunk_info['chunk_id']}"
    chunk_data = zstd_get(chunk_url)
    if chunk_data is None:
        return False

    expected_md5 = (chunk_info.get('uncompressed_md5') or '').lower()
    if expected_md5 and hashlib.md5(chunk_data).hexdigest() != expected_md5:
        print(f"❌ MD5 校验失败: {chunk_info['chunk_id']}")
        return False

    output_path = os.path.join(output_dir, chunk_info['chunk_id'])
    with open(output_path, 'wb') as f:
        f.write(chunk_data)
    return True


def download_all_chunks(chunk_ids_file, chunk_prefix, output_dir, max_workers):
    with open(chunk_ids_file, 'r', encoding='utf-8') as f:
        all_chunks = json.load(f)

    print(f"总共需要下载 {len(all_chunks)} 个 chunk")
    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    failed_count = 0
    total = len(all_chunks)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_single_chunk, chunk_prefix, chunk, output_dir): chunk
            for chunk in all_chunks
        }

        for i, future in enumerate(as_completed(futures), 1):
            try:
                if future.result():
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                print(f"❌ 下载异常: {futures[future]['chunk_id']} - {e}")
            if i % 200 == 0 or i == total:
                print(f"进度 [{i}/{total}] 成功 {success_count} 失败 {failed_count}")

    print(f"\n下载完成:")
    print(f"  成功: {success_count} chunks")
    print(f"  失败: {failed_count} chunks")
    print(f"  保存位置: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="下载 Sophon chunks，仅保存 chunk 文件（不组装）")
    parser.add_argument("chunk_ids_file", help="Manifest.py 生成的 chunk_ids.json")
    parser.add_argument("chunk_prefix", help="chunk 下载地址前缀: chunk_download.url_prefix")
    parser.add_argument("output_dir", nargs="?", default="chunks", help="输出目录 (默认 chunks)")
    parser.add_argument("max_workers", nargs="?", type=int, default=10, help="并发线程数 (默认 10)")
    args = parser.parse_args()

    download_all_chunks(args.chunk_ids_file, args.chunk_prefix, args.output_dir, args.max_workers)
