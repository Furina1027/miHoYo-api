import json
import requests
import zstandard as zstd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def zstd_get(url):
    """下载并解压 Zstd 压缩的数据"""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()

            # 使用 zstandard 解压
            dctx = zstd.ZstdDecompressor()
            decompressed_data = dctx.decompress(response.content)
            return decompressed_data
        except Exception as e:
            if attempt == 2:
                return None
    return None


def download_single_chunk(chunk_prefix, chunk_info, output_dir):
    """下载单个 chunk 并保存为文件"""
    chunk_url = f"{chunk_prefix}/{chunk_info['chunk_id']}"
    chunk_data = zstd_get(chunk_url)

    if chunk_data:
        # 保存为独立文件,文件名为 chunk_id(无后缀)
        output_path = os.path.join(output_dir, chunk_info['chunk_id'])
        with open(output_path, 'wb') as f:
            f.write(chunk_data)
        return True
    return False


def download_all_chunks(chunk_ids_file, chunk_prefix, output_dir, max_workers=10):
    """下载 chunk_ids.json 中的所有 chunks"""
    # 读取 chunk_ids.json
    with open(chunk_ids_file, 'r', encoding='utf-8') as f:
        all_chunks = json.load(f)

    print(f"总共需要下载 {len(all_chunks)} 个 chunk")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 并发下载所有 chunks
    success_count = 0
    failed_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_single_chunk, chunk_prefix, chunk, output_dir): chunk
            for chunk in all_chunks
        }

        for i, future in enumerate(as_completed(futures), 1):
            chunk_info = futures[future]
            try:
                success = future.result()
                if success:
                    success_count += 1
                    print(f"[{i}/{len(all_chunks)}] 下载成功: {chunk_info['chunk_id']}")
                else:
                    failed_count += 1
                    print(f"[{i}/{len(all_chunks)}] 下载失败: {chunk_info['chunk_id']}")
            except Exception as e:
                failed_count += 1
                print(f"[{i}/{len(all_chunks)}] 下载异常: {chunk_info['chunk_id']} - {e}")

                # 统计
    print(f"\n下载完成:")
    print(f"  成功: {success_count} chunks")
    print(f"  失败: {failed_count} chunks")
    print(f"  保存位置: {output_dir}")


if __name__ == "__main__":
    # 配置参数
    chunk_ids_file = "chunk_ids.json"
    chunk_prefix = "https://autopatchcn.yuanshen.com/client_app/sophon/chunks/cxgf44wie1a8/keNBn8xtnZIG"
    output_dir = "chunks"  # 所有 chunk 文件保存在这个目录

    download_all_chunks(chunk_ids_file, chunk_prefix, output_dir, max_workers=10)