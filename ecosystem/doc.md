# push文档开放接口文档 V1.0.5

::: details 点击展开版本更新日志

> 1.0 接口更新日期：2026-08-11\
> 首次发布：文档列表、创建、内容读写、发布、重命名、删除、分享设置
>
> 1.0.1 文档更新日期：2026-08-13\
> 开放接口路径 `/open/document` 调整为 `/open/doc`
>
> 1.0.2 接口更新日期：2026-08-17\
> 新增导入 Word（`.docx`）创建文档接口 `/open/doc/import`
>
> 1.0.3 接口更新日期：2026-08-18\
> 新增推送文档接口 `/open/doc/send`；文档体例与主站开放接口对齐；分页默认 `pageSize` 调整为 20，响应补充 `pages`
>
> 1.0.4 接口更新日期：2026-08-18\
> 去掉独立推送接口 `/open/doc/send`；发布后通过主站 [发送消息接口](/doc/guide/api.md) 推送，`template` 传 `doc`，`pushId` 传 `docCode`
>
> 1.0.5 接口更新日期：2026-08-20\
> 新增文件夹管理（目录树 / 创建 / 重命名 / 删除 / 移动）；创建、导入与列表支持 `folderId`；新增移动文档 `/open/doc/move`

:::

::: details 点击查看目录

[[toc]]

:::

## 文档说明
&nbsp;&nbsp;&nbsp;&nbsp;push文档是 pushplus 提供的在线文档能力，基于 Tiptap 富文本。开放接口用于通过程序管理自己的文档（创建、写入内容、发布、分享、按文件夹归档等）。鉴权方式与 [pushplus 开放接口](/doc/guide/openApi.md) 一致：先获取 AccessKey，再在请求头携带 `access-key`。

&nbsp;&nbsp;&nbsp;&nbsp;AccessKey 的申请、安全 IP、secretKey 配置与主站开放接口相同，请先阅读 [开放接口文档 - 获取AccessKey](/doc/guide/openApi.html#一-获取accesskey)。

&nbsp;&nbsp;&nbsp;&nbsp;推荐优先使用官方 [pushplus SDK](/doc/guide/sdk.md)，而不是自行编写 HTTP 请求代码。SDK 已封装 AccessKey 刷新、发送频率控制、回调等常见场景，可降低开发成本和出错概率。

&nbsp;&nbsp;&nbsp;&nbsp;文档开放接口的基础地址为：

```
https://www.pushplus.plus/push/api
```

分享页地址形如：`https://www.pushplus.plus/push/doc/{docCode}`（接口返回的 `shareUrl` 字段）。

&nbsp;&nbsp;&nbsp;&nbsp;可通过 `create` 创建空白文档，或通过 `import` 上传 Word（`.docx`）生成文档。再经 `content` / `saveContent` / `publish` 完成「写内容 → 发布到分享页」。需要推送给自己、群组或好友时，调用主站 [发送消息接口](/doc/guide/api.md)，`template` 传 `doc`，`pushId` 传 `docCode`。

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

## 类型与状态说明

### sharePerm / shareLogin

| 字段 | 取值 | 说明 |
|---|---|---|
| sharePerm | 0 | 关闭分享 |
| sharePerm | 1 | 开启分享（仅可查看） |
| shareLogin | 0 | 免登录可打开分享页 |
| shareLogin | 1 | 需登录后打开分享页 |

### perm

| 字段 | 取值 | 说明 |
|---|---|---|
| perm | 1 | 当前用户可查看 |
| perm | 2 | 当前用户可编辑 |

开放接口查询的是「我的文档」，因此列表与管理类接口返回的 `perm` 一般为 `2`。

### 草稿与发布
文档采用「草稿 / 发布快照」模型：

1. `saveContent` 只写入草稿，不影响已对外分享的内容
2. `publish` 将草稿同步为分享页快照
3. 开启分享且从未发布过时，系统会自动用当前草稿生成首版快照

| 字段 | 类型 | 说明 |
|---|---|---|
| published | 布尔 | 是否已发布过；`true` 表示分享页已有发布快照 |
| publishDirty | 布尔 | 草稿与发布快照是否不一致；保存草稿后未重新发布时为 `true` |
| publishTime | 字符串 | 最近发布时间；从未发布过时不返回该字段 |

## 文件夹说明
文档、表单、表格各自独立的文件夹空间，互不影响。`folderId` / `parentId` / `targetFolderId` 为空、不传或 `0` 表示根目录。

| 规则 | 说明 |
|---|---|
| 列表 `params.folderId` | 不传不过滤（返回全部）；`0` 为当前根目录下的文档；正整数为指定文件夹。有 `keyword` 时忽略该条件 |
| 响应 `folderId` | 所属文件夹 id；位于根目录时不返回该字段 |
| 嵌套 | 最多 5 层（根目录下第一层为 1） |
| 数量 | 文档工作区最多 200 个文件夹 |
| 同名 | 同一父目录下文件夹名称不可重复 |
| 删除文件夹 | 不会删除其中的文档；子文件夹与文档会上移到父目录（无父目录则回到根目录） |

## 一. 文档接口

### 1. 我的文档分页
分页查询当前用户的文档列表，支持按关键词、是否已开启分享、文件夹筛选。列表不返回正文内容。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20,
  "params": {
    "keyword": "工作同步",
    "shareEnabled": true,
    "folderId": 0
  }
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize | 否 | 20 | 每页大小，最大值为50
params.keyword | 否 | 无 | 按标题关键词搜索；传入时忽略 `folderId`，在全部文档中搜索
params.shareEnabled | 否 | 无 | `true` 时仅返回已开启分享的文档；不传则全部
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
        "docCode": "Ab3xY7kP",
        "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
        "title": "本周工作同步",
        "sharePerm": 1,
        "shareLogin": 1,
        "perm": 2,
        "published": true,
        "folderId": 2001,
        "publishTime": "2026-08-11 10:00:00",
        "createTime": "2026-08-10 09:00:00",
        "updateTime": "2026-08-11 10:00:00"
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
list | 数组 | 文档列表

- 文档列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 文档分享码
shareUrl | 字符串 | 分享链接
title | 字符串 | 标题
sharePerm | 数字 | 分享权限：0关闭 / 1开启（仅可查看）
shareLogin | 数字 | 分享是否需登录：0免登录 / 1需登录
perm | 数字 | 当前用户权限：1可查看 / 2可编辑
published | 布尔 | 是否已发布过
folderId | 数字 | 所属文件夹 id；位于根目录时不返回
publishTime | 日期 | 最近发布时间；从未发布过时不返回
createTime | 日期 | 创建时间
updateTime | 日期 | 更新时间

### 2. 创建文档
创建空白文档。创建后默认关闭分享；可通过「保存内容」「发布」写入并对外同步。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "title": "本周工作同步",
  "folderId": 2001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
title | 是 | 无 | 标题，最长 100 字
folderId | 否 | 根目录 | 放入指定文件夹；空或 `0` 为根目录。文件夹须属于当前用户的文档工作区

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 0,
    "shareLogin": 1,
    "perm": 2,
    "published": false,
    "publishDirty": false,
    "folderId": 2001,
    "createTime": "2026-08-11 12:00:00",
    "updateTime": "2026-08-11 12:00:00"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 文档分享码
shareUrl | 字符串 | 分享链接
title | 字符串 | 标题
sharePerm | 数字 | 分享权限：0关闭 / 1开启（仅可查看）；新建默认为 0
shareLogin | 数字 | 分享是否需登录：0免登录 / 1需登录；新建默认为 1
perm | 数字 | 当前用户权限：1可查看 / 2可编辑
published | 布尔 | 是否已发布过；新建为 `false`
publishDirty | 布尔 | 草稿与发布快照是否不一致；新建为 `false`
folderId | 数字 | 所属文件夹 id；位于根目录时不返回
publishTime | 日期 | 最近发布时间；从未发布过时不返回
createTime | 日期 | 创建时间
updateTime | 日期 | 更新时间

### 3. 导入 Word 创建文档
上传 Word 文件（`.docx`）创建文档。标题默认取文件名（去掉扩展名，最长 100 字）；正文转为 HTML 草稿。创建后默认关闭分享，需再调用「发布文档」才会同步到分享页。

说明：

1. 仅支持 `.docx`。旧版 `.doc` 请先用 Word 另存为 `.docx`
2. 文件大小不超过 2MB；转换后的 HTML（含内嵌图片）也不超过约 2MB
3. 会尽量保留标题、段落、列表、加粗/斜体、链接、表格和图片；页眉页脚、文本框等复杂排版不会完全还原
4. 图片以内嵌方式写入草稿。图片过多导致超限时，请先减少图片再导入

- 请求地址：https://www.pushplus.plus/push/api/open/doc/import
- 请求方式：POST
- Content-Type: multipart/form-data
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数（form-data）

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
file | 是 | 无 | Word 文件，仅支持 `.docx`，不超过 2MB
folderId | 否 | 根目录 | 放入指定文件夹；空或 `0` 为根目录

- 调用示例（curl）
```
curl -X POST "https://www.pushplus.plus/push/api/open/doc/import" \
  -H "access-key: d7b******62f" \
  -F "file=@/path/to/本周工作同步.docx" \
  -F "folderId=2001"
```
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 0,
    "shareLogin": 1,
    "perm": 2,
    "published": false,
    "publishDirty": false,
    "folderId": 2001,
    "createTime": "2026-08-17 12:00:00",
    "updateTime": "2026-08-17 12:00:00"
  }
}
```
- 响应字段说明：同「创建文档」；`title` 默认取 Word 文件名。

### 4. 获取文档内容
按分享码获取当前用户自己的文档元信息与草稿正文（HTML）。仅能读取自己创建的文档。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/content?docCode=Ab3xY7kP
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": true,
    "publishTime": "2026-08-11 10:00:00",
    "createTime": "2026-08-10 09:00:00",
    "updateTime": "2026-08-11 12:30:00",
    "content": "<h1>本周工作同步</h1><p>需求评审与排期确认。</p>"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 文档分享码
shareUrl | 字符串 | 分享链接
title | 字符串 | 标题
sharePerm | 数字 | 分享权限：0关闭 / 1开启（仅可查看）
shareLogin | 数字 | 分享是否需登录：0免登录 / 1需登录
perm | 数字 | 当前用户权限：1可查看 / 2可编辑
published | 布尔 | 是否已发布过
publishDirty | 布尔 | 草稿与发布快照是否不一致
publishTime | 日期 | 最近发布时间；从未发布过时不返回
createTime | 日期 | 创建时间
updateTime | 日期 | 更新时间
content | 字符串 | HTML 草稿正文

### 5. 保存文档内容
保存文档草稿 HTML。保存后不影响分享页，需再调用「发布文档」才会同步对外内容。仅所有者可保存。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/saveContent
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Ab3xY7kP",
  "content": "<h1>本周工作同步</h1><ul><li>需求评审与排期确认</li><li>两个新功能已上线</li></ul>"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码
content | 是 | 无 | HTML 内容；允许空文档（后端归一化为空段落），最长约 2MB

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": true,
    "publishTime": "2026-08-11 10:00:00",
    "createTime": "2026-08-10 09:00:00",
    "updateTime": "2026-08-11 12:30:00"
  }
}
```
- 响应字段说明：同「创建文档」；已发布过再保存草稿后，`publishDirty` 一般为 `true`。

### 6. 发布文档
将草稿同步为分享页快照。发布成功后 `published` 为 `true`，`publishDirty` 为 `false`，并写入 `publishTime`。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/publish?docCode=Ab3xY7kP
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": false,
    "publishTime": "2026-08-11 12:35:00",
    "createTime": "2026-08-10 09:00:00",
    "updateTime": "2026-08-11 12:35:00"
  }
}
```
- 响应字段说明：同「创建文档」；发布后 `published` 为 `true`，`publishDirty` 为 `false`。

### 7. 重命名
修改文档标题，仅所有者可操作。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/rename
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Ab3xY7kP",
  "title": "本周工作同步（已更新）"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码
title | 是 | 无 | 新标题，最长 100 字

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 8. 删除文档
删除文档（逻辑删除），仅所有者可操作。删除后分享链接不可访问。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/delete?docCode=Ab3xY7kP
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 9. 移动文档到文件夹
将文档移动到指定文件夹。`targetFolderId` 为空或 `0` 时移回根目录。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Ab3xY7kP",
  "targetFolderId": 2001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码
targetFolderId | 否 | 根目录 | 目标文件夹 id；空或 `0` 为根目录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 10. 更新分享设置
开启或关闭文档分享，并可设置打开分享页是否需要登录。仅支持「关闭 / 开启仅查看」，不再提供可编辑分享。

开启分享且从未发布过时，会自动用当前草稿生成首版快照。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/updateShare
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Ab3xY7kP",
  "sharePerm": 1,
  "shareLogin": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 文档分享码
sharePerm | 是 | 无 | 0关闭 / 1开启（仅可查看）
shareLogin | 否 | 沿用原值 | 0免登录 / 1需登录；开启分享时缺省为需登录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Ab3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/doc/Ab3xY7kP",
    "title": "本周工作同步",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": false,
    "publishTime": "2026-08-11 12:35:00",
    "createTime": "2026-08-10 09:00:00",
    "updateTime": "2026-08-11 12:40:00"
  }
}
```
- 响应字段说明：同「创建文档」。

### 11. 推送文档
文档开放接口不单独提供推送接口。发布后可通过 [发送消息接口](/doc/guide/api.md) 推送分享页，`template` 传 `doc`，`pushId` 传 `docCode`。

- 请求地址：https://www.pushplus.plus/send
- 请求方式：POST
- Content-Type: application/json
- 请求参数:
```
{
  "token": "d90******c20",
  "title": "本周工作同步",
  "content": "请查收",
  "template": "doc",
  "pushId": "Ab3xY7kP",
  "channel": "wechat"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
token | 是 | 无 | 用户token或消息token
title | 否 | 无 | 消息标题
content | 是 | 无 | 消息内容
template | 是 | html | 固定传 `doc`
pushId | 是 | 无 | 文档编码 `docCode`
channel | 否 | wechat | 发送渠道
topic | 否 | 无 | 群组编码，不填仅发送给自己
to | 否 | 无 | 好友令牌，多人用逗号隔开

> 说明：完整参数见 [发送消息接口](/doc/guide/api.md)。

## 二. 文件夹接口
文档工作区的文件夹管理。路径前缀为 `/open/doc/folder`。规则见上文「文件夹说明」。查询只需调用目录树：当前层子文件夹按 `parentId` 过滤即可，不必再提供列表或面包屑接口。

### 1. 文件夹目录树
返回当前用户文档工作区的完整目录树。根目录下的文件夹作为数组第一层，子文件夹在 `children` 中。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/folder/tree
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
      "id": 2001,
      "name": "周报",
      "createTime": "2026-08-20 10:00:00",
      "updateTime": "2026-08-20 10:00:00",
      "children": [
        {
          "id": 2002,
          "parentId": 2001,
          "name": "本周周报",
          "createTime": "2026-08-20 11:00:00",
          "updateTime": "2026-08-20 11:00:00"
        }
      ]
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

- 请求地址：https://www.pushplus.plus/push/api/open/doc/folder/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "parentId": 0,
  "name": "周报"
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
    "id": 2001,
    "name": "周报",
    "createTime": "2026-08-20 10:00:00",
    "updateTime": "2026-08-20 10:00:00"
  }
}
```

### 3. 重命名文件夹

- 请求地址：https://www.pushplus.plus/push/api/open/doc/folder/rename
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 2001,
  "name": "本周周报"
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
删除指定文件夹。其中的子文件夹与文档会上移到父目录，不会被一并删除。

- 请求地址：https://www.pushplus.plus/push/api/open/doc/folder/delete?id=2001
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

- 请求地址：https://www.pushplus.plus/push/api/open/doc/folder/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 2001,
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
2. create（创建空白文档）或 import（上传 Word 生成文档）
3. saveContent（按需改写 HTML 草稿；import 已写入正文时可跳过）
4. updateShare（开启分享，可选）
5. publish（同步到分享页）
6. 将 shareUrl 分享给阅读者，或通过 /send 推送（template=doc, pushId=docCode）
```
