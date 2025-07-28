# 发送渠道说明

## 引言
　&emsp;&emsp;pushplus支持多种发送渠道，可以通过接口上的channel参数来指定想要的推送消息渠道。如不指定默认使用官网微信公众号渠道发送。

## 发送渠道枚举

发送渠道 | 是否免费 | 描述 | 使用教程
---| --- |--- | --- | 
wechat | 免费 | 微信公众号渠道 | [绑定自己的公众号](../extend/mp.html)
webhook | 免费 | 第三方webhook渠道；企业微信、钉钉、飞书、bark、Gotify、腾讯轻联、集简云、server酱、IFTTT、WxPusher；| [webhook渠道配置](../extend/webhook.html)
cp | 免费 | 企业微信应用渠道 | [企业微信应用配置](../extend/cp.html)
mail | 免费 | 邮箱渠道 | [邮件渠道使用说明](../extend/mail.html)
sms | 收费 | 短信渠道。成功发送1条短信需要10积分（0.1元） | [短信渠道配置](../extend/sms.html)

## 请求示例

- 请求地址：http://www.pushplus.plus/send
- 请求方式：POST
- 请求内容：

```
{
    "token":"{token}",
    "title":"标题",
    "content":"消息内容",
    "channel":"webhook",
    "webhook":"pushplus"
}
```
- 说明：使用webhook渠道的示例。具体请查看对应渠道的配置教程。