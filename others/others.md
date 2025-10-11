# 前瞻直播兑换码

**请求方式：** GET

**API端点：**
```
https://api-takumi-static.mihoyo.com/event/miyolive/refreshCode
```

**请求头：**
```
x-rpc-act_id: {活动ID}
```
- **活动ID**: 米游社直播间URL中的`act_id`，如原神6.1前瞻直播间URL`https://webstatic.mihoyo.com/bbs/event/live/index.html?act_id=ea202509221143399804`，`act_id`为`ea202509221143399804`，若没有这个请求头，会返回活动已结束，返回码`-500012`。

**参数：**

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| version | str | d91cb1 | 固定值 |
| time | num | 时间戳 | 秒级Unix时间戳，当前时间 |

**JSON返回：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| retcode | num | 返回码 | 0表示成功 |
| message | str | 返回消息 | 通常为"OK" |
| data | obj | 兑换码信息数据 | 包含所有可用兑换码 |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| code_list | arr | 兑换码列表 | 包含所有可用的兑换码信息 |

`data`对象→`code_list`数组→对象：

| 字段 | 类型 | 内容 | 备注 |
|------|------|------|------|
| title | str | 奖励描述 | HTML格式的奖励内容描述 |
| code | str | 兑换码 | 可在游戏中使用的兑换码 |
| img | str | 奖励图片URL | 奖励图标URL |
| to_get_time | num | 可使用时间 | Unix时间戳，表示该兑换码的可使用时间 |

<details>
<summary>查看示例</summary>

```json
{
  "retcode": 0,
  "message": "OK",
  "data": {
    "code_list": [
      {
        "title": "<p style=\"white-space: pre-wrap;\">原石*<span style=\"color:rgba(255,173,210,1)\">100</span> 精锻用魔矿*<span style=\"color:rgba(255,173,210,1)\">10</span></p>",
        "code": "原神奈芙尔月之二上线",
        "img": "https://webstatic.mihoyo.com/upload/op-public/2023/04/20/2ac4e2cdf1323b88dee21535ca309776_2153184369291799401.png",
        "to_get_time": "1760098290"
      },
      {
        "title": "<p style=\"white-space: pre-wrap;\">原石*<span style=\"color:rgba(255,173,210,1)\">100</span><span style=\"color:rgba(38,38,38,1)\"> </span>大英雄的经验*<span style=\"color:rgba(255,173,210,1)\">5</span></p>",
        "code": "月之二再战猎月人",
        "img": "https://webstatic.mihoyo.com/upload/op-public/2023/04/20/c3acaca2b90a30602563907db26d1f98_2838188309465475516.png",
        "to_get_time": "1760098650"
      },
      {
        "title": "<p style=\"white-space: pre-wrap;\">原石*<span style=\"color:rgba(255,173,210,1)\">100</span> 摩拉*<span style=\"color:rgba(255,173,210,1)\">50000</span></p>",
        "code": "我现在就要玩千星奇域",
        "img": "https://webstatic.mihoyo.com/upload/op-public/2023/04/20/28a9ff9f20a5e0ad0bc420dda4c7cb2a_6963573865784698666.png",
        "to_get_time": "1760099850"
      }
    ]
  }
}
```
</details>
