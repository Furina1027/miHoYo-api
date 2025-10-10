import requests
import zstandard as zstd
from google.protobuf import message
# 需要先从 Sophon.proto 生成 Python protobuf 文件
import Sophon_pb2


def zstd_get(url):
    """下载并解压 Zstd 压缩的数据"""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 使用 zstandard 解压
            dctx = zstd.ZstdDecompressor()
            decompressed_data = dctx.decompress(response.content)
            return decompressed_data
        except Exception as e:
            print(f"下载失败 (尝试 {attempt + 1}/3): {e}")
            if attempt == 2:
                return None
    return None


def download_and_parse_manifest(manifest_url):
    """下载并解析 manifest 文件"""
    # 1. 使用 ZstdGet 下载 manifest 文件
    manifest_data = zstd_get(manifest_url)
    if not manifest_data:
        print("下载 manifest 失败")
        return None

        # 2. 使用 Protocol Buffers 反序列化
    manifest = Sophon_pb2.SophonChunkManifest()
    try:
        manifest.ParseFromString(manifest_data)
        return manifest
    except message.DecodeError as e:
        print(f"解析 manifest 失败: {e}")
        return None

    # 使用示例
def export_all_chunk_ids(manifest):
        """导出所有 chunk ID"""
        all_chunks = []

        for file in manifest.chuncks:
            for chunk in file.chunks:
                chunk_info = {
                    'file': file.file,
                    'chunk_id': chunk.id,
                    'offset': chunk.offset,
                    'compressed_size': chunk.compressed_size,
                    'uncompressed_size': chunk.uncompressed_size,
                    'compressed_md5': chunk.compressed_md5,
                    'uncompressed_md5': chunk.uncompressed_md5
                }
                all_chunks.append(chunk_info)

        return all_chunks

if __name__ == "__main__":
        manifest_url = "https://autopatchcn.yuanshen.com/client_app/sophon/manifests/cxgf44wie1a8/keNBn8xtnZIG/manifest_02a289d4e886c74d_15cd4224f71a0bcef2b305f629396eac"

        manifest = download_and_parse_manifest(manifest_url)

        if manifest:
            # 导出所有 chunk ID
            chunks = export_all_chunk_ids(manifest)

            print(f"总共 {len(chunks)} 个 chunk")

            # 打印前几个示例
            for i, chunk in enumerate(chunks[:10]):
                print(f"\nChunk {i + 1}:")
                print(f"  文件: {chunk['file']}")
                print(f"  Chunk ID: {chunk['chunk_id']}")
                print(f"  偏移量: {chunk['offset']}")
                print(f"  压缩大小: {chunk['compressed_size']}")
                print(f"  解压大小: {chunk['uncompressed_size']}")

                # 保存到文件
            import json
            with open('chunk_ids.json', 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            print(f"\n所有 chunk 信息已保存到 chunk_ids.json")
