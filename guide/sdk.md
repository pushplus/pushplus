# pushplus SDK

## 引言

为了方便调用 pushplus 接口、避免自行编码的复杂度，官方提供了多语言 SDK。SDK 已封装**发送频率控制**、**开放接口 AccessKey 管理**、**消息回调解析**等常见场景，可在项目中快速集成，降低开发成本和出错概率。

SDK实现了：发送消息接口，多渠道发送消息接口，pushplus开放接口，push表单、push文档、push表格的开放接口。

目前支持 **Java**、**Python**、**Node.js**、**Go** 四种语言，后续会视情况增加其他语言。

## Java SDK

### 1. 引入依赖

普通 Java 项目：

```xml
<dependency>
    <groupId>com.perk-net</groupId>
    <artifactId>perk-pushplus-sdk-core</artifactId>
    <version>1.3.2</version>
</dependency>
```

Spring Boot 项目：

```xml
<dependency>
    <groupId>com.perk-net</groupId>
    <artifactId>perk-pushplus-sdk-spring-boot-starter</artifactId>
    <version>1.3.2</version>
</dependency>
```

### 2. Spring Boot 配置

`application.yml`：

```yaml
pushplus:
  token: ${PUSHPLUS_TOKEN}
  secret-key: ${PUSHPLUS_SECRET_KEY}
```

具体使用参考源码地址中的 README.md。
maven仓库地址：[https://central.sonatype.com/artifact/com.perk-net/perk-pushplus-sdk-spring-boot-starter](https://central.sonatype.com/artifact/com.perk-net/perk-pushplus-sdk-spring-boot-starter)

### 3. 源码地址

- Github：[https://github.com/pushplus/perk-pushplus-sdk](https://github.com/pushplus/perk-pushplus-sdk)
- Gitee：[https://gitee.com/perk-net/perk-pushplus-sdk](https://gitee.com/perk-net/perk-pushplus-sdk)

## Python SDK

### 1. 构建客户端

```python
from perk_pushplus import PushPlusClient

client = (
    PushPlusClient.builder()
    .token("your_user_token")          # 个人中心 -> 一对一推送
    .secret_key("your_secret_key")     # 个人中心 -> 开发设置（开放接口必填）
    .build()
)
```

> `PushPlusClient` 线程安全，建议作为单例长期持有。

### 2. 发送消息

```python
from perk_pushplus import Channel, SendRequest, Template

# 最简：默认 wechat / html
short_code = client.send_simple("标题", "<b>内容</b>")

# 完整：使用 Builder
short_code = client.send(
    SendRequest.builder()
    .title("CPU 告警")
    .content("# CPU > 90%\n请尽快处理")
    .template(Template.MARKDOWN)
    .channel(Channel.WECHAT)
    .topic("ops")
    .callback_url("https://your.host/pushplus/callback")
    .build()
)
```

更多使用说明参考：[https://pypi.org/project/perk-pushplus-sdk/](https://pypi.org/project/perk-pushplus-sdk/)

### 3. 源码地址

- Github：[https://github.com/pushplus/perk-pushplus-python-sdk](https://github.com/pushplus/perk-pushplus-python-sdk)
- Gitee：[https://gitee.com/perk-net/perk-pushplus-python-sdk](https://gitee.com/perk-net/perk-pushplus-python-sdk)

## Node.js SDK

### 1. 安装

```bash
npm install @perk-net/perk-pushplus-sdk
# 或
pnpm add @perk-net/perk-pushplus-sdk
# 或
yarn add @perk-net/perk-pushplus-sdk
```

浏览器直接通过 CDN 引入：

```html
<script src="https://unpkg.com/@perk-net/perk-pushplus-sdk/dist/index.global.js"></script>
<script>
  // 全局变量名 PerkPushPlus
  const client = new PerkPushPlus.PushPlusClient({ token: 'your_user_token' });
  client.sendSimple('标题', 'Hello PushPlus').then(console.log);
</script>
```

更多使用查看项目地址：[https://www.npmjs.com/package/@perk-net/perk-pushplus-sdk](https://www.npmjs.com/package/@perk-net/perk-pushplus-sdk)

### 2. 源码地址

- Github：[https://github.com/pushplus/perk-pushplus-nodejs-sdk](https://github.com/pushplus/perk-pushplus-nodejs-sdk)
- Gitee：[https://gitee.com/perk-net/perk-pushplus-nodejs-sdk](https://gitee.com/perk-net/perk-pushplus-nodejs-sdk)

## Go SDK

纯 Go 实现，基于标准库 `net/http`，无额外重依赖。覆盖**消息发送接口**与**全部开放接口**，内置 AccessKey 自动管理、本地限流守卫（命中 `code=900` 时自动短路）与类型化回调解析。

### 1. 引入依赖

```bash
go get github.com/pushplus/perk-pushplus-go-sdk
```

### 2. 构建客户端

```go
import pushplus "github.com/pushplus/perk-pushplus-go-sdk"

client := pushplus.NewClient(
    pushplus.WithToken("your_user_token"),     // 必填，个人中心 -> 一对一推送
    pushplus.WithSecretKey("your_secret_key"), // 调用开放接口才需要
)
```

> `Client` 线程安全，建议作为单例长期持有。

### 3. 发送消息

```go
// 最简：默认 wechat / html
shortCode, err := client.SendSimple(ctx, "标题", "Hello PushPlus")

// 完整：Markdown / 群组 / 回调
_, err = client.Send(ctx, &pushplus.SendRequest{
    Title:       "CPU 告警",
    Content:     "# CPU > 90%\n请尽快处理",
    Template:    pushplus.TemplateMarkdown,
    Channel:     pushplus.ChannelWechat,
    Topic:       "ops",
    CallbackURL: "https://your.host/pushplus/callback",
})

// 多渠道发送
req := (&pushplus.BatchSendRequest{
    Title:   "多渠道告警",
    Content: "CPU > 90%",
}).
    AddChannel(pushplus.ChannelWechat, "").
    AddChannel(pushplus.ChannelWebhook, "bark")

results, err := client.BatchSend(ctx, req)
```

### 4. 开放接口

配置 `secretKey` 后，AccessKey 由 SDK 自动获取与刷新，可直接调用：

```go
me, err := client.User().MyInfo(ctx)
msgs, err := client.OpenMessage().List(ctx, pushplus.NewPageQuery(1, 20))
topics, err := client.Topic().List(ctx, pushplus.NewTopicListQuery(1, 20, 0))
```

更多能力（Webhook 配置、图片服务、回调解析、限流守卫等）见源码 README。

### 5. 源码地址

- Github：[https://github.com/pushplus/perk-pushplus-go-sdk](https://github.com/pushplus/perk-pushplus-go-sdk)
- Gitee：[https://gitee.com/perk-net/perk-pushplus-go-sdk](https://gitee.com/perk-net/perk-pushplus-go-sdk)
