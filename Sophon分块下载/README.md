# Sophon Chunk 下载系统完整流程

本文档详细介绍了从 API 请求到文件下载的完整流程，基于原神等米哈游游戏的 Sophon chunk 下载系统。


## 第一步: 获取版本信息

### API 端点

https://github.com/Furina1027/miHoYo-api/blob/main/%E5%90%AF%E5%8A%A8%E5%99%A8/launcher.md#%E7%B1%B3%E5%93%88%E6%B8%B8%E5%90%AF%E5%8A%A8%E5%99%A8%E6%B8%B8%E6%88%8F%E5%88%86%E6%94%AF%E4%BF%A1%E6%81%AF

- **CN 服务器**: `hyp-api.mihoyo.com`, launcher_id: `jGHBHlcOq1`
- **Global 服务器**: `sg-hyp-api.hoyoverse.com`, launcher_id: `VYTpXlbWo8`

### 响应示例

```json
{
  "retcode": 0,
  "data": {
    "game_branches": [
      {
        "game": {"biz": "hk4e_cn"},
        "main": {
          "package_id": "xxx",
          "branch": "main",
          "password": "xxx",
          "tag": "6.0.0"
        }
      }
    ]
  }
}
```

## 第二步: 请求 getBuild API

### API 端点

```
GET https://{host}/downloader/sophon_chunk/api/getBuild?branch={branch}&package_id={package_id}&password={password}
```

- **CN 服务器**: `downloader-api.mihoyo.com`
- **Global 服务器**: `sg-downloader-api.hoyoverse.com`

### 响应结构

```json
{
  "retcode": 0,
  "data": {
    "build_id": "fRVqBXREJxgT",
    "tag": "6.0.0",
    "manifests": [
      {
        "category_name": "游戏资源-外网",
        "manifest": {
          "id": "manifest_447a8efc62cc9c01_...",
          "compressed_size": "6291414",
          "uncompressed_size": "11759785"
        },
        "chunk_download": {
          "url_prefix": "https://autopatchcn.yuanshen.com/client_app/sophon/chunks/...  "
        },
        "manifest_download": {
          "url_prefix": "https://autopatchcn.yuanshen.com/client_app/sophon/manifests/...  "
        },
        "stats": {
          "file_count": "2298",
          "chunk_count": "79218"
        }
      }
    ]
  }
}
```

## 第三步: 下载并解析 Manifest

### Manifest URL 构造

```
manifest_download.url_prefix + "/" + manifest.id
```

例如:
```
https://autopatchcn.yuanshen.com/client_app/sophon/manifests/cxgf44wie1a8/keNBn8xtnZIG/manifest_447a8efc62cc9c01_5b94c65f18a898c898ac1d015e141423  
```

### Python 实现

```python
import requests
import zstandard as zstd
import Sophon_pb2

def zstd_get(url):
    """下载并解压 Zstd 压缩数据"""
    response = requests.get(url, verify=False)
    dctx = zstd.ZstdDecompressor()
    return dctx.decompress(response.content)

def download_manifest(manifest_url):
    """下载并解析 manifest"""
    manifest_data = zstd_get(manifest_url)
    manifest = Sophon_pb2.SophonChunkManifest()
    manifest.ParseFromString(manifest_data)
    return manifest
```

### Protobuf 定义

需要先创建 `Sophon.proto` 文件:

```protobuf
syntax = "proto3";

message SophonChunkManifest {
    repeated SophonChunkFile chuncks = 1;
}

message SophonChunkFile {
    string file = 1;
    repeated SophonChunk chunks = 2;
    bool is_folder = 3;
    int64 size = 4;
    string md5 = 5;
}

message SophonChunk {
    string id = 1;
    string uncompressed_md5 = 2;
    int64 offset = 3;
    int64 compressed_size = 4;
    int64 uncompressed_size = 5;
    int64 unknown = 6;
    string compressed_md5 = 7;
}
```

生成 Python 代码:
```bash
protoc --python_out=. Sophon.proto
```

## 第四步: 提取 Chunk 信息

### Manifest 数据结构

每个 manifest 包含多个文件，每个文件包含多个 chunk:

```python
for file in manifest.chuncks:
    print(f"文件: {file.file}, 大小: {file.size}, MD5: {file.md5}")
    for chunk in file.chunks:
        print(f"  Chunk ID: {chunk.id}")
        print(f"  偏移量: {chunk.offset}")
        print(f"  压缩大小: {chunk.compressed_size}")
        print(f"  解压大小: {chunk.uncompressed_size}")
```

### 导出 Chunk 列表

```python
def export_chunks(manifest):
    chunks = []
    for file in manifest.chuncks:
        for chunk in file.chunks:
            chunks.append({
                'file': file.file,
                'chunk_id': chunk.id,
                'offset': chunk.offset,
                'compressed_size': chunk.compressed_size,
                'uncompressed_size': chunk.uncompressed_size,
                'uncompressed_md5': chunk.uncompressed_md5
            })
    return chunks
```

## 第五步: 下载 Chunks

### Chunk URL 构造

```
chunk_download.url_prefix + "/" + chunk.id
```

例如:
```
https://autopatchcn.yuanshen.com/client_app/sophon/chunks/cxgf44wie1a8/keNBn8xtnZIG/7235f0b611e65fef_044cd9c617cb5d49a02b46ec53710b07  
```

### 并发下载实现

Python 实现:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_file_chunks(file_name, chunks, chunk_prefix, max_workers=10):
    """并发下载单个文件的所有 chunks"""
    file_size = max(c['offset'] + c['uncompressed_size'] for c in chunks)
    file_buffer = bytearray(file_size)
    
    def download_chunk(chunk):
        url = f"{chunk_prefix}/{chunk['chunk_id']}"
        data = zstd_get(url)
        return {'offset': chunk['offset'], 'data': data}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_chunk, c) for c in chunks]
        
        for future in as_completed(futures):
            result = future.result()
            start = result['offset']
            end = start + len(result['data'])
            file_buffer[start:end] = result['data']
    
    return file_buffer
```

## 第六步: 组装和验证文件

### 按偏移量组装

每个 chunk 的 `offset` 字段指定了数据在最终文件中的位置:

```python
# 预分配缓冲区
file_buffer = bytearray(file.size)

# 将每个 chunk 复制到正确位置
for chunk_result in downloaded_chunks:
    start = chunk_result['offset']
    end = start + len(chunk_result['data'])
    file_buffer[start:end] = chunk_result['data']
```

### MD5 验证

```python
import hashlib

def verify_and_save(file_buffer, file_path, expected_md5):
    """验证 MD5 并保存文件"""
    # 计算 MD5
    md5_hash = hashlib.md5(file_buffer).hexdigest()
    
    if md5_hash != expected_md5:
        print(f"MD5 不匹配: {md5_hash} != {expected_md5}")
        return False
    
    # 创建目录并保存
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(file_buffer)
    
    return True
```

## 第七步: 完整下载流程

### 逐文件处理

为了降低内存占用，建议逐个文件处理:

```python
def download_all_files(manifest, chunk_prefix, output_dir):
    """逐文件下载并保存"""
    for file in manifest.chuncks:
        print(f"下载: {file.file}")
        
        # 按文件分组 chunks
        chunks = [{
            'chunk_id': c.id,
            'offset': c.offset,
            'uncompressed_size': c.uncompressed_size
        } for c in file.chunks]
        
        # 下载并组装
        file_buffer = download_file_chunks(file.file, chunks, chunk_prefix)
        
        # 验证并保存
        file_path = os.path.join(output_dir, file.file)
        if verify_and_save(file_buffer, file_path, file.md5):
            print(f"✓ 保存成功: {file.file}")
        else:
            print(f"✗ 验证失败: {file.file}")
```

### 重试机制

```python
def download_with_retry(file, chunk_prefix, output_dir, max_retries=3):
    """带重试的文件下载"""
    for attempt in range(max_retries):
        try:
            chunks = [...]  # 提取 chunks
            file_buffer = download_file_chunks(file.file, chunks, chunk_prefix)
            
            if verify_and_save(file_buffer, output_dir, file.md5):
                return True
        except Exception as e:
            print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
    
    return False
```

## 完整 Python 示例

```python
import json
import requests
import zstandard as zstd
import hashlib
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import Sophon_pb2
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def zstd_get(url):
    """下载并解压 Zstd 数据"""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            dctx = zstd.ZstdDecompressor()
            return dctx.decompress(response.content)
        except Exception as e:
            if attempt == 2:
                raise
    return None

def download_manifest(manifest_url):
    """下载并解析 manifest"""
    data = zstd_get(manifest_url)
    manifest = Sophon_pb2.SophonChunkManifest()
    manifest.ParseFromString(data)
    return manifest

def download_file(file, chunk_prefix, chunk_prefix_url, output_dir, max_workers=10):
    """下载单个文件的所有 chunks 并组装"""
    print(f"正在下载: {file.file}")
    
    # 预分配文件缓冲区
    file_buffer = bytearray(file.size)
    
    # 准备下载任务
    def download_chunk(chunk):
        chunk_url = f"{chunk_prefix_url}/{chunk.id}"
        chunk_data = zstd_get(chunk_url)
        return {
            'offset': chunk.offset,
            'data': chunk_data,
            'chunk_id': chunk.id
        }
    
    # 并发下载 chunks
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        chunk_futures = [executor.submit(download_chunk, chunk) for chunk in file.chunks]
        
        # 等待所有 chunks 下载完成并组装
        for future in as_completed(chunk_futures):
            try:
                result = future.result()
                start = result['offset']
                end = start + len(result['data'])
                file_buffer[start:end] = result['data']
            except Exception as e:
                print(f"下载 chunk {result['chunk_id']} 失败: {e}")
                raise
    
    # 验证 MD5
    calculated_md5 = hashlib.md5(file_buffer).hexdigest()
    if calculated_md5.lower() != file.md5.lower():
        raise ValueError(f"MD5 验证失败: {calculated_md5} != {file.md5}")
    
    # 保存文件
    file_path = os.path.join(output_dir, file.file)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as f:
        f.write(file_buffer)
    
    print(f"✓ 已保存: {file.file}")
    return True

def download_all_files(manifest, chunk_prefix_url, output_dir):
    """下载 manifest 中的所有文件"""
    total_size = sum(file.size for file in manifest.chuncks)
    print(f"总大小: {total_size / 1024 / 1024 / 1024:.2f} GB")
    print(f"文件数量: {len(manifest.chuncks)}")
    
    success_count = 0
    for file in manifest.chuncks:
        retry_count = 0
        while retry_count < 3:
            try:
                if download_file(file, file.chunks, chunk_prefix_url, output_dir):
                    success_count += 1
                    break
            except Exception as e:
                retry_count += 1
                print(f"下载 {file.file} 失败 (尝试 {retry_count}/3): {e}")
        
        if retry_count == 3:
            print(f"✗ 最终失败: {file.file}")
    
    print(f"下载完成: {success_count}/{len(manifest.chuncks)} 个文件")
    return success_count == len(manifest.chuncks)

# 使用示例
if __name__ == "__main__":
    # 假设已获取到 manifest_url 和 chunk_prefix_url
    manifest = download_manifest(manifest_url)
    download_all_files(manifest, chunk_prefix_url, "./downloaded_files/")
```
