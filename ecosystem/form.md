# push表单开放接口文档 V1.0.4

::: details 点击展开版本更新日志

> 1.0 接口更新日期：2026-08-06\
> 首次发布：表单列表、创建、复制、保存设计、详情、发布差异、发布、停止收集、删除
>
> 1.0.1 接口更新日期：2026-08-11\
> 补充 `theme`、`settings` 对象字段说明
>
> 1.0.2 文档更新日期：2026-08-18\
> 文档体例与主站开放接口对齐；分页入参与主站一致（`current` / `pageSize` / `params`），默认 `pageSize` 调整为 20，响应补充 `pages`；补充推送说明
>
> 1.0.3 文档更新日期：2026-08-20\
> 新增提交后 Webhook 推送：`settings.webhookEnabled` / `settings.webhookUrl`（会员专享）；保存时校验地址并发送测试请求
>
> 1.0.4 接口更新日期：2026-08-20\
> 新增文件夹管理（目录树 / 创建 / 重命名 / 删除 / 移动）；创建与列表支持 `folderId`；新增移动表单 `/open/form/move`

:::

::: details 点击查看目录

[[toc]]

:::

## 文档说明
&nbsp;&nbsp;&nbsp;&nbsp;push表单是 pushplus 提供的表单收集能力。开放接口用于通过程序管理自己的表单（创建、设计、发布、停止、删除、按文件夹归档等）。鉴权方式与 [pushplus 开放接口](/doc/guide/openApi.md) 一致：先获取 AccessKey，再在请求头携带 `access-key`。

&nbsp;&nbsp;&nbsp;&nbsp;AccessKey 的申请、安全 IP、secretKey 配置与主站开放接口相同，请先阅读 [开放接口文档 - 获取AccessKey](/doc/guide/openApi.html#一-获取accesskey)。

&nbsp;&nbsp;&nbsp;&nbsp;推荐优先使用官方 [pushplus SDK](/doc/guide/sdk.md)，而不是自行编写 HTTP 请求代码。SDK 已封装 AccessKey 刷新、发送频率控制、回调等常见场景，可降低开发成本和出错概率。

&nbsp;&nbsp;&nbsp;&nbsp;表单开放接口的基础地址为：

```
https://www.pushplus.plus/push/api
```

填写页地址形如：`https://www.pushplus.plus/push/form/{formCode}`（接口返回的 `fillUrl` 字段）。

## 鉴权说明
调用本章节接口时，需在 HTTP Header 中携带：

| Header 名称 | 是否必填 | 说明 |
|---|---|---|
| access-key | 是 | 通过主站 `getAccessKey` 接口获取的令牌 |

也可兼容 Header / Cookie 中的 `pushToken`（浏览器登录态），但程序调用请统一使用 `access-key`。

获取 AccessKey 示例（与主站相同）：

- 请求地址：https://www.pushplus.plus/api/common/openApi/getAccessKey
- 请求方式：POST
- 请求参数：

```
{
  "token": "d90******c20",
  "secretKey": "qLc******gdk"
}
```

## 通用响应格式
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {}
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| code | 数字 | 业务状态码，200 表示成功 |
| msg | 字符串 | 提示信息 |
| data | 对象 | 业务数据；无业务数据时该字段可能不返回 |

## 表单状态说明

| status | 说明 |
|---|---|
| 0 | 草稿 |
| 1 | 收集中 |
| 2 | 已停止 |

## 文件夹说明
表单、文档、表格各自独立的文件夹空间，互不影响。`folderId` / `parentId` / `targetFolderId` 为空、不传或 `0` 表示根目录。

| 规则 | 说明 |
|---|---|
| 列表 `params.folderId` | 不传不过滤（返回全部）；`0` 为当前根目录下的表单；正整数为指定文件夹。有 `keyword` 时忽略该条件 |
| 响应 `folderId` | 所属文件夹 id；位于根目录时不返回该字段 |
| 嵌套 | 最多 5 层（根目录下第一层为 1） |
| 数量 | 表单工作区最多 200 个文件夹（不计入表单配额） |
| 同名 | 同一父目录下文件夹名称不可重复 |
| 删除文件夹 | 不会删除其中的表单；子文件夹与表单会上移到父目录（无父目录则回到根目录） |

## 题型 type 说明
保存表单设计时，`items` 中每道题通过 `type` 区分题型，常用取值如下：

| type | 说明 |
|---|---|
| input | 单行文本 |
| textarea | 多行文本 |
| radio | 单选题 |
| checkbox | 多选题 |
| select | 下拉选择 |
| imageRadio | 图片单选 |
| imageCheckbox | 图片多选 |
| fillBlank | 多项填空 |
| number | 数字 |
| date | 日期 |
| rate | 评分题 |
| scale | 量表题 |
| nps | NPS |
| sort | 排序题 |
| image | 图片上传 |
| location | 地理位置 |
| cascade | 多级联动 |
| matrixRadio | 矩阵单选 |
| matrixCheckbox | 矩阵多选 |
| matrixRate | 矩阵评分 |
| matrixScale | 矩阵量表 |
| matrixFill | 矩阵填空 |
| dynamicTable | 自增表格 |
| paragraph | 文本描述（不收集数据） |
| section | 分段说明（不收集数据） |
| pagebreak | 分页（不收集数据） |

## 一. 表单接口

### 1. 我的表单分页
分页查询当前用户的表单列表，支持按关键词、状态、文件夹筛选。列表接口不返回完整题目明细。

- 请求地址：https://www.pushplus.plus/push/api/open/form/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20,
  "params": {
    "keyword": "满意度",
    "status": 1,
    "folderId": 0
  }
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize | 否 | 20 | 每页大小，最大值为50
params.keyword | 否 | 无 | 按标题关键词搜索；传入时忽略 `folderId`，在全部表单中搜索
params.status | 否 | 无 | 表单状态：0草稿 / 1收集中 / 2已停止
params.folderId | 否 | 无 | 所属文件夹：不传不过滤；`0` 为根目录；正整数为指定文件夹

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 1,
    "pages": 1,
    "list": [
      {
        "id": 10001,
        "formCode": "a1b2c3d4",
        "fillUrl": "https://www.pushplus.plus/push/form/a1b2c3d4",
        "title": "用户满意度调查",
        "description": "请花1分钟完成填写",
        "status": 1,
        "responseCount": 12,
        "folderId": 1001,
        "publishTime": "2026-08-01 10:00:00",
        "createTime": "2026-07-28 09:00:00",
        "updateTime": "2026-08-01 10:00:00"
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 表单列表

- 表单列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 表单 id
formCode | 字符串 | 分享码；未发布时可能不返回
fillUrl | 字符串 | 填写链接；未发布时可能不返回
title | 字符串 | 标题
description | 字符串 | 描述
status | 数字 | 状态：0草稿 / 1收集中 / 2已停止
responseCount | 数字 | 答卷数
folderId | 数字 | 所属文件夹 id；位于根目录时不返回
publishTime | 日期 | 发布时间
createTime | 日期 | 创建时间
updateTime | 日期 | 更新时间

### 2. 创建表单
创建一个空白表单（草稿状态）。创建后可通过「保存表单设计」写入题目，再调用「发布表单」开放收集。

- 请求地址：https://www.pushplus.plus/push/api/open/form/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "title": "用户满意度调查",
  "folderId": 1001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
title | 是 | 无 | 表单标题，最长 100 字
folderId | 否 | 根目录 | 放入指定文件夹；空或 `0` 为根目录。文件夹须属于当前用户的表单工作区

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 10001,
    "title": "用户满意度调查",
    "status": 0,
    "responseCount": 0,
    "folderId": 1001,
    "createTime": "2026-08-06 12:00:00",
    "updateTime": "2026-08-06 12:00:00"
  }
}
```

> 说明：创建/复制返回草稿信息，不含题目明细；`formCode`、`fillUrl` 在首次发布后才会返回。复制后的新表单仍在源表单所在文件夹。

### 3. 复制表单
基于已有表单复制一份新表单（草稿），便于复用题目设计。

- 请求地址：https://www.pushplus.plus/push/api/open/form/copy?id=10001
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 源表单 id

- 响应内容：同「创建表单」，返回新表单信息。

### 4. 保存表单设计
保存表单标题、描述、题目列表、主题与收集设置。保存后仅更新草稿；若表单已发布，需再调用「发布表单」才会把最新题目同步到填写页。

- 请求地址：https://www.pushplus.plus/push/api/open/form/save
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 10001,
  "title": "用户满意度调查",
  "description": "请花1分钟完成填写",
  "items": [
    {
      "id": "q_name",
      "type": "input",
      "label": "您的姓名",
      "description": "",
      "required": true,
      "placeholder": "请输入姓名"
    },
    {
      "id": "q_score",
      "type": "radio",
      "label": "整体满意度",
      "required": true,
      "options": ["非常满意", "满意", "一般", "不满意"],
      "allowOther": false
    }
  ],
  "theme": {
    "primaryColor": "#1677ff",
    "backgroundColor": "#f5f5f5",
    "headerImage": "https://image.pushplus.plus/form/xxx.jpg",
    "backgroundImage": "",
    "cover": {
      "enabled": false,
      "image": "",
      "buttonText": "开始填写"
    }
  },
  "settings": {
    "endTime": "2026-12-31 23:59:59",
    "maxResponses": 1000,
    "oncePerUser": false,
    "allowAnonymous": false,
    "password": "",
    "showQuestionNumber": true,
    "onePerPage": false,
    "showPrevButton": true,
    "hideTitle": false,
    "hideCopyright": false,
    "hideAd": false,
    "showOutline": false,
    "thankText": "问卷到此结束，感谢您的参与！",
    "redirectEnabled": false,
    "redirectUrl": "",
    "webhookEnabled": false,
    "webhookUrl": "",
    "allowEdit": false
  }
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id
title | 是 | 无 | 表单标题，最长 100 字
description | 否 | 无 | 表单描述，最长 2000 字
items | 否 | 无 | 题目列表（JSON 数组），每题至少含 `id`、`type`、`label`
theme | 否 | 无 | 主题外观对象，字段见下表「theme 对象字段」
settings | 否 | 无 | 收集/展示设置对象，字段见下表「settings 对象字段」

#### theme 对象字段

参数名称 | 类型 | 默认值 | 说明
---|---|---|---
primaryColor | 字符串 | `#409eff` | 控件主色（按钮、选中态、进度条等），建议十六进制色值，如 `#1677ff`
backgroundColor | 字符串 | `#f5f7fa` | 填写页整体背景色
headerImage | 字符串 | 空 | 表单头图 URL；空字符串表示不展示头图
backgroundImage | 字符串 | 空 | 页面背景图 URL；空字符串表示不使用背景图
cover | 对象 | 无 | 封面页配置，见下表「cover 对象字段」

##### cover 对象字段

参数名称 | 类型 | 默认值 | 说明
---|---|---|---
enabled | 布尔 | false | 是否开启封面页；开启后填写前先展示封面（标题 + 描述 + 开始按钮）
image | 字符串 | 空 | 封面图 URL
buttonText | 字符串 | `开始填写` | 封面页开始按钮文案，最长 20 字

#### settings 对象字段

参数名称 | 类型 | 默认值 | 说明
---|---|---|---
endTime | 字符串 / null | null | 截止时间，格式 `yyyy-MM-dd HH:mm:ss`；`null` 或不传表示不限制。保存后立即对填写者生效
maxResponses | 数字 / null | null | 答卷总数上限，范围 1～1000000；`null` 或不传表示不限制。保存后立即生效
oncePerUser | 布尔 | false | 每人限填一次。开启匿名答卷时按浏览器指纹判断，否则按登录账号判断
allowAnonymous | 布尔 | false | 允许匿名答卷；为 `true` 时无需登录即可提交
password | 字符串 | 空 | 填写密码，最长 32 字；空字符串表示不需要密码。保存后立即生效
showQuestionNumber | 布尔 | true | 是否显示题目编号
onePerPage | 布尔 | false | 一页一题（每道题单独一页展示）
showPrevButton | 布尔 | true | 分页时是否显示「上一页」按钮
hideTitle | 布尔 | false | 隐藏标题与引导语
hideCopyright | 布尔 | false | 隐藏版权信息（**会员专享**；非会员保存时会被强制为 `false`）
hideAd | 布尔 | false | 去除广告（**会员专享**；非会员保存时会被强制为 `false`）
showOutline | 布尔 | false | 是否显示大纲
thankText | 字符串 | 空 | 提交后感谢语，最长 200 字；空则使用默认文案「问卷到此结束，感谢您的参与！」
redirectEnabled | 布尔 | false | 提交完成后是否跳转（**会员专享**；非会员保存时会被强制为 `false`）
redirectUrl | 字符串 | 空 | 跳转链接，最长 500 字；需同时开启 `redirectEnabled`
webhookEnabled | 布尔 | false | 提交后是否 Webhook 推送（**会员专享**；非会员保存时会被强制为 `false`）。详见 [提交后Webhook推送](/ecosystem/form-webhook.md)
webhookUrl | 字符串 | 空 | Webhook 地址，最长 500 字，须为 `http://` 或 `https://` 公网地址；需同时开启 `webhookEnabled`。新启用或变更地址时会先发送测试请求，对方须返回 `{"code": 200, "msg": "success"}`，否则保存失败
allowEdit | 布尔 | false | 允许填写者修改答卷（重新提交将覆盖原答卷）

> 说明：`theme`、`settings` 保存后即可影响填写页展示与收集规则；题目（`items`）若表单已发布，仍需再调用「发布表单」才会同步到填写页。

- 题目对象常用字段

参数名称 | 类型 | 说明
---|---|---
id | 字符串 | 题目唯一标识
type | 字符串 | 题型，见上文「题型 type 说明」
alias | 字符串 | 题目别名（选填），用于开放接口中稳定标识本题；未设置时以 `id` 为准
label | 字符串 | 题目标题
description | 字符串 | 题目说明
required | 布尔 | 是否必填
placeholder | 字符串 | 输入提示（文本类题型）
options | 数组 | 选项列表（单选/多选/下拉等）
rows / columns | 数组 | 矩阵类题目的行/列配置

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 5. 表单详情
获取表单完整信息，包含草稿题目、主题、设置，以及是否存在「未发布的题目改动」。

- 请求地址：https://www.pushplus.plus/push/api/open/form/detail?id=10001
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 10001,
    "formCode": "a1b2c3d4",
    "fillUrl": "https://www.pushplus.plus/push/form/a1b2c3d4",
    "title": "用户满意度调查",
    "description": "请花1分钟完成填写",
    "items": [],
    "theme": {
      "primaryColor": "#1677ff",
      "backgroundColor": "#f5f5f5",
      "headerImage": "",
      "backgroundImage": "",
      "cover": {
        "enabled": false,
        "image": "",
        "buttonText": "开始填写"
      }
    },
    "settings": {
      "endTime": null,
      "maxResponses": null,
      "oncePerUser": false,
      "allowAnonymous": false,
      "password": "",
      "showQuestionNumber": true,
      "onePerPage": false,
      "showPrevButton": true,
      "hideTitle": false,
      "hideCopyright": false,
      "hideAd": false,
      "showOutline": false,
      "thankText": "",
      "redirectEnabled": false,
      "redirectUrl": "",
      "webhookEnabled": false,
      "webhookUrl": "",
      "allowEdit": false
    },
    "status": 1,
    "publishDirty": true,
    "responseCount": 12,
    "folderId": 1001,
    "publishTime": "2026-08-01 10:00:00",
    "createTime": "2026-07-28 09:00:00",
    "updateTime": "2026-08-06 12:00:00"
  }
}
```
- 响应字段说明（相对列表接口的补充字段）

参数名称 | 类型 | 说明
---|---|---
items | 数组 | 草稿题目列表
theme | 对象 | 主题外观，字段同「保存表单设计」中的 theme 对象字段
settings | 对象 | 收集/展示设置，字段同「保存表单设计」中的 settings 对象字段
publishDirty | 布尔 | 草稿题目与发布快照不一致（有未发布改动）时为 true
folderId | 数字 | 所属文件夹 id；位于根目录时不返回

### 6. 草稿与发布快照差异
在更新发布前，对比草稿题目与当前发布快照，判断改动是否会影响已有答卷统计（删题、改题型、改选项等）。建议在已有答卷的表单上，发布前先调用本接口做提示。

- 请求地址：https://www.pushplus.plus/push/api/open/form/publishDiff?id=10001
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "dirty": true,
    "breaking": true,
    "responseCount": 12,
    "added": ["您的建议"],
    "removed": ["旧题目A"],
    "typeChanged": ["整体满意度"],
    "optionChanged": ["您从哪里了解到我们"]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
dirty | 布尔 | 草稿与发布快照是否不一致
breaking | 布尔 | 是否存在会影响历史答卷统计的破坏性变更
responseCount | 数字 | 已有答卷数
added | 数组 | 新增题目标题列表
removed | 数组 | 删除题目标题列表
typeChanged | 数组 | 题型变更的题目标题列表
optionChanged | 数组 | 选项/行列变更的题目标题列表

### 7. 发布表单
将当前草稿题目发布为正式收集版本。草稿状态会变为「收集中」；若表单此前已停止，发布后会重新开放收集。

- 请求地址：https://www.pushplus.plus/push/api/open/form/publish?id=10001
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 10001,
    "formCode": "a1b2c3d4",
    "fillUrl": "https://www.pushplus.plus/push/form/a1b2c3d4",
    "title": "用户满意度调查",
    "status": 1,
    "previousStatus": 2,
    "publishDirty": false,
    "publishTime": "2026-08-06 12:30:00"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 表单 id
formCode | 字符串 | 分享码；首次发布时生成
fillUrl | 字符串 | 填写链接
title | 字符串 | 标题
previousStatus | 数字 | 发布前的状态（用于提示「已停止」的表单被重新开放）
status | 数字 | 发布后状态，一般为 1（收集中）
publishDirty | 布尔 | 发布后为 false
publishTime | 日期 | 发布时间

### 8. 停止收集
停止表单收集。停止后填写页不可再提交，已有答卷保留。

- 请求地址：https://www.pushplus.plus/push/api/open/form/stop?id=10001
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 9. 删除表单
删除指定表单。删除后不可恢复，请谨慎调用。

- 请求地址：https://www.pushplus.plus/push/api/open/form/delete?id=10001
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 10. 移动表单到文件夹
将表单移动到指定文件夹。`targetFolderId` 为空或 `0` 时移回根目录。

- 请求地址：https://www.pushplus.plus/push/api/open/form/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 10001,
  "targetFolderId": 1001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 表单 id
targetFolderId | 否 | 根目录 | 目标文件夹 id；空或 `0` 为根目录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 11. 推送表单
表单开放接口不单独提供推送接口。发布后可通过 [发送消息接口](/doc/guide/api.md) 推送填写页，`template` 传 `form`，`pushId` 传 `formCode`。

- 请求地址：https://www.pushplus.plus/send
- 请求方式：POST
- Content-Type: application/json
- 请求参数:
```
{
  "token": "d90******c20",
  "title": "用户满意度调查",
  "content": "请花1分钟完成填写",
  "template": "form",
  "pushId": "a1b2c3d4",
  "channel": "wechat"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
token | 是 | 无 | 用户token或消息token
title | 否 | 无 | 消息标题
content | 是 | 无 | 消息内容
template | 是 | html | 固定传 `form`
pushId | 是 | 无 | 表单编码 `formCode`（发布后才有）
channel | 否 | wechat | 发送渠道
topic | 否 | 无 | 群组编码，不填仅发送给自己
to | 否 | 无 | 好友令牌，多人用逗号隔开

> 说明：需先发布表单并拿到 `formCode`，才能推送。完整参数见 [发送消息接口](/doc/guide/api.md)。

### 12. 提交后 Webhook 推送
填写者提交答卷后，可将答卷 POST 到你配置的地址（**会员专享**）。配置方式、测试请求、正式推送字段与接收方响应格式见 [提交后Webhook推送说明](/doc/ecosystem/form-webhook.md)。

保存 `settings` 时：

- 开启 `webhookEnabled` 必须同时填写合法的 `webhookUrl`
- 新启用或变更地址时，服务端会先向该地址发送测试 POST；未返回 `{"code": 200, "msg": "success"}` 则保存失败，该地址不会用于后续推送
- `settings` 保存后立即生效，无需再发布

## 二. 文件夹接口
表单工作区的文件夹管理。路径前缀为 `/open/form/folder`。规则见上文「文件夹说明」。查询只需调用目录树：当前层子文件夹按 `parentId` 过滤即可，不必再提供列表或面包屑接口。

### 1. 文件夹目录树
返回当前用户表单工作区的完整目录树。根目录下的文件夹作为数组第一层，子文件夹在 `children` 中。

- 请求地址：https://www.pushplus.plus/push/api/open/form/folder/tree
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数：无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": [
    {
      "id": 1001,
      "name": "调研问卷",
      "createTime": "2026-08-20 10:00:00",
      "updateTime": "2026-08-20 10:00:00",
      "children": [
        {
          "id": 1002,
          "parentId": 1001,
          "name": "客户调研",
          "createTime": "2026-08-20 11:00:00",
          "updateTime": "2026-08-20 11:00:00"
        }
      ]
    },
    {
      "id": 1003,
      "name": "活动报名",
      "createTime": "2026-08-20 12:00:00",
      "updateTime": "2026-08-20 12:00:00"
    }
  ]
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|---|---
id | 数字 | 文件夹 id
parentId | 数字 | 父文件夹 id；位于根目录时不返回
name | 字符串 | 文件夹名称
createTime | 日期 | 创建时间
updateTime | 日期 | 更新时间
children | 数组 | 子文件夹；无子文件夹时不返回

### 2. 创建文件夹
在指定父目录下创建文件夹。名称最长 100 字。

- 请求地址：https://www.pushplus.plus/push/api/open/form/folder/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "parentId": 0,
  "name": "调研问卷"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
name | 是 | 无 | 文件夹名称，最长 100 字
parentId | 否 | 根目录 | 父文件夹 id；空或 `0` 为根目录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 1001,
    "name": "调研问卷",
    "createTime": "2026-08-20 10:00:00",
    "updateTime": "2026-08-20 10:00:00"
  }
}
```

### 3. 重命名文件夹

- 请求地址：https://www.pushplus.plus/push/api/open/form/folder/rename
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1001,
  "name": "客户调研"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 文件夹 id
name | 是 | 无 | 新名称，最长 100 字

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 4. 删除文件夹
删除指定文件夹。其中的子文件夹与表单会上移到父目录，不会被一并删除。

- 请求地址：https://www.pushplus.plus/push/api/open/form/folder/delete?id=1001
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 文件夹 id

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 5. 移动文件夹
将文件夹移动到另一个父目录。不能移动到自身或自己的子文件夹中；移动后总深度不可超过 5 层。

- 请求地址：https://www.pushplus.plus/push/api/open/form/folder/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1001,
  "targetFolderId": 0
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 文件夹 id
targetFolderId | 否 | 根目录 | 目标父文件夹 id；空或 `0` 为根目录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

## 典型调用流程

```
1. getAccessKey
2. POST /open/form/create（创建草稿，拿到 id；此时尚无 formCode / fillUrl）
3. POST /open/form/save（写入题目与设置）
4. GET /open/form/publishDiff（可选，检查差异）
5. POST /open/form/publish（发布并开始收集，此时才会生成 formCode / fillUrl）
6. 将 fillUrl 分享给填写者，或通过 /send 推送（template=form, pushId=formCode）
7. 需要时调用 stop 停止，或 delete 删除
```
