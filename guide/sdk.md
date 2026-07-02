# pushplus SDK

## 引言
&nbsp;&nbsp;&nbsp;&nbsp;为了方便大家调用pushplus接口，避免自行编码的复杂度。特别是处理发送消息频率问题，开放接口令牌逻辑，回调接口等场景。提供了pushplus接口的sdk，可以在项目中快速的使用，减少开发成本和出错的可能性。后续会视情况增加其他开发语言的sdk。

## Java SDK 

普通 Java 项目：

```xml
<dependency>
    <groupId>com.perk-net</groupId>
    <artifactId>perk-pushplus-sdk-core</artifactId>
    <version>1.1.0</version>
</dependency>
```

Spring Boot 项目：

```xml
<dependency>
    <groupId>com.perk-net</groupId>
    <artifactId>perk-pushplus-sdk-spring-boot-starter</artifactId>
    <version>1.1.0</version>
</dependency>
```

Spring Boot 配置：

`application.yml`：

```yaml
pushplus:
  token: ${PUSHPLUS_TOKEN}
  secret-key: ${PUSHPLUS_SECRET_KEY}
```

具体使用参考源码地址中的README.md

### 源码地址
Github：[https://github.com/pushplus/perk-pushplus-sdk](https://github.com/pushplus/perk-pushplus-sdk) \
Gitee：[https://gitee.com/perk-net/perk-pushplus-sdk](https://gitee.com/perk-net/perk-pushplus-sdk)

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
Github：[https://github.com/pushplus/perk-pushplus-python-sdk](https://github.com/pushplus/perk-pushplus-python-sdk)\
Gitee：[https://gitee.com/perk-net/perk-pushplus-python-sdk](https://gitee.com/perk-net/perk-pushplus-python-sdk)

## Nodejs SDK
### 安装

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

### 源码地址
Github：[https://github.com/pushplus/perk-pushplus-nodejs-sdk.git](https://github.com/pushplus/perk-pushplus-nodejs-sdk.git)\
Gitee：[https://gitee.com/perk-net/perk-pushplus-nodejs-sdk](https://gitee.com/perk-net/perk-pushplus-nodejs-sdk)
