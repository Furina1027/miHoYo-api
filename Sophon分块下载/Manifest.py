"""下载并解析 Sophon manifest（zstd 压缩的 protobuf），导出 chunk_ids.json。

用法:
    python Manifest.py <manifest_url>

manifest_url = manifest_download.url_prefix + "/" + manifest.id
"""
import argparse
import json

import requests
import zstandard as zstd
from google.protobuf import message

# 需要先从 Sophon.proto 生成 Python protobuf 文件: protoc --python_out=. Sophon.proto
import Sophon_pb2


def zstd_get(url, retries=3):
    """下载并解压 Zstd 压缩的数据"""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return zstd.ZstdDecompressor().decompress(response.content)
        except Exception as e:
            print(f"下载失败 (尝试 {attempt}/{retries}): {e}")
    return None


def download_and_parse_manifest(manifest_url):
    """下载并解析 manifest 文件"""
    manifest_data = zstd_get(manifest_url)
    if not manifest_data:
        print("下载 manifest 失败")
        return None

    manifest = Sophon_pb2.SophonChunkManifest()
    try:
        manifest.ParseFromString(manifest_data)
        return manifest
    except message.DecodeError as e:
        print(f"解析 manifest 失败: {e}")
        return None


def export_all_chunk_ids(manifest):
    """从 manifest 中提取所有 chunk 信息（附带文件级大小与 MD5，供下载后校验）"""
    def to_hex_str(val):
        return val.hex() if isinstance(val, bytes) else str(val)

    all_chunks = []
    for file in manifest.chunks:
        for chunk in file.chunks:
            all_chunks.append({
                'file': file.file,
                'file_size': file.size,
                'file_md5': file.md5,
                'chunk_id': chunk.id,
                'offset': chunk.offset,
                'compressed_size': chunk.compressed_size,
                'uncompressed_size': chunk.uncompressed_size,
                'compressed_md5': to_hex_str(chunk.compressed_md5),
                'uncompressed_md5': to_hex_str(chunk.uncompressed_md5),
            })
    return all_chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="下载并解析 Sophon manifest，导出 chunk_ids.json")
    parser.add_argument("manifest_url", help="manifest 下载地址: manifest_download.url_prefix + / + manifest.id")
    args = parser.parse_args()

    manifest = download_and_parse_manifest(args.manifest_url)
    if not manifest:
        raise SystemExit(1)

    chunks = export_all_chunk_ids(manifest)
    print(f"总共 {len(chunks)} 个 chunk")

    for i, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {i + 1}:")
        print(f"  文件: {chunk['file']}")
        print(f"  Chunk ID: {chunk['chunk_id']}")
        print(f"  偏移量: {chunk['offset']}")
        print(f"  压缩大小: {chunk['compressed_size']}")
        print(f"  解压大小: {chunk['uncompressed_size']}")

    with open('chunk_ids.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print("\n所有 chunk 信息已保存到 chunk_ids.json")
