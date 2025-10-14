# 米哈游启动器

## 米哈游启动器游戏分支信息

**请求方式：** GET

**API端点：**

**国服：**

```
https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGameBranches
```

**国际服：**

```
https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGameBranches
```

**内测（崩坏：因缘精灵）：**

```
https://hyp-api-beta.mihoyo.com/hyp/hyp-connect/api/getGameBranches
https://sg-hyp-api-beta.hoyoverse.com/hyp/hyp-connect/api/getGameBranches
```

**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game_ids[] | str | 游戏ID数组 | 可传入多个游戏ID获取分支信息 |
| launcher_id | str | 启动器ID | 必需参数 |

**启动器ID：**

| ID | 游戏 | 服务器 | 区域 | 备注 |
| -- | --- | ----- | ---- | --- |
| jGHBHlcOq1 | 绝区零<br>崩坏：星穹铁道<br>原神<br>崩坏3 | 官服 | 国服 | |
| VYTpXlbWo8 | 绝区零<br>崩坏：星穹铁道<br>原神<br>崩坏3 | 国际服 | 国际服 | |
| umfgRO5gh5 | 原神 | 哔哩哔哩服 | 国服 | |
| 6P5gHMNyK3 | 崩坏：星穹铁道 | 哔哩哔哩服 | 国服 | |
| xV0f4r1GT0 | 绝区零 | 哔哩哔哩服 | 国服 | |
| TC4836G73s | 崩坏：因缘精灵 | 官服 | 国服 | 一测 |
| 95ODRGH3xC | 崩坏：因缘精灵 | 国际服 | 国际服 | 一测 |

**游戏ID：**

| 游戏ID | 游戏 | 服务器 | 区域 | biz标识 |
|--------|-------|--------|-------|-------|
| 1Z8W5NHUQb | 原神 | 官服 | 国服 | hk4e_cn |
| T2S0Gz4Dr2 | 原神 | 哔哩哔哩服 | 国服 | hk4e_cn |
| osvnlOc0S8 | 崩坏3 | 官服 | 国服 | bh3_cn |
| 64kMb5iAWu | 崩坏：星穹铁道 | 官服 | 国服 | hkrpg_cn |
| EdtUqXfCHh | 崩坏：星穹铁道 | 哔哩哔哩服 | 国服 | hkrpg_cn |
| x6znKlJ0xK | 绝区零 | 官服 | 国服 | nap_cn |
| HXAFlmYa17 | 绝区零 | 哔哩哔哩服 | 国服 | nap_cn |
| j7rlly0oYR | 崩坏：因缘精灵 | 官服 | 国服 | abc_cn |
| gopR6Cufr3 | 原神 | 国际服 | 国际服 | hk4e_global |
| 4ziysqXOQ8 | 崩坏：星穹铁道 | 国际服 | 国际服 | hkrpg_global |
| U5hbdsT9W7 | 绝区零 | 国际服 | 国际服 | nap_global |
| 5TIVvvcwtM<br>g0mMIvshDb<br>uxB4MC7nzC<br>bxPTXSET5t<br> wkE5P5WsIf| 崩坏三 | 欧美服<br>日服<br>韩服<br>东南亚服<br>繁中服 | 国际服 | bh3_global |
| 4qvmDrMwKS | 崩坏：因缘精灵 | 国际服 | 国际服 | abc_global |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | |
| data | obj | 游戏分支信息数据 | 包含各游戏的分支信息 |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game_branches | arr | 游戏分支信息数组 | 包含每个请求游戏的分支信息 |

`data`对象→`game_branches`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game | obj | 游戏基本信息 | 包含游戏ID和biz标识 |
| main | obj | 主分支信息 | 包含版本、包信息等 |
| pre_download | obj/null | 预下载分支信息 | 如无预下载版本则为null |

`game_branches`数组→对象→`game`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| id | str | 游戏唯一ID | 用于标识特定游戏 |
| biz | str | 业务标识 | 如hk4e_cn, bh3_cn等 |

`game_branches`数组→对象→`main`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| package_id | str | 包ID |  |
| branch | str | 分支名称 |  |
| password | str | 密码 | 用于下载验证 |
| tag | str | 当前版本标签 | 如"6.0.0" |
| diff_tags | arr | 差异更新版本标签 | 可用于增量更新 |
| categories | arr | 分类信息数组 | 包含游戏分类标签 |

 `game_branches`数组→对象→`pre_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| package_id | str | 包ID |  |
| branch | str | 分支名称 | |
| password | str | 密码 | 用于下载验证 |
| tag | str | 预下载版本标签 |  |
| diff_tags | arr | 差异更新版本标签 |  |
| categories | arr | 分类信息数组 | 包含游戏分类标签 |

 `main`和`pre_download`对象→`categories`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| category_id | str | 分类ID |  |
| matching_field | str | 匹配字段 | 如"game", "zh-cn" |

<details>
<summary>查看示例</summary>

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

## 米哈游启动器游戏包信息

**请求方式：** GET

**API端点：**

**国服：**

```
https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages
```

**国际服：**

```
https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages
```

**内测（崩坏：因缘精灵）：**

```
https://hyp-api-beta.mihoyo.com/hyp/hyp-connect/api/getGamePackages
https://sg-hyp-api-beta.hoyoverse.com/hyp/hyp-connect/api/getGamePackages
```

**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game_ids[] | str | 游戏ID数组 | 可传入多个游戏ID获取包信息 |
| launcher_id | str | 启动器ID | 必需参数 |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | 通常为"OK" |
| data | obj | 游戏包信息数据 | 包含各游戏的包信息 |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game_packages | arr | 游戏包信息数组 | 包含每个请求游戏的包信息 |

`data`对象→`game_packages`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game | obj | 游戏基本信息 | 包含游戏ID和biz标识 |
| main | obj | 主版本包信息 | 包含当前版本的完整包和补丁 |
| pre_download | obj/null | 预下载版本包信息 | 如无预下载版本则为null |

`game_packages`数组→对象→`game`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| id | str | 游戏唯一ID | 用于标识特定游戏 |
| biz | str | 业务标识 | 如hk4e_cn, bh3_cn等 |

`game_packages`数组→对象→`main`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| major | obj | 主要版本信息 | 包含最新版本的完整包 |
| patches | arr | 补丁信息数组 | 包含从旧版本升级的补丁包 |

`main`对象→`major`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| version | str | 版本号 | 原神的截止到5.5.0 后续改为chunk，无完整包|
| game_pkgs | arr | 游戏包信息数组 | 完整游戏安装包(可能分卷) |
| audio_pkgs | arr | 音频包信息数组 | 各语言音频包 |
| res_list_url | str | 资源列表URL | 拼接pkg_version后得到资源列表文件 |

`major`对象→`game_pkgs`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| url | str | 下载链接 | 游戏包下载地址 |
| md5 | str | MD5校验码 | 用于验证文件完整性 |
| size | str | 压缩包大小 | 以字节为单位的字符串 |
| decompressed_size | str | 解压后大小 | 解压后文件总大小 |

`major`对象→`audio_pkgs`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| language | str | 语言代码 | 如zh-cn, en-us等 |
| url | str | 音频包下载链接 | 该语言音频包地址 |
| md5 | str | MD5校验码 | 音频包完整性校验 |
| size | str | 压缩包大小 | 以字节为单位的字符串 |
| decompressed_size | str | 解压后大小 | 解压后音频文件大小 |

`main`对象→`patches`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| version | str | 源版本号 | 从该版本升级 |
| game_pkgs | arr | 游戏补丁包数组 | 从源版本到当前版本的补丁 |
| audio_pkgs | arr | 音频补丁包数组 | 各语言音频补丁 |
| res_list_url | str | 资源列表URL | 补丁相关资源列表 |

`patches`数组→对象→`game_pkgs`数组→对象：
- 字段结构与`major`→`game_pkgs`数组→对象相同

`patches`数组→对象→`audio_pkgs`数组→对象：
- 字段结构与`major`→`audio_pkgs`数组→对象相同

`game_packages`数组→对象→`pre_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| major | obj/null | 预下载主版本信息 | 如无预下载版本则为null |
| patches | arr | 预下载补丁信息数组 | 预下载版本的补丁信息 |

<details>
<summary>查看示例</summary>

```json
{
  "retcode": 0,
  "message": "OK",
  "data": {
    "game_packages": [
      {
        "game": {
          "id": "x6znKlJ0xK",
          "biz": "nap_cn"
        },
        "main": {
          "major": {
            "version": "2.2.0",
            "game_pkgs": [
              {
                "url": "https://autopatchcn.juequling.com/package_download/op/client_app/download/20250812112735_F9w8fDSRV9mlRWTN/VolumeZip/juequling_2.2.0_AS.zip.001",
                "md5": "9F61BBC0EEF73D854AC0C459D58157EC",
                "size": "6647971840",
                "decompressed_size": "14625538049"
              }
            ],
            "audio_pkgs": [
              {
                "language": "zh-cn",
                "url": "https://autopatchcn.juequling.com/package_download/op/client_app/download/20250812112735_F9w8fDSRV9mlRWTN/audio_zip_Cn.zip",
                "md5": "481924e98e52e07d147ad6d16823bcd3",
                "size": "2256858880",
                "decompressed_size": "4965089536"
              }
            ],
            "res_list_url": "https://autopatchcn.juequling.com/package_download/op/client_app/download/20250812112735_F9w8fDSRV9mlRWTN/SplitAudioZip"
          },
          "patches": [
            {
              "version": "2.1.0",
              "game_pkgs": [
                {
                  "url": "https://autopatchcn.juequling.com/pclauncher/nap_cn/game_2.1.0_2.2.0_hdiff_xARmtyURqIWoaeBq.zip",
                  "md5": "1452a6440cea7cf198da32d88fbed49b",
                  "size": "6634745090",
                  "decompressed_size": "13942289326"
                }
              ],
              "audio_pkgs": [
                {
                  "language": "zh-cn",
                  "url": "https://autopatchcn.juequling.com/pclauncher/nap_cn/audio_zh-cn_2.1.0_2.2.0_hdiff_iMQhEGgLdRuYIJbT.zip",
                  "md5": "7788d3b91a7de1b09ed94ecb624cf8af",
                  "size": "192621612",
                  "decompressed_size": "396597665"
                }
              ],
              "res_list_url": ""
            }
          ]
        },
        "pre_download": {
          "major": null,
          "patches": []
        }
      }
    ]
  }
}
```
</details>

## Sophon分块下载

**请求方式：** GET

**API端点：**

**国服：**

```
https://downloader-api.mihoyo.com/downloader/sophon_chunk/api/getBuild
```

**国际服：**

```
https://sg-downloader-api.hoyoverse.com/downloader/sophon_chunk/api/getBuild
```

**内测（崩坏：因缘精灵）：**

```
https://api-beta.mihoyo.com/downloader/sophon_chunk/api/getBuild
https://sg-beta-api.hoyoverse.com/downloader/sophon_chunk/api/getBuild
```


**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| branch | str | 分支名称 | "main"或"predownload" |
| package_id | str | 包ID | 从getGameBranches获取 |
| password | str | 密码 | 从getGameBranches获取 |
| tag | str | 版本号 | 非必须，默认当前版本，若获取过去的版本branch需为main |
| plat_app | str | 平台应用标识 | 非必须，如"ddxf5qt290cg" |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | 通常为"OK" |
| data | obj | 构建信息数据 | 包含分块下载相关信息 |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| build_id | str | 构建ID |  |
| tag | str | 版本标签 | 如"6.0.0" |
| manifests | arr | 清单信息数组 | 包含各类资源的分块信息 |

`data`对象→`manifests`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| category_id | str | 分类ID | 资源分类唯一标识 |
| category_name | str | 分类名称 | 如"游戏资源-外网" |
| manifest | obj | 清单基本信息 | 包含清单校验信息 |
| chunk_download | obj | 分块下载配置 | 分块文件下载相关配置 |
| manifest_download | obj | 清单下载配置 | 清单文件下载相关配置 |
| matching_field | str | 匹配字段 | 如"game", "zh-cn"等 |
| stats | obj | 统计信息 | 完整资源统计信息 |
| deduplicated_stats | obj | 去重统计信息 | 去重后的资源统计信息 |

`manifests`数组→对象→`manifest`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| id | str | 清单ID | 清单文件唯一标识 |
| checksum | str | 校验码 | 清单文件MD5校验码 |
| compressed_size | str | 压缩大小 | 清单文件压缩后大小 |
| uncompressed_size | str | 解压大小 | 清单文件解压后大小 |

`manifests`数组→对象→`chunk_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| encryption | num | 加密类型 | 0表示未加密 |
| password | str | 下载密码 | 分块下载密码，通常为空 |
| compression | num | 压缩类型 | 1表示启用压缩 |
| url_prefix | str | URL前缀 | 分块文件下载URL前缀 |
| url_suffix | str | URL后缀 | 分块文件下载URL后缀 |

`manifests`数组→对象→`manifest_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| encryption | num | 加密类型 | 0表示未加密 |
| password | str | 下载密码 | 清单下载密码，通常为空 |
| compression | num | 压缩类型 | 1表示启用压缩 |
| url_prefix | str | URL前缀 | 清单文件下载URL前缀 |
| url_suffix | str | URL后缀 | 清单文件下载URL后缀 |

`manifests`数组→对象→`stats`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| compressed_size | str | 压缩总大小 | 所有分块压缩后总大小 |
| uncompressed_size | str | 解压总大小 | 所有分块解压后总大小 |
| file_count | str | 文件数量 | 资源文件总数 |
| chunk_count | str | 分块数量 | 分块文件总数 |

`manifests`数组→对象→`deduplicated_stats`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| compressed_size | str | 去重压缩总大小 | 去重后分块压缩总大小 |
| uncompressed_size | str | 去重解压总大小 | 去重后分块解压总大小 |
| file_count | str | 文件数量 | 资源文件总数 |
| chunk_count | str | 去重分块数量 | 去重后分块文件总数 |

<details>
<summary>查看示例</summary>

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


## Sophon分块下载（预下载）

上述接口若`branch`参数为`predownload`，返回的为下个版本的完整包，并不是增量包，增量包需要另一个接口。

**请求方式：** POST

**API端点：**
```
https://downloader-api.mihoyo.com/downloader/sophon_chunk/api/getPatchBuild
```

**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| branch | str | 分支名称 | "predownload" |
| package_id | str | 包ID | 从getGameBranches获取 |
| password | str | 密码 | 从getGameBranches获取 |
| plat_app | str | 平台应用标识 | 非必需 |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | 通常为"OK" |
| data | obj | 补丁构建信息数据 | 包含补丁分块下载相关信息 |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| build_id | str | 构建ID | 唯一标识该构建版本 |
| patch_id | str | 补丁ID | 唯一标识该补丁版本 |
| tag | str | 目标版本 | 如"2.3.0" |
| manifests | arr | 清单信息数组 | 包含各类资源的补丁分块信息 |

`data`对象→`manifests`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| category_id | str | 分类ID | 资源分类唯一标识 |
| category_name | str | 分类名称 | 如"游戏资源-外网" |
| manifest | obj | 清单基本信息 | 包含清单校验信息 |
| diff_download | obj | 差异下载配置 | 补丁文件下载相关配置 |
| manifest_download | obj | 清单下载配置 | 清单文件下载相关配置 |
| matching_field | str | 匹配字段 | 如"game", "zh-cn"等 |
| stats | obj | 统计信息 | 补丁资源统计信息 |

`manifests`数组→对象→`manifest`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| id | str | 清单ID | 清单文件唯一标识 |
| checksum | str | 校验码 | 清单文件MD5校验码 |
| compressed_size | str | 压缩大小 | 清单文件压缩后大小 |
| uncompressed_size | str | 解压大小 | 清单文件解压后大小 |

`manifests`数组→对象→`diff_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| encryption | num | 加密类型 | 0表示未加密 |
| password | str | 下载密码 | 补丁下载密码，通常为空 |
| compression | num | 压缩类型 | 1表示启用压缩 |
| url_prefix | str | URL前缀 | 补丁文件下载URL前缀 |
| url_suffix | str | URL后缀 | 补丁文件下载URL后缀 |

`manifests`数组→对象→`manifest_download`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| encryption | num | 加密类型 | 0表示未加密 |
| password | str | 下载密码 | 清单下载密码，通常为空 |
| compression | num | 压缩类型 | 1表示启用压缩 |
| url_prefix | str | URL前缀 | 清单文件下载URL前缀 |
| url_suffix | str | URL后缀 | 清单文件下载URL后缀 |

`manifests`数组→对象→`stats`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| {version} | obj | 版本统计信息 | 以源版本号为键的统计信息 |
| compressed_size | str | 压缩总大小 | 补丁分块压缩后总大小 |
| uncompressed_size | str | 解压总大小 | 补丁分块解压后总大小 |
| file_count | str | 文件数量 | 补丁分块文件总数 |
| chunk_count | str | 分块数量 | 补丁分块总数 |

以绝区零`2.3.0`版本预下载为例，`tag`字段为`2.3.0`表示目标版本是`2.3.0`，当 `stats` 对象包含 `{version}` 字段时（如 `2.1.0`, `2.2.0`），表示从该版本升级到`2.3.0`，需要下载对应的补丁分块。当 `stats` 对象为空 `{}` 时，表示从`2.1.0`, `2.2.0`升级到`2.3.0`都无需下载此分块，只有本地无游戏资源，直接下载到`2.3.0`才需要下载此分块，此时可以直接用上个接口。

<details>
<summary>查看示例</summary>

```json
{
  "retcode": 0,
  "message": "OK",
  "data": {
    "build_id": "vSW4X58H3qTt",
    "patch_id": "bYijqL2uIVFZ",
    "tag": "2.3.0",
    "manifests": [
      {
        "category_id": "10047",
        "category_name": "游戏资源-外网",
        "manifest": {
          "id": "manifest_6c4ed0e7f0c3cb52_4944f82d38bef855da3c6516ef149c0d",
          "checksum": "4944f82d38bef855da3c6516ef149c0d",
          "compressed_size": "371602",
          "uncompressed_size": "1491851"
        },
        "diff_download": {
          "encryption": 0,
          "password": "",
          "compression": 1,
          "url_prefix": "https://autopatchcn.juequling.com/pclauncher/diffs/cxi9diu5aadc/2025-09-24/2.3.0/Se5W9E6sLXil/10047",
          "url_suffix": ""
        },
        "manifest_download": {
          "encryption": 0,
          "password": "",
          "compression": 1,
          "url_prefix": "https://autopatchcn.juequling.com/pclauncher/manifests/cxi9diu5aadc/2025-09-24/2.3.0/Se5W9E6sLXil",
          "url_suffix": ""
        },
        "matching_field": "game",
        "stats": {
          "2.2.0": {
            "compressed_size": "7220611294",
            "uncompressed_size": "7220611294",
            "file_count": "7716",
            "chunk_count": "129"
          },
          "2.1.0": {
            "compressed_size": "8966922648",
            "uncompressed_size": "8966922648",
            "file_count": "7716",
            "chunk_count": "159"
          }
        }
      }
    ]
  }
}
```
</details>




















