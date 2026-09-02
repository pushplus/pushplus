# push表格开放接口文档 V1.0.5

::: details 点击展开版本更新日志

> 1.0 接口更新日期：2026-08-13\
> 首次发布：表格列表、创建、内容读写、按区域写入单元格、发布、重命名、删除、分享设置\
> 说明：保存仅写草稿，需 `publish` 后分享页才同步；开放响应使用表格专用 VO
>
> 1.0.1 文档更新日期：2026-08-13\
> 补充获取/保存内容接口中 `content` JSON 各字段说明\
> 开放接口路径 `/open/sheet` 调整为 `/open/excel`；分享页地址调整为 `/push/excel/{docCode}`
>
> 1.0.2 接口更新日期：2026-08-17\
> 新增导入 Excel（`.xlsx` / `.xls`）创建表格接口 `/open/excel/import`
>
> 1.0.3 接口更新日期：2026-08-18\
> 新增推送表格接口 `/open/excel/send`；文档体例与主站开放接口对齐；分页默认 `pageSize` 调整为 20，响应补充 `pages`
>
> 1.0.4 接口更新日期：2026-08-18\
> 去掉独立推送接口 `/open/excel/send`；发布后通过主站 [发送消息接口](/doc/guide/api.md) 推送，`template` 传 `excel`，`pushId` 传 `docCode`
>
> 1.0.5 接口更新日期：2026-08-20\
> 新增文件夹管理（目录树 / 创建 / 重命名 / 删除 / 移动）；创建、导入与列表支持 `folderId`；新增移动表格 `/open/excel/move`

:::

::: details 点击查看目录

[[toc]]

:::

## 文档说明
&nbsp;&nbsp;&nbsp;&nbsp;push表格是 pushplus 提供的在线表格能力。开放接口用于通过程序管理自己的表格（创建、写入内容、按区域写单元格、发布、分享、按文件夹归档等）。鉴权方式与 [pushplus 开放接口](/doc/guide/openApi.md) 一致：先获取 AccessKey，再在请求头携带 `access-key`。

&nbsp;&nbsp;&nbsp;&nbsp;AccessKey 的申请、安全 IP、secretKey 配置与主站开放接口相同，请先阅读 [开放接口文档 - 获取AccessKey](/doc/guide/openApi.html#一-获取accesskey)。

&nbsp;&nbsp;&nbsp;&nbsp;推荐优先使用官方 [pushplus SDK](/doc/guide/sdk.md)，而不是自行编写 HTTP 请求代码。SDK 已封装 AccessKey 刷新、发送频率控制、回调等常见场景，可降低开发成本和出错概率。

&nbsp;&nbsp;&nbsp;&nbsp;表格开放接口的基础地址为：

```
https://www.pushplus.plus/push/api
```

分享页地址形如：`https://www.pushplus.plus/push/excel/{docCode}`（接口返回的 `shareUrl` 字段）。

&nbsp;&nbsp;&nbsp;&nbsp;可通过 `create` 创建空白表格，或通过 `import` 上传 Excel 生成表格。再经 `saveContent` / `writeCells` / `publish` 完成「写草稿 → 发布到分享页」。需要推送给自己、群组或好友时，调用主站 [发送消息接口](/doc/guide/api.md)，`template` 传 `excel`，`pushId` 传 `docCode`。

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

开放接口查询的是「我的表格」，因此列表与管理类接口返回的 `perm` 一般为 `2`。

### 草稿与发布
表格与文档一致，采用「草稿 / 发布快照」模型：

1. `saveContent` / `writeCells` 只写入草稿，不影响已对外分享的内容
2. `publish` 将草稿同步为分享页快照
3. 开启分享且从未发布过时，系统会自动用当前草稿生成首版快照

| 字段 | 类型 | 说明 |
|---|---|---|
| published | 布尔 | 是否已发布过；`true` 表示分享页已有发布快照 |
| publishDirty | 布尔 | 草稿与发布快照是否不一致；保存草稿后未重新发布时为 `true` |
| publishTime | 字符串 | 最近发布时间；从未发布过时不返回该字段 |

### 表格内容格式
获取、保存接口中的 `content` 是 **JSON 字符串**（整表快照），须以 `{` 开头，最长约 2MB。解析后是一本工作簿：包含工作表顺序、各工作表单元格数据。只改局部单元格时，可改用 `writeCells`，不必每次提交整表。

空表可为 `{}`。行号、列号均为 **从 0 开始**：`"0"` 行 `"0"` 列对应 A1，`"1"` 行 `"0"` 列对应 A2，`"0"` 行 `"1"` 列对应 B1。

解析后的常用结构如下（保存时按此对象序列化为字符串再传入 `content`）：

```
{
  "id": "workbook-1",
  "name": "销售日报",
  "sheetOrder": ["sheet-1"],
  "styles": {
    "header": {
      "fs": 11,
      "bl": 1,
      "bg": { "rgb": "#E8F1FF" },
      "cl": { "rgb": "#1558D6" },
      "ht": 2,
      "vt": 2
    }
  },
  "sheets": {
    "sheet-1": {
      "id": "sheet-1",
      "name": "Sheet1",
      "rowCount": 1000,
      "columnCount": 20,
      "defaultColumnWidth": 88,
      "defaultRowHeight": 24,
      "freeze": {
        "xSplit": 0,
        "ySplit": 1,
        "startRow": 1,
        "startColumn": 0
      },
      "columnData": {
        "0": { "w": 120 },
        "1": { "w": 100 }
      },
      "cellData": {
        "0": {
          "0": { "v": "日期", "t": 1, "s": "header" },
          "1": { "v": "销售额", "t": 1, "s": "header" }
        },
        "1": {
          "0": { "v": "2026-08-13", "t": 1 },
          "1": { "v": 12800, "t": 2 }
        },
        "2": {
          "0": { "v": "合计", "t": 1 },
          "1": { "f": "=SUM(B2:B10)" }
        }
      }
    }
  }
}
```

#### 工作簿根对象

参数名称 | 类型 | 是否必填 | 说明
---|---|---|---
id | 字符串 | 否 | 工作簿 ID。新建或自行构造时可自定义，读取时原样返回
name | 字符串 | 否 | 工作簿名称，一般与表格标题一致
sheetOrder | 数组 | 是（有多表时） | 工作表 ID 的显示顺序，如 `["sheet-1","sheet-2"]`。标签栏按此顺序排列
sheets | 对象 | 是 | 工作表集合。key 为工作表 ID，value 为该工作表对象，见下表
styles | 对象 | 否 | 命名样式表。key 为样式名（如 `header`），单元格通过 `s` 引用。不设样式时可省略

#### sheets.{sheetId} 工作表对象

参数名称 | 类型 | 是否必填 | 说明
---|---|---|---
id | 字符串 | 是 | 工作表 ID，须与 `sheets` 的 key、以及 `sheetOrder` 中的值一致
name | 字符串 | 是 | 工作表标签名，如 `Sheet1`。`writeCells` 的 `sheetName` 按此匹配
rowCount | 数字 | 否 | 行数，默认约 1000。写入超出范围的单元格时会自动扩大
columnCount | 数字 | 否 | 列数，默认约 20。同上，不足时会自动扩大
defaultColumnWidth | 数字 | 否 | 默认列宽（像素）
defaultRowHeight | 数字 | 否 | 默认行高（像素）
freeze | 对象 | 否 | 冻结窗格。`ySplit` 为冻结行数，`xSplit` 为冻结列数；`startRow` / `startColumn` 为冻结后滚动起点（从 0 计）
columnData | 对象 | 否 | 列配置。key 为列序号（从 0 计，`"0"` 即 A 列）。`w` 为列宽（像素），`hd` 为是否隐藏（`1` 隐藏 / `0` 显示）
rowData | 对象 | 否 | 行配置。key 为行序号（从 0 计）。`h` 为行高（像素），`hd` 为是否隐藏
cellData | 对象 | 否 | 单元格数据。key 为行序号，内层 key 为列序号，value 为单元格对象，见下表
mergeData | 数组 | 否 | 合并单元格区域列表。项如 `{ "startRow": 0, "startColumn": 0, "endRow": 0, "endColumn": 2 }` 表示合并 A1:C1

#### cellData.{row}.{col} 单元格对象

参数名称 | 类型 | 是否必填 | 说明
---|---|---|---
v | 字符串 / 数字 / 布尔 | 否 | 单元格显示值。文本用字符串，数字用数值（便于公式计算）。仅有公式、无固定值时可省略
t | 数字 | 否 | 值类型：`1` 文本、`2` 数字、`3` 布尔、`4` 强制按文本。不传时由 `v` 的实际类型推断
f | 字符串 | 否 | 公式，须以 `=` 开头，如 `=SUM(B2:B10)`、`=A2+A3`。有公式时表格会按公式计算结果写入显示值
s | 字符串 / 对象 | 否 | 单元格样式。字符串时引用根对象 `styles` 中的样式名；也可直接写样式对象（字段同下表）

只写值时，最小单元格为 `{ "v": "日期" }` 或 `{ "v": 12800 }`。`writeCells` 写入的单元格即为这种只含 `v` 的形式。

#### styles.{styleName} / 单元格 s 样式对象

参数名称 | 类型 | 说明
---|---|---
ff | 字符串 | 字体，如 `Arial`、`微软雅黑`
fs | 数字 | 字号，如 `11`
bl | 数字 | 是否加粗：`1` 是 / `0` 否
it | 数字 | 是否斜体：`1` 是 / `0` 否
cl | 对象 | 文字颜色，如 `{ "rgb": "#1558D6" }`
bg | 对象 | 背景色，如 `{ "rgb": "#E8F1FF" }`
ht | 数字 | 水平对齐：`1` 左对齐、`2` 居中、`3` 右对齐
vt | 数字 | 垂直对齐：`1` 顶端、`2` 居中、`3` 底端
n | 对象 / 字符串 | 数字格式。常用如日期 `yyyy-mm-dd`、金额 `0.00`

读取接口返回的 `content` 可能还包含缩放、滚动位置、插件资源等附加字段，保存时可原样回传，自行构造时不必填写。

## 文件夹说明
表格、表单、文档各自独立的文件夹空间，互不影响。`folderId` / `parentId` / `targetFolderId` 为空、不传或 `0` 表示根目录。

| 规则 | 说明 |
|---|---|
| 列表 `params.folderId` | 不传不过滤（返回全部）；`0` 为当前根目录下的表格；正整数为指定文件夹。有 `keyword` 时忽略该条件 |
| 响应 `folderId` | 所属文件夹 id；位于根目录时不返回该字段 |
| 嵌套 | 最多 5 层（根目录下第一层为 1） |
| 数量 | 表格工作区最多 200 个文件夹 |
| 同名 | 同一父目录下文件夹名称不可重复 |
| 删除文件夹 | 不会删除其中的表格；子文件夹与表格会上移到父目录（无父目录则回到根目录） |

## 一. 表格接口

### 1. 我的表格分页
分页查询当前用户的表格列表，支持按关键词、是否已开启分享、文件夹筛选。列表不返回正文内容。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20,
  "params": {
    "keyword": "销售日报",
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
params.keyword | 否 | 无 | 按标题关键词搜索；传入时忽略 `folderId`，在全部表格中搜索
params.shareEnabled | 否 | 无 | `true` 时仅返回已开启分享的表格；不传则全部
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
        "docCode": "Sh3xY7kP",
        "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
        "title": "销售日报",
        "sharePerm": 1,
        "shareLogin": 1,
        "perm": 2,
        "published": true,
        "folderId": 3001,
        "publishTime": "2026-08-13 10:00:00",
        "createTime": "2026-08-12 09:00:00",
        "updateTime": "2026-08-13 10:00:00"
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
list | 数组 | 表格列表

- 表格列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 表格分享码
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

### 2. 创建表格
创建空白表格。创建后默认关闭分享；可通过「保存内容 / 写入单元格」「发布」写入并对外同步。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "title": "销售日报",
  "folderId": 3001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
title | 是 | 无 | 标题，最长 100 字
folderId | 否 | 根目录 | 放入指定文件夹；空或 `0` 为根目录。文件夹须属于当前用户的表格工作区

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 0,
    "shareLogin": 1,
    "perm": 2,
    "published": false,
    "publishDirty": false,
    "folderId": 3001,
    "createTime": "2026-08-13 12:00:00",
    "updateTime": "2026-08-13 12:00:00"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 表格分享码
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

### 3. 导入 Excel 创建表格
上传 Excel 文件创建表格。标题默认取文件名（去掉扩展名，最长 100 字）；各工作表内容写入草稿。创建后默认关闭分享，需再调用「发布表格」才会同步到分享页。

说明：

1. 支持 `.xlsx`、`.xls`；加密文件不支持
2. 文件大小不超过 2MB；转换后的整表 JSON 也不超过约 2MB
3. 最多 20 个工作表；每个工作表最多 5000 行、200 列
4. 会导入单元格值、公式和合并单元格；样式、图片、图表不会导入

- 请求地址：https://www.pushplus.plus/push/api/open/excel/import
- 请求方式：POST
- Content-Type: multipart/form-data
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数（form-data）

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
file | 是 | 无 | Excel 文件，支持 `.xlsx` / `.xls`，不超过 2MB
folderId | 否 | 根目录 | 放入指定文件夹；空或 `0` 为根目录

- 调用示例（curl）
```
curl -X POST "https://www.pushplus.plus/push/api/open/excel/import" \
  -H "access-key: d7b******62f" \
  -F "file=@/path/to/销售日报.xlsx" \
  -F "folderId=3001"
```
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 0,
    "shareLogin": 1,
    "perm": 2,
    "published": false,
    "publishDirty": false,
    "folderId": 3001,
    "createTime": "2026-08-17 12:00:00",
    "updateTime": "2026-08-17 12:00:00"
  }
}
```
- 响应字段说明：同「创建表格」；`title` 默认取 Excel 文件名。

### 4. 获取表格内容
按分享码获取当前用户自己的表格元信息与草稿正文。`content` 为整表 JSON 字符串，字段含义见上文「表格内容格式」。仅能读取自己创建的表格。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/content?docCode=Sh3xY7kP
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": true,
    "publishTime": "2026-08-13 10:00:00",
    "createTime": "2026-08-12 09:00:00",
    "updateTime": "2026-08-13 12:30:00",
    "content": "{\"id\":\"workbook-1\",\"name\":\"销售日报\",\"sheetOrder\":[\"sheet-1\"],\"sheets\":{\"sheet-1\":{\"id\":\"sheet-1\",\"name\":\"Sheet1\",\"rowCount\":1000,\"columnCount\":20,\"cellData\":{\"0\":{\"0\":{\"v\":\"日期\",\"t\":1},\"1\":{\"v\":\"销售额\",\"t\":1}},\"1\":{\"0\":{\"v\":\"2026-08-13\",\"t\":1},\"1\":{\"v\":12800,\"t\":2}}}}}}"
  }
}
```

`content` 为 JSON 字符串，解析后等价于：

```
{
  "id": "workbook-1",
  "name": "销售日报",
  "sheetOrder": ["sheet-1"],
  "sheets": {
    "sheet-1": {
      "id": "sheet-1",
      "name": "Sheet1",
      "rowCount": 1000,
      "columnCount": 20,
      "cellData": {
        "0": {
          "0": { "v": "日期", "t": 1 },
          "1": { "v": "销售额", "t": 1 }
        },
        "1": {
          "0": { "v": "2026-08-13", "t": 1 },
          "1": { "v": 12800, "t": 2 }
        }
      }
    }
  }
}
```

上例中：第 0 行第 0 列（A1）为文本「日期」，第 0 行第 1 列（B1）为「销售额」；第 1 行第 0 列（A2）为「2026-08-13」，第 1 行第 1 列（B2）为数字 12800。完整字段见上文「表格内容格式」。

- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
docCode | 字符串 | 表格分享码
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
content | 字符串 | 整表草稿 JSON 字符串，解析后字段见上文「表格内容格式」

### 5. 保存表格内容
整表覆盖保存草稿。`content` 为整表 JSON 字符串，字段含义见上文「表格内容格式」。保存后不影响分享页，需再调用「发布表格」才会同步对外内容。仅所有者可保存。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/saveContent
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Sh3xY7kP",
  "content": "{\"id\":\"workbook-1\",\"name\":\"销售日报\",\"sheetOrder\":[\"sheet-1\"],\"sheets\":{\"sheet-1\":{\"id\":\"sheet-1\",\"name\":\"Sheet1\",\"rowCount\":1000,\"columnCount\":20,\"cellData\":{\"0\":{\"0\":{\"v\":\"日期\",\"t\":1},\"1\":{\"v\":\"销售额\",\"t\":1}},\"1\":{\"0\":{\"v\":\"2026-08-13\",\"t\":1},\"1\":{\"v\":12800,\"t\":2}}}}}}"
}
```

`content` 传入前请先将对象序列化为字符串。自行构造时至少需要 `sheetOrder`、`sheets`，以及工作表的 `id`、`name`。单元格可只写 `v`；数字请传数值而不是字符串，便于后续公式计算。

- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码
content | 是 | 无 | 整表 JSON 字符串，须以 `{` 开头，最长约 2MB；解析后字段见上文「表格内容格式」

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": true,
    "publishTime": "2026-08-13 10:00:00",
    "createTime": "2026-08-12 09:00:00",
    "updateTime": "2026-08-13 12:30:00"
  }
}
```
- 响应字段说明：同「创建表格」；已发布过再保存草稿后，`publishDirty` 一般为 `true`。

### 6. 按区域写入单元格
从指定起始单元格起，按二维数组向右向下写入单元格值。写入结果进入草稿，不影响分享页；需再调用「发布表格」才会同步。仅所有者可操作。

适用场景：定时任务追加一行数据、外部系统同步局部区域等，无需每次提交整表 JSON。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/writeCells
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Sh3xY7kP",
  "sheetName": "Sheet1",
  "range": "A2",
  "values": [
    ["2026-08-13", 12800],
    ["2026-08-14", 15600]
  ]
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码
sheetName | 否 | 活动表/第一张表 | 工作表名称
range | 是 | 无 | 起始单元格，如 `A1`；`values` 从此处向右向下展开
values | 是 | 无 | 二维数组，外层为行、内层为列；最多 5000 行、200 列

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": true,
    "publishTime": "2026-08-13 10:00:00",
    "createTime": "2026-08-12 09:00:00",
    "updateTime": "2026-08-13 12:40:00"
  }
}
```
- 响应字段说明：同「创建表格」；写入后 `publishDirty` 一般为 `true`。

### 7. 发布表格
将草稿同步为分享页快照。发布成功后 `published` 为 `true`，`publishDirty` 为 `false`，并写入 `publishTime`。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/publish?docCode=Sh3xY7kP
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": false,
    "publishTime": "2026-08-13 12:45:00",
    "createTime": "2026-08-12 09:00:00",
    "updateTime": "2026-08-13 12:45:00"
  }
}
```
- 响应字段说明：同「创建表格」；发布后 `published` 为 `true`，`publishDirty` 为 `false`。

### 8. 重命名
修改表格标题，仅所有者可操作。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/rename
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Sh3xY7kP",
  "title": "销售日报（已更新）"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码
title | 是 | 无 | 新标题，最长 100 字

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 9. 删除表格
删除表格（逻辑删除），仅所有者可操作。删除后分享链接不可访问。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/delete?docCode=Sh3xY7kP
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 10. 移动表格到文件夹
将表格移动到指定文件夹。`targetFolderId` 为空或 `0` 时移回根目录。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Sh3xY7kP",
  "targetFolderId": 3001
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码
targetFolderId | 否 | 根目录 | 目标文件夹 id；空或 `0` 为根目录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 11. 更新分享设置
开启或关闭表格分享，并可设置打开分享页是否需要登录。仅支持「关闭 / 开启仅查看」，不再提供可编辑分享。

开启分享且从未发布过时，会自动用当前草稿生成首版快照。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/updateShare
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "docCode": "Sh3xY7kP",
  "sharePerm": 1,
  "shareLogin": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
docCode | 是 | 无 | 表格分享码
sharePerm | 是 | 无 | 0关闭 / 1开启（仅可查看）
shareLogin | 否 | 沿用原值 | 0免登录 / 1需登录；开启分享时缺省为需登录

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "docCode": "Sh3xY7kP",
    "shareUrl": "https://www.pushplus.plus/push/excel/Sh3xY7kP",
    "title": "销售日报",
    "sharePerm": 1,
    "shareLogin": 1,
    "perm": 2,
    "published": true,
    "publishDirty": false,
    "publishTime": "2026-08-13 12:45:00",
    "createTime": "2026-08-12 09:00:00",
    "updateTime": "2026-08-13 12:50:00"
  }
}
```
- 响应字段说明：同「创建表格」。

### 12. 推送表格
表格开放接口不单独提供推送接口。发布后可通过 [发送消息接口](/doc/guide/api.md) 推送分享页，`template` 传 `excel`，`pushId` 传 `docCode`。

- 请求地址：https://www.pushplus.plus/send
- 请求方式：POST
- Content-Type: application/json
- 请求参数:
```
{
  "token": "d90******c20",
  "title": "销售日报",
  "content": "请查收",
  "template": "excel",
  "pushId": "Sh3xY7kP",
  "channel": "wechat"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
token | 是 | 无 | 用户token或消息token
title | 否 | 无 | 消息标题
content | 是 | 无 | 消息内容
template | 是 | html | 固定传 `excel`
pushId | 是 | 无 | 表格编码 `docCode`
channel | 否 | wechat | 发送渠道
topic | 否 | 无 | 群组编码，不填仅发送给自己
to | 否 | 无 | 好友令牌，多人用逗号隔开

> 说明：完整参数见 [发送消息接口](/doc/guide/api.md)。

## 二. 文件夹接口
表格工作区的文件夹管理。路径前缀为 `/open/excel/folder`。规则见上文「文件夹说明」。查询只需调用目录树：当前层子文件夹按 `parentId` 过滤即可，不必再提供列表或面包屑接口。

### 1. 文件夹目录树
返回当前用户表格工作区的完整目录树。根目录下的文件夹作为数组第一层，子文件夹在 `children` 中。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/folder/tree
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
      "id": 3001,
      "name": "销售数据",
      "createTime": "2026-08-20 10:00:00",
      "updateTime": "2026-08-20 10:00:00",
      "children": [
        {
          "id": 3002,
          "parentId": 3001,
          "name": "本月销售",
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

- 请求地址：https://www.pushplus.plus/push/api/open/excel/folder/create
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "parentId": 0,
  "name": "销售数据"
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
    "id": 3001,
    "name": "销售数据",
    "createTime": "2026-08-20 10:00:00",
    "updateTime": "2026-08-20 10:00:00"
  }
}
```

### 3. 重命名文件夹

- 请求地址：https://www.pushplus.plus/push/api/open/excel/folder/rename
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 3001,
  "name": "本月销售"
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
删除指定文件夹。其中的子文件夹与表格会上移到父目录，不会被一并删除。

- 请求地址：https://www.pushplus.plus/push/api/open/excel/folder/delete?id=3001
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

- 请求地址：https://www.pushplus.plus/push/api/open/excel/folder/move
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 3001,
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

### 整表写入

```
1. getAccessKey
2. create（创建空白表格）或 import（上传 Excel 生成表格）
3. saveContent（按需写入整表 JSON 草稿；import 已写入内容时可跳过）
4. updateShare（开启分享，可选）
5. publish（同步到分享页）
6. 将 shareUrl 分享给阅读者，或通过 /send 推送（template=excel, pushId=docCode）
```

### 增量追加行

```
1. getAccessKey
2. writeCells（按区域写入草稿，如从 A2 起追加两行）
3. publish（同步到分享页）
```
