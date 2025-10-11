import json
import requests
import zstandard as zstd
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_and_decompress_chunk(url):
    """下载并使用流式解压（兼容 raw zstd block）"""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            raw_data = response.content

            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(io.BytesIO(raw_data)) as reader:
                return reader.read()
        except Exception as e:
            if attempt == 2:
                print(f"❌ 最终失败: {url} | 错误: {e}")
                return None
    return None


def download_chunk(chunk_prefix, chunk_info):
    """下载单个 chunk（不处理 chunk_prefix 空格）"""
    chunk_url = f"{chunk_prefix}/{chunk_info['chunk_id']}"
    chunk_data = download_and_decompress_chunk(chunk_url)

    if chunk_data is not None:
        return {
            'offset': chunk_info['offset'],
            'data': chunk_data,
            'success': True
        }
    else:
        return {
            'chunk_id': chunk_info['chunk_id'],
            'success': False
        }


def download_and_save_file(file_name, file_chunks, chunk_prefix, output_dir, max_workers=10):
    print(f"\n正在下载文件: {file_name} ({len(file_chunks)} 个 chunks)")

    downloaded_chunks = []
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
                print(f"  ✅ [{completed}/{len(file_chunks)}] 下载成功")
            else:
                print(f"  ❌ [{completed}/{len(file_chunks)}] 下载失败: {result['chunk_id']}")

    if len(downloaded_chunks) != len(file_chunks):
        print(f"  ✗ 跳过保存: 缺少 chunks ({len(downloaded_chunks)}/{len(file_chunks)})")
        return False

    total_size = max(c['offset'] + len(c['data']) for c in downloaded_chunks)
    file_buffer = bytearray(total_size)
    for chunk in downloaded_chunks:
        start = chunk['offset']
        file_buffer[start:start + len(chunk['data'])] = chunk['data']

    output_path = Path(output_dir) / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(file_buffer)

    print(f"  ✓ 已保存: {file_name} ({len(file_buffer)} 字节)")
    return True


def download_all_chunks(chunk_ids_file, chunk_prefix, output_dir, max_workers=10):
    with open(chunk_ids_file, 'r', encoding='utf-8') as f:
        all_chunks = json.load(f)

    files_dict = {}
    for chunk in all_chunks:
        file_name = chunk['file']
        files_dict.setdefault(file_name, []).append(chunk)

    print(f"总共 {len(files_dict)} 个文件, {len(all_chunks)} 个 chunks")

    success_count = 0
    for i, (file_name, file_chunks) in enumerate(files_dict.items(), 1):
        print(f"\n[{i}/{len(files_dict)}]")
        if download_and_save_file(file_name, file_chunks, chunk_prefix, output_dir, max_workers):
            success_count += 1

    print(f"\n下载完成: {success_count}/{len(files_dict)} 个文件成功保存")


if __name__ == "__main__":
    chunk_ids_file = "chunk_ids.json"
    chunk_prefix = "https://autopatchcn.yuanshen.com/client_app/sophon/chunks/cxgf44wie1a8/keNBn8xtnZIG"
    output_dir = "downloaded_files"

    download_all_chunks(chunk_ids_file, chunk_prefix, output_dir, max_workers=10)
