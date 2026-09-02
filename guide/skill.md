# pushplus Skill 使用说明

## Skill简介
&nbsp;&nbsp;&nbsp;&nbsp;Skill 是给 AI 智能体准备的能力说明书。安装后，智能体会在你需要发通知、推送微信消息、查询发送结果、管理群组好友时，按文档调用 [消息接口](/guide/api.md) 和 [开放接口](/guide/openApi.md)。\
&nbsp;&nbsp;&nbsp;&nbsp;pushplus Notification Skill **无需安装额外依赖**，智能体只要能使用 Shell / curl 即可。兼容 [OpenClaw（Claw）](https://docs.openclaw.ai/tools/skills) 和 [WorkBuddy](https://www.workbuddy.ai/) 等支持 `SKILL.md` 的客户端。\
&nbsp;&nbsp;&nbsp;&nbsp;**只发消息**时提供 `PUSHPLUS_TOKEN` 即可；**调用开放接口**（查发送结果、管群组/好友/黑名单/渠道、绑定 ClawBot 等）还需要用户 token、`secretKey`，并用它们换取 `AccessKey`。仅有一个 pushToken 无法调用开放接口。

当前版本：v1.3.2。技能市场：[ClawHub - pushplus-notification](https://clawhub.ai/pcstx/skills/pushplus-notification)

## 与 MCP Server 的区别

| | Skill | MCP Server |
| --- | --- | --- |
| 运行方式 | 智能体直接按说明书调用 HTTP 接口 | 本地再跑一个 MCP 服务进程 |
| 依赖 | 无，只需 curl / Shell | 需安装 Node 或 Java，并配置 MCP |
| 适用场景 | Claw、WorkBuddy 等 Agent 客户端 | Cursor、Claude Desktop、Cline 等 MCP 客户端 |
| 说明文档 | 本文 | [pushplus MCP Server](/guide/mcp.md) |

两者能力互补，按自己使用的客户端选择即可。

## 前置条件

1. 在 [pushplus 官网](https://www.pushplus.plus) 注册并完成[实名认证](/function/verify.md)，调用发送接口前必须实名。
2. 运行环境能执行 `curl`（macOS / Linux 一般自带；Windows 可用 Git Bash 或系统自带 curl）。
3. 按下面「凭证说明」准备对应密钥。只发消息与调用开放接口所需凭证不同。

## 凭证说明

| 能力 | 需要的凭证 | 说明 |
| --- | --- | --- |
| 发送消息 `/send`、`/batchSend` | `PUSHPLUS_TOKEN` | 用户 token 或消息 token 均可 |
| 开放接口（查结果、群组、好友、渠道、ClawBot 等） | **用户 token** + `secretKey` → `AccessKey` | 消息 token 不能换 AccessKey；请求 IP 须在安全 IP 列表内 |

用户 token 与消息 token 的区别见[用户token和消息token有什么区别](/help/token.md)。开放接口鉴权细节见[开放接口文档 - 获取AccessKey](/guide/openApi.md#一-获取accesskey)。

### 1. 只发消息

设置环境变量或在对话中提供即可：

```
export PUSHPLUS_TOKEN="你的Token"
```

### 2. 调用开放接口

开放接口权限较高，**默认关闭**。需要先在官网完成这些配置：

1. 个人中心 → **开发设置**，开启开放接口。
2. 配置 `secretKey`（建议至少 32 位数字、英文大小写随机组合）。
3. 把 Claw / WorkBuddy 所在机器的公网 IP 加入 **安全 IP** 列表，否则获取 AccessKey 会返回 403。
4. 这里的 token 必须是**用户 token**，不支持消息 token。

Skill 会用用户 token 和 secretKey 换取 AccessKey（有效期约 7200 秒），后续请求在 Header 里带 `access-key`。对应环境变量：

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `PUSHPLUS_TOKEN` | 是 | **用户 token**（开放接口不支持消息 token） |
| `PUSHPLUS_SECRET_KEY` | 是 | 开发设置中的 secretKey |
| `PUSHPLUS_ACCESS_KEY` | 否 | 已缓存的 AccessKey；过期后 Skill 会重新获取 |

```
export PUSHPLUS_TOKEN="你的用户Token"
export PUSHPLUS_SECRET_KEY="你的SecretKey"
```

也可写入项目根目录 `.env`（Skill **只会读取** `PUSHPLUS_` 开头的行）：

```
PUSHPLUS_TOKEN=你的用户Token
PUSHPLUS_SECRET_KEY=你的SecretKey
```

凭证优先级：对话中提供 → 环境变量 → `.env`。找不到时智能体会询问，不会猜测。完整 token / secretKey / accessKey 不会在回复里明文展示。

> 重复获取 AccessKey 会使旧 key 失效。Claw、WorkBuddy 与其他程序不要同时各自刷新，否则会互相覆盖。请求机器 IP 不在安全 IP 列表内时，会返回 403。

## 获取 Skill

### 1. ClawHub（推荐）

技能主页：[https://clawhub.ai/pcstx/skills/pushplus-notification](https://clawhub.ai/pcstx/skills/pushplus-notification)

OpenClaw 安装：

```
openclaw skills install @pcstx/pushplus-notification
```

希望所有本地 Agent 都能用时，加上 `--global`：

```
openclaw skills install @pcstx/pushplus-notification --global
```

也可以用 ClawHub CLI：

```
npx clawhub@latest install @pcstx/pushplus-notification
```

或直接对智能体说：

```
帮我用 ClawHub 安装 pushplus-notification。如果还没装 ClawHub，先安装（npm i -g clawhub）。
```

### 2. 手动下载

无法访问 ClawHub 时，可下载压缩包后手动安装：

[https://1822104859.share.123pan.cn/123pan/3UMBjv-HwGUh](https://1822104859.share.123pan.cn/123pan/3UMBjv-HwGUh)

解压后目录如下，核心文件是 `SKILL.md`：

```
skill/
├── SKILL.md        # 技能主文件（必需）
├── reference.md    # 开放接口说明（按需加载）
└── README.md
```

请将 `skill` 文件夹**重命名为** `pushplus-notification`，再拷贝到对应客户端的技能目录。智能体通过目录名和 `SKILL.md` 里的 `name` 识别技能。

## 在 OpenClaw（Claw）中使用

### 安装位置

| 范围 | 路径 | 说明 |
| --- | --- | --- |
| 当前工作区 | `<工作区>/skills/pushplus-notification/` | 只对当前 Agent 生效 |
| 本机共享 | `~/.openclaw/skills/pushplus-notification/` | 对应 `openclaw skills install ... --global` |

手动安装示例：

```
# 解压后重命名，再拷到 OpenClaw 技能目录
mv skill pushplus-notification
cp -R pushplus-notification ~/.openclaw/skills/
```

本地目录安装也可以：

```
openclaw skills install ./pushplus-notification
```

安装后重启或新开一轮对话，技能就会被加载。

### 配置凭证

只发消息：配置 `PUSHPLUS_TOKEN`。要查发送结果、管群组好友等，再配置 `PUSHPLUS_SECRET_KEY`（须为用户 token）。详见上文「凭证说明」。

### 对话示例

安装完成后，直接用自然语言即可，例如：

- 发送一条微信消息通知我任务完成了
- 用 ClawBot 渠道提醒我
- 把这段错误日志推送到我的邮箱
- 用 pushplus 同时发微信和邮件通知
- 帮我查一下刚才那条消息发成功了没有（需开放接口凭证）

智能体会先展示标题和内容摘要，**确认后再真正发送**。`code=200` 只表示服务端已受理，返回的流水号可用于查询最终结果；查询结果走开放接口，必须先配好用户 token 和 secretKey。

## 在 WorkBuddy 中使用

WorkBuddy 兼容 OpenClaw 的 `SKILL.md` 格式，安装后即可在对话里触发推送。

### 方式一：拷贝到技能目录

解压并重命名后，放到用户级技能目录（跨项目通用）：

- macOS / Linux：`~/.workbuddy/skills/pushplus-notification/`
- Windows：`%USERPROFILE%\.workbuddy\skills\pushplus-notification\`

```
mv skill pushplus-notification
cp -R pushplus-notification ~/.workbuddy/skills/
```

只想在某个项目里使用时，放到项目根目录的 `.workbuddy/skills/pushplus-notification/`。

拷贝完成后重启 WorkBuddy，或新开一轮对话。可在技能列表中确认是否出现 `pushplus-notification`。

### 方式二：界面导入

1. 打开 WorkBuddy，进入 Skills / 技能管理。
2. 选择「导入」或「导入技能包」。
3. 选择解压并重命名后的 `pushplus-notification` 文件夹，或自行将 `SKILL.md`、`reference.md` 打成 zip 后导入。
4. 导入成功后即可在当前会话中使用。

> 从网盘下载的压缩包根目录名是 `skill`，导入前请先改名为 `pushplus-notification`，避免技能显示成无意义的名称。

### 配置凭证与使用

与 OpenClaw 相同：只发消息配置 `PUSHPLUS_TOKEN`；调用开放接口还需 `PUSHPLUS_SECRET_KEY`，且 token 必须是用户 token。对 WorkBuddy 说：

- 用 pushplus 给我发一条微信通知，标题是「部署完成」，内容是「生产环境已发布」
- 帮我把会议纪要推到邮箱
- 查一下刚才那条消息的发送结果

也可以用 `@pushplus-notification` 手动指定技能。

## 常用能力说明

Skill 会按 [消息接口文档](/guide/api.md) 调用接口，常用参数如下。

### 发送渠道（channel）

| 值 | 费用 | 说明 |
| --- | --- | --- |
| wechat | 免费 | 微信公众号（默认） |
| app | 免费 | App（安卓 / 鸿蒙 / iOS） |
| extension | 免费 | 浏览器插件 / 桌面应用程序 |
| webhook | 免费 | 第三方 webhook，需填写渠道编码 option |
| clawbot | 免费 | 微信 ClawBot，见[渠道说明](/channel/clawbot.md) |
| qq | 免费 | QQ 机器人，发给自己或 QQ 群，见[渠道说明](/channel/qq.md) |
| cp | 免费 | 企业微信应用，需 option |
| mail | 免费 | 邮箱，option 可选 |
| sms | 收费 | 短信 |
| voice | 收费 | 语音 |

多渠道一次发送时，使用 `/batchSend`，`channel` 用逗号分隔，如 `wechat,mail`。

### 发送模板（template）

| 场景 | 建议模板 |
| --- | --- |
| 简单文本、ClawBot、QQ 机器人 | txt |
| 报告 / 日志 | markdown |
| 富文本 / 邮件 | html（默认） |
| 结构化数据 | json |
| push 表单 / 文档 / 表格 | form / doc / excel，需同时传 pushId |

### 注意事项

1. 发送前智能体会展示摘要并等待确认，避免误发。
2. `topic`（群组）与 `to`（好友）不要同时填写。
3. `webhook`、`cp`、`qq` 的 `option` 填个人中心已配置的**渠道编码**，不是完整 URL。qq 不填 option 时发给自己。
4. 短信、语音为收费渠道，发送前会提示消耗积分。
5. 完整 token、secretKey、accessKey 不会在回复里明文展示。
6. 删除消息、群组、好友、解绑 ClawBot 等破坏性操作也会先确认。
7. 查发送结果、管理群组/好友等必须走开放接口：需要**用户 token + secretKey**，并在开发设置中开启、配置安全 IP。只有 pushToken（尤其是消息 token）不够。

查询发送结果、管理群组 / 好友 / 黑名单 / 渠道、绑定 ClawBot 等开放能力，见 [开放接口文档](/guide/openApi.md)。
