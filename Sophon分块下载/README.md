# Sophon Chunk 下载系统完整流程

本文档详细介绍了从 API 请求到文件下载的完整流程，以原神为例。

## 环境准备

```bash
pip install -r requirements.txt   # requests / zstandard / protobuf
protoc --python_out=. Sophon.proto
```

运行后在 `Sophon.proto` 同目录下会生成 `Sophon_pb2.py` 文件。

## 第一步: 获取版本信息

见 [../launcher/launcher.md](../launcher/launcher.md#米哈游启动器游戏分支信息)。

<details>
<summary>查看响应示例</summary>

```json
{
  "retcode": 0,
  "message": "OK",
  "data": {
    "game_branches": [
      {
        "game": {
          "id": "1Z8W5NHUQb",
          "biz": "hk4e_cn"
        },
        "main": {
          "package_id": "8xfMve0uwQ",
          "branch": "main",
          "password": "CW8GbLNU8f",
          "tag": "7.0.0",
          "diff_tags": [
            "6.7.0",
            "6.6.0"
          ],
          "categories": [
            {
              "category_id": "10017",
              "matching_field": "game",
              "type": "CATEGORY_TYPE_RESOURCE",
              "scenarios": [
                "CATEGORY_SCENARIO_FULL"
              ]
            }
          ],
          "required_client_version": ""
        },
        "pre_download": null
      }
    ]
  }
}
```
</details>

需要其中的 `package_id`、`branch`、`password`。

## 第二步: 获取 Sophon 分块信息

见 [../launcher/launcher.md](../launcher/launcher.md#sophon分块下载)。

<details>
<summary>查看响应示例</summary>

```json
{
  "retcode": 0,
  "message": "OK",
  "data": {
    "build_id": "fRVqBXREJxgT",
    "tag": "6.0.0",
    "manifests": [
      {
        "category_id": "10017",
        "category_name": "游戏资源-外网",
        "manifest": {
          "id": "manifest_447a8efc62cc9c01_5b94c65f18a898c898ac1d015e141423",
          "checksum": "5b94c65f18a898c898ac1d015e141423",
          "compressed_size": "6291414",
          "uncompressed_size": "11759785"
        },
        "chunk_download": {
          "encryption": 0,
          "password": "",
          "compression": 1,
          "url_prefix": "https://autopatchcn.yuanshen.com/client_app/sophon/chunks/cxgf44wie1a8/keNBn8xtnZIG",
          "url_suffix": ""
        },
        "manifest_download": {
          "encryption": 0,
          "password": "",
          "compression": 1,
          "url_prefix": "https://autopatchcn.yuanshen.com/client_app/sophon/manifests/cxgf44wie1a8/keNBn8xtnZIG",
          "url_suffix": ""
        },
        "matching_field": "game",
        "stats": {
          "compressed_size": "89392824348",
          "uncompressed_size": "91705439345",
          "file_count": "2298",
          "chunk_count": "79218"
        },
        "deduplicated_stats": {
          "compressed_size": "89294554661",
          "uncompressed_size": "91572064024",
          "file_count": "2298",
          "chunk_count": "79107"
        }
      }
    ]
  }
}
```
</details>

## 第三步: 下载并解析 Manifest 并导出 chunk 信息

### Manifest URL 构造

```
manifest_download.url_prefix + "/" + manifest.id
```

例如:

```
https://autopatchcn.yuanshen.com/client_app/sophon/manifests/cxgf44wie1a8/keNBn8xtnZIG/manifest_447a8efc62cc9c01_5b94c65f18a898c898ac1d015e141423  
```

直接在浏览器访问上述完整 URL 可以手动下载 manifest，以下是自动下载并解析的步骤。

### 运行 Manifest.py

```bash
python Manifest.py <manifest_url>
```

解析完成后会生成 `chunk_ids.json` 文件，格式如下：

```json
[
  {
    "file": "HoYoKProtect.sys",
    "file_size": 1309507,
    "file_md5": "044cd9c617cb5d49a02b46ec53710b07",
    "chunk_id": "7235f0b611e65fef_044cd9c617cb5d49a02b46ec53710b07",
    "offset": 0,
    "compressed_size": 1181056,
    "uncompressed_size": 1309507,
    "compressed_md5": "09a3550ced31661a793e6796b095a5ec",
    "uncompressed_md5": "044cd9c617cb5d49a02b46ec53710b07"
  }
]
```

## 第四步: 下载 Chunks

### Chunk URL 构造

```
chunk_download.url_prefix + "/" + chunk.id
```

例如:

```
https://autopatchcn.yuanshen.com/client_app/sophon/chunks/cxgf44wie1a8/keNBn8xtnZIG/7235f0b611e65fef_044cd9c617cb5d49a02b46ec53710b07  
```

直接在浏览器访问上述 URL 可以下载单个 chunk。

### 下载并组装成完整文件

```bash
python chunkdownloaded.py <chunk_ids.json> <chunk_prefix> [output_dir] [max_workers]
```

按 `offset` 将各 chunk 拼接还原，过程中逐 chunk 校验 MD5，最终对整个文件做 MD5 校验。下载完成后文件保存在 `downloaded_files` 文件夹。

### 只下载 chunk（不组装）

```bash
python chunkdownloaded2.py <chunk_ids.json> <chunk_prefix> [output_dir] [max_workers]
```

chunk 文件（以 chunk_id 命名）会保存到 `chunks` 文件夹，同样会做 MD5 校验。
