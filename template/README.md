# 消息模板说明

## 引言
　&emsp;&emsp;使用template参数来指定消息模板，不同的消息模板会影响接收到消息内容的展示效果。可以根据需要的展示效果来选择，同时注意不同的消息模板会对content参数的内容有所限定和要求。

## 消息模板枚举

模板名称 | 描述 | 使用教程
--| --| --|
html | 默认模板，支持html文本 | 
txt | 纯文本展示，不转义html |
json | 内容基于json格式展示 |
markdown | 内容基于markdown格式展示 | 
cloudMonitor | 阿里云监控报警定制模板 | [阿里云监控](../extend/cloudMonitor.html)
jenkins | jenkins插件定制模板 | [jenkins插件](../extend/jenkins.html)
route | 路由器插件定制模板 | [路由器插件](../extend/route.html)
pay | 支付成功通知模板 | [支付成功模板教程](../extend/pay.html)

## 请求示例

- 请求地址：http://www.pushplus.plus/send
- 请求方式：POST
- 请求内容：

```
{
    "token":"{token}",
    "title":"标题",
    "content":"# 大标题 \n ##### 小标题 \n  1. 第一项 \n 2. 第二项 \n 3. 第三项",
    "template":"markdown"
}
```
- 说明：markdown语法参考[https://www.appinn.com/markdown/](https://www.appinn.com/markdown/)。支持html格式，换行使用\n来表示。
