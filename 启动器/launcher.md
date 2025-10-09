# 游戏启动器信息
## 米哈游启动器游戏分支信息API指南

**请求方式：** GET

**API端点：**
```
https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGameBranches
```

**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| game_ids[] | str | 游戏ID数组 | 可传入多个游戏ID获取分支信息 |
| launcher_id | str | 启动器ID | 必需参数 |

**支持的游戏ID：**

| 游戏ID | 对应游戏 | biz标识 |
|--------|----------|---------|
| 1Z8W5NHUQb | 《原神》国服 | hk4e_cn |
| osvnlOc0S8 | 《崩坏3》国服 | bh3_cn |
| 64kMb5iAWu | 《崩坏：星穹铁道》国服 | hkrpg_cn |
| x6znKlJ0xK | 《绝区零》国服 | nap_cn |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | 通常为"OK" |
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
| package_id | str | 包ID | 游戏安装包唯一标识 |
| branch | str | 分支名称 | 通常为"main" |
| password | str | 密码 | 用于下载验证 |
| tag | str | 当前版本标签 | 如"6.0.0" |
| diff_tags | arr | 差异更新版本标签 | 可用于增量更新 |
| categories | arr | 分类信息数组 | 包含语言和游戏分类 |

`main`对象→`categories`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| category_id | str | 分类ID | 数字字符串 |
| matching_field | str | 匹配字段 | 可能是语言代码或分类标识 |

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
