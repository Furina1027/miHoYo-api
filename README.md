# miHoYo-api

米哈游启动器（国服 / 国际服）API 文档，以及 Sophon 分块下载协议的解析与示例脚本。

## 目录

| 路径 | 内容 |
|------|------|
| [launcher/launcher.md](launcher/launcher.md) | 启动器 API：游戏分支信息 / 游戏包信息 / Sophon 分块下载（含预下载增量补丁） |
| [Sophon分块下载/](Sophon分块下载/README.md) | Sophon chunk 完整下载流程文档 + Python 示例脚本（manifest 解析、chunk 下载组装） |
| [others/others.md](others/others.md) | 其他接口：前瞻直播兑换码 |

## 接口一览

| 接口 | 方式 | 端点 | 用途 |
|------|------|------|------|
| getGameBranches | GET | `hyp-api.mihoyo.com`（国服）<br>`sg-hyp-api.hoyoverse.com`（国际服） | 取游戏分支的 `package_id` / `password` / 版本 `tag` |
| getGamePackages | GET | 同上 | 老式完整包 / 补丁包 / 音频包直链（部分游戏已停用） |
| getBuild | GET | `downloader-api.mihoyo.com`（国服）<br>`sg-downloader-api.hoyoverse.com`（国际服） | 当前版本 Sophon 分块清单信息 |
| getPatchBuild | POST | 同上 | 预下载版本的增量补丁清单信息 |
| refreshCode | GET | `api-takumi-static.mihoyo.com` | 前瞻直播兑换码 |

各接口的参数与返回字段详见 [launcher/launcher.md](launcher/launcher.md) 与 [others/others.md](others/others.md)。

## Sophon 分块下载流程

1. `getGameBranches` 取游戏的 `package_id`、`password`
2. `getBuild` 取各资源分类的 `manifest_download.url_prefix` 与 manifest id
3. 下载 manifest（zstd 压缩的 protobuf），解析出所有 chunk
4. 按 `url_prefix + chunk_id` 下载 chunk，按 `offset` 组装成完整文件，MD5 校验

完整步骤与可直接运行的脚本见 [Sophon分块下载/README.md](Sophon分块下载/README.md)。

## 声明

1. **请勿滥用，本项目仅用于学习和测试！**
2. 利用本项目提供的接口造成不良影响及后果与本人无关。
