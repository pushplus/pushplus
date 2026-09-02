# push表单提交后Webhook推送说明

&emsp;&emsp;会员可在表单设置中开启「提交后Webhook推送」。填写者提交（或修改）答卷成功后，push表单会向配置的地址发送 **POST JSON**，便于接入自建系统、低代码平台或消息机器人。

&emsp;&emsp;本文说明的是 **答卷回调到你的地址**，与 pushplus 消息渠道里的 [webhook渠道配置](/doc/extend/webhook.md) 不同：后者是调用 `/send` 把消息推到企业微信、钉钉等；前者是表单收集完成后主动把答卷 POST 出去。

## 使用条件

- **pushplus 会员专享**。非会员保存时 `webhookEnabled` 会被强制为 `false`，填写页提交也不会推送。
- 地址须以 `http://` 或 `https://` 开头，最长 500 字；不可使用本机或内网地址。
- 设置保存在表单的 `settings` 中，**保存后立即生效，无需重新发布**（题目仍以发布快照为准）。

## 如何配置

1. 打开 [push表单](https://www.pushplus.plus/push/pushform) 设计器，进入「设置」→「提交后」。
2. 打开「提交后Webhook推送」，填写 Webhook 地址。
3. 输入地址后失焦（或按回车），系统会先发送一条 **测试请求**。
4. 测试通过后再保存。测试未通过的地址 **不能保存为已开启**，后续答卷也不会向该地址推送。

也可通过开放接口在保存表单设计时写入 `settings.webhookEnabled`、`settings.webhookUrl`。新启用或变更地址时，服务端会同样先发测试请求，未通过则保存失败。详见 [push表单开放接口](/doc/ecosystem/form.html#settings-对象字段)。

## 接收方需返回

请确保地址可公网访问，并在收到请求后响应：

```
{"code": 200, "msg": "success"}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| code | 数字 | 必须为 `200` 才视为成功 |
| msg | 字符串 | 建议固定为 `success`；`code` 非 200 时，该字段会作为失败原因提示 |

HTTP 状态码需为 2xx，且响应体为上述 JSON。测试保存与正式推送均按此规则校验。

## 测试请求

填写或保存地址时，服务端会向该地址 POST 一条测试数据，用于确认地址可访问且响应格式正确。

- 请求方式：POST
- Content-Type: `application/json`
- User-Agent: `PushForm-Webhook/1.0`
- 请求体：

```
{
  "event": "form.webhook.test",
  "formTitle": "用户满意度调查",
  "message": "这是一条Webhook测试请求,用于验证地址是否可访问"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| event | 字符串 | 固定为 `form.webhook.test` |
| formTitle | 字符串 | 当前表单标题 |
| message | 字符串 | 提示这是测试请求 |

> 说明：请根据 `event` 区分测试与正式答卷，避免把测试数据写入业务库。

## 正式推送内容

填写者提交成功后（事务提交之后）异步 POST 答卷。推送失败只记日志，**不影响填写成功**。允许修改答卷时，再次提交也会推送，此时 `updated` 为 `true`。

- 请求方式：POST
- Content-Type: `application/json`
- User-Agent: `PushForm-Webhook/1.0`
- 请求体：

```
{
  "event": "form.submit",
  "formId": 10001,
  "formCode": "a1b2c3d4",
  "formTitle": "用户满意度调查",
  "responseId": 20001,
  "updated": false,
  "submitTime": "2026-08-20 12:00:00",
  "durationMs": 12345,
  "userNickName": "匿名用户",
  "answers": [
    {
      "itemId": "q_name",
      "type": "input",
      "label": "您的姓名",
      "value": "张三"
    },
    {
      "itemId": "q_score",
      "type": "radio",
      "label": "整体满意度",
      "value": "满意"
    }
  ],
  "answerMap": {
    "q_name": "张三",
    "q_score": "满意"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| event | 字符串 | 固定为 `form.submit` |
| formId | 数字 | 表单 id |
| formCode | 字符串 | 表单分享码 |
| formTitle | 字符串 | 表单标题 |
| responseId | 数字 | 答卷 id |
| updated | 布尔 | `true` 表示填写者修改答卷后的再次提交 |
| submitTime | 字符串 | 提交时间，格式 `yyyy-MM-dd HH:mm:ss` |
| durationMs | 数字 | 填写耗时（毫秒） |
| userNickName | 字符串 | 填写人昵称；匿名答卷为「匿名用户」 |
| answers | 数组 | 按题目顺序的答卷明细，见下表 |
| answerMap | 对象 | 以题目 `itemId` 为键、答案为值的映射，便于程序读取 |

#### answers 数组元素

| 字段 | 类型 | 说明 |
|---|---|---|
| itemId | 字符串 | 题目 id |
| type | 字符串 | 题型，见 [题型 type 说明](/doc/ecosystem/form.html#题型-type-说明) |
| label | 字符串 | 题目标题 |
| value | 任意 | 答案；单选/填空为字符串，多选为数组，矩阵/多项填空等为对象或数组 |

分段说明、分页、文本描述等不收集数据的展示题不会出现在 `answers` / `answerMap` 中。

## 注意事项

- 连接超时约 5 秒、读取超时约 10 秒；不会跟随 HTTP 重定向。
- 已保存且测试通过的地址，后续答卷都会尝试推送。若接收方后来临时不可用，不影响填写成功，只会推送失败。
- 测试未通过（未返回 `{"code": 200, "msg": "success"}`）的地址不会开启推送。
- 会员过期后，即使设置里仍留有地址，提交时也不会再推送。
