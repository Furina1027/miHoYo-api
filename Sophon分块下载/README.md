# Sophon Chunk 下载系统完整流程

本文档详细介绍了从 API 请求到文件下载的完整流程，以原神为例。


## 第一步: 获取版本信息

https://github.com/Furina1027/miHoYo-api/blob/main/launcher/launcher.md#%E7%B1%B3%E5%93%88%E6%B8%B8%E5%90%AF%E5%8A%A8%E5%99%A8%E6%B8%B8%E6%88%8F%E5%88%86%E6%94%AF%E4%BF%A1%E6%81%AF

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
          "tag": "6.0.0",
          "diff_tags": [
            "5.8.0",
            "5.7.0"
          ],
          "categories": [
            {
              "category_id": "10017",
              "matching_field": "game"
            },
            {
              "category_id": "10018",
              "matching_field": "zh-cn"
            },
            {
              "category_id": "10019",
              "matching_field": "en-us"
            },
            {
              "category_id": "10021",
              "matching_field": "ja-jp"
            },
            {
              "category_id": "10020",
              "matching_field": "ko-kr"
            }
          ]
        },
        "pre_download": null
      }
    ]
  }
}
```
</details>
需要其中的`package_id`,`branch`,`password`

## 第二步: 获取Sophon分块信息

https://github.com/Furina1027/miHoYo-api/blob/main/launcher/launcher.md#sophon%E5%88%86%E5%9D%97%E4%B8%8B%E8%BD%BD

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
      },
      {
        "category_id": "10018",
        "category_name": "语音包-中文-外网",
        "manifest": {
          "id": "manifest_02a289d4e886c74d_15cd4224f71a0bcef2b305f629396eac",
          "checksum": "15cd4224f71a0bcef2b305f629396eac",
          "compressed_size": "1275002",
          "uncompressed_size": "2369368"
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
        "matching_field": "zh-cn",
        "stats": {
          "compressed_size": "15930548130",
          "uncompressed_size": "18468421533",
          "file_count": "162",
          "chunk_count": "16176"
        },
        "deduplicated_stats": {
          "compressed_size": "15930273559",
          "uncompressed_size": "18468101109",
          "file_count": "162",
          "chunk_count": "16175"
        }
      },
      {
        "category_id": "10019",
        "category_name": "语音包-英文-外网",
        "manifest": {
          "id": "manifest_ecbe3407ed3014ba_36ec283737b7cc4c516c1e6e17174543",
          "checksum": "36ec283737b7cc4c516c1e6e17174543",
          "compressed_size": "1407964",
          "uncompressed_size": "2609784"
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
        "matching_field": "en-us",
        "stats": {
          "compressed_size": "18786783763",
          "uncompressed_size": "21164826818",
          "file_count": "162",
          "chunk_count": "17821"
        },
        "deduplicated_stats": {
          "compressed_size": "18786783763",
          "uncompressed_size": "21164826818",
          "file_count": "162",
          "chunk_count": "17821"
        }
      },
      {
        "category_id": "10021",
        "category_name": "语音包-日文-外网",
        "manifest": {
          "id": "manifest_df63d982899ac9e6_ec61815bf1f4a04ead646fdccfe0ea9b",
          "checksum": "ec61815bf1f4a04ead646fdccfe0ea9b",
          "compressed_size": "1563663",
          "uncompressed_size": "2909147"
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
        "matching_field": "ja-jp",
        "stats": {
          "compressed_size": "18564857626",
          "uncompressed_size": "23951053996",
          "file_count": "162",
          "chunk_count": "19879"
        },
        "deduplicated_stats": {
          "compressed_size": "18564857626",
          "uncompressed_size": "23951053996",
          "file_count": "162",
          "chunk_count": "19879"
        }
      },
      {
        "category_id": "10020",
        "category_name": "语音包-韩文-外网",
        "manifest": {
          "id": "manifest_9ec87fc7cca89c19_ccb2564a5e5691c19b642e801fd0bbf6",
          "checksum": "ccb2564a5e5691c19b642e801fd0bbf6",
          "compressed_size": "1203777",
          "uncompressed_size": "2234129"
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
        "matching_field": "ko-kr",
        "stats": {
          "compressed_size": "15534106403",
          "uncompressed_size": "18271152490",
          "file_count": "162",
          "chunk_count": "15247"
        },
        "deduplicated_stats": {
          "compressed_size": "15534106403",
          "uncompressed_size": "18271152490",
          "file_count": "162",
          "chunk_count": "15247"
        }
      }
    ]
  }
}
```
</details>

## 第三步: 下载并解析 Manifest并导出chunkid

### Manifest URL 构造

```
manifest_download.url_prefix + "/" + manifest.id
```

例如:
```
https://autopatchcn.yuanshen.com/client_app/sophon/manifests/cxgf44wie1a8/keNBn8xtnZIG/manifest_447a8efc62cc9c01_5b94c65f18a898c898ac1d015e141423  
```
直接在浏览器访问上述完整 URL 可以手动下载manifest，以下是自动下载并解析的步骤。

### Protobuf 定义

需要先创建 `Sophon.proto` 文件，可以直接下载项目中的`Sophon.proto`文件

生成 Python 代码:
```bash
protoc --python_out=. Sophon.proto
```
运行后`Sophon.proto`同目录下会自动生成`Sophon_pb2.py`文件

### Python 解析

依赖安装

```bash
pip install requests zstandard protobuf
```
确保目录下已有`Sophon_pb2.py`文件

运行`Manifest.py`

 ```bash
   python manifest_parser.py
   ```

解析完成后会生成 `chunk_ids.json` 文件，格式如下：
```json
[
 {
    "file": "HoYoKProtect.sys",
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
直接在浏览器访问上述URL 可以下载单个chunk

### 下载并组装

Python 实现:

确保已经生成格式正确的`chunk_ids.json` 文件

运行`chunkdownloaded.py`

 ```bash
   python sophon_downloader.py
   ```

下载完成后，文件在`downloaded_files`文件夹

若不想组装，只下载chunk文件，运行`chunkdownloaded2.py`文件

 ```bash
   python sophon_downloader2.py
   ```
chunk文件会保存到`chunk`文件夹



















