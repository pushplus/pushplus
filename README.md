# 介绍
![pushplus消息推送](./images/push.png)

> **官网：[www.pushplus.plus](https://www.pushplus.plus)** \
> **微信公众号：pushplus 推送加** \
> **QQ交流群：28619686 <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=t9IbRihvvusEIo7r6bgz-7QgEPOaH0OU&jump_from=webapi">![pushplus用户交流群](./images/group.png)</a>** \
> **&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 161672256 <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=NQsL2uotO-d-i2uMYa-HiypRHc7IIs2z&jump_from=webapi">![pushplus用户交流2群](./images/group.png)</a>** 

## 引言
　&emsp;&emsp;pushplus(推送加)是一个集成了微信、短信、邮件、企业微信、钉钉、飞书、bark、Gotify、腾讯轻联、集简云等渠道的实时消息推送平台。只需要调用简单的API，即可帮您迅速完成消息的推送，使用简单方便。

## 开发的目的
　&emsp;&emsp;pushplus的目的就是大幅简化消息类推送功能的开发。像是微信公众号的主动推送技术上并不复杂，但是需要认证服务号，备案的域名。这就导致了个人用户与模板消息无缘。而很多时候开发者也只需要一个简单的提醒功能，单独去维护一个推送项目，成本太大，所以pushplus就是为了解决这些用户的痛点，为帮助普通用户和开发者而来的。

## 文档目录

### 简介
- [介绍](/) - pushplus消息推送平台介绍
- [联系我们](/introduce/contact.md) - 联系方式

### 使用教程
- [一对一消息](/function/one.md) - 一对一推送功能
- [一对多消息](/function/more.md) - 一对多推送功能
- [好友消息](/function/friend.md) - 好友功能介绍
- [文本命令](/function/txt.md) - 文本处理功能
- [会员功能](/function/vip.md) - 会员特权功能
- [收/发消息设置](/function/setting.md) - 系统设置功能
- [系统功能额度](/guide/use.md) - 系统功能使用额度
- [消息接口限制](/help/limit.md) - 使用限制说明
- [实名认证说明](/function/verify.md) - 账号验证功能
- [预处理信息配置](/function/pre.md) - 消息预处理功能

### API文档
- [消息接口文档](/guide/api.md) - API接口使用说明
- [开放接口文档](/guide/openApi.md) - 开放API说明
- [消息回调说明](/guide/callback.md) - 回调接口使用说明
- [返回码说明](/guide/code.md) - 状态码说明
- [Demo代码](/guide/demo.md) - 各种语言的代码示例

### 渠道配置
- [发送渠道说明](/channel/) - 消息发送渠道说明
- [短信渠道配置](/extend/sms.md) - 短信集成
- [绑定自己的微信公众号](/extend/mp.md) - 微信公众号集成
- [webhook渠道配置](/extend/webhook.md) - WebHook集成
- [邮件渠道配置](/extend/mail.md) - 邮件集成
- [企业微信应用配置](/extend/cp.md) - 企业微信集成
- ['浏览器插件使用教程'](/extend/extension.md) - 浏览器插件

### 消息模板
- [消息模板说明](/template/) - 消息模板中心
- [支付成功通知模板](/extend/pay.md) - 支付通知集成
- [Jenkins插件](/extend/jenkins.md) - Jenkins集成
- [阿里云监控](/extend/cloudMonitor.md) - 云监控集成
- [路由器插件](/extend/route.md) - 路由器插件

### 扩展应用
- [xxl-job推送设置](/extend/xxl-job.md) - XXL-Job集成
- [推送到企业微信机器人教程](/extend/cpbot.md) - 企业微信机器人配置
- [推送到钉钉机器人教程](/extend/dingding.md) - 钉钉机器人配置
- [推送到飞书机器人教程](/extend/feishu.md) - 飞书机器人配置
- [通过腾讯轻联实现发送短信](/extend/hiflow.md) - 腾讯轻联集成
- [通过集简云发送企业微信消息](/extend/jijyun.md) - 集简云集成
- [调用IFTTT的webhook](/extend/ifttt.md) - IFTTT集成

### 常见问题
- [常见问题](/help/) - 使用帮助和常见问题
- [Get请求导致的问题](/help/get.md) - Get请求问题
- [实名认证相关问题](/help/verify.md) - 验证功能说明
- [用户token和消息token有什么区别](/help/token.md) - Token使用说明
- [发送消息接口限制](/help/limit.md) - 使用限制说明
- [微信消息模板是否可以自定义](/help/template.md) - 消息模板说明
- [收不到消息如何排查](/help/message.md) - 消息相关问题
- [才收到几条消息却被限制发送了](/help/count.md) - 使用统计说明
- [IP被禁止访问原因](/help/ip.md) - IP限制说明
- [如何解封账号](/help/lockdown.md) - 账号封禁说明
- [一对多消息为什么只有我自己收到](/help/topic.md) - 主题功能说明
- [提示无用户接收消息](/help/nouser.md) - 无用户问题
- [如何在公众号中显示推送内容](/help/showmessage.md) - 消息展示问题
- [菜单上的激活消息有什么用](/help/activation.md) - 关于激活消息
- [是否支持发送图片](/help/image.md) - 图片发送说明
- [消息内容中如何换行](/help/line.md) - 消息换行问题
- [用户信息状态不合法](/help/status.md) - 状态码说明
- [接口是否支持https](/help/https.md) - HTTPS相关问题
- [json模板如何正确展示](/help/json.md) - JSON格式说明
- [pushplus官网](/help/homepage.md) - 主页功能说明

