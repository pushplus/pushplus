# 阿里云监控推送功能
## 引言
　&emsp;&emsp;阿里云提供了一套完善的云监控服务，不仅可以监控阿里云上的服务器、数据库、网站等资源，同时也可以将非阿里云的机器加入到它的监控服务中心去。但是美中不足的是，阿里体系下是用钉钉进行报警提醒的，并不支持微信，于是便开发了这个功能，方便大家利用pushplus来推送阿里云监控的告警信息到微信上。
        
## 使用步骤
1. 在pushplus网站中找到您的用户token或消息token。如果需要一对多推送还需要新建一个群组，记下群组编码。\
![token](./images/info.png)

1. 到阿里云监控后台新增需要报警的规则。
具体可以访问：<a href="https://cloudmonitor.console.aliyun.com/" target="_blank">https://cloudmonitor.console.aliyun.com/</a>
![rule](./images/c2.png)

3. 在创建报警规则>通知方式>报警回调中填入以下格式的地址：
http://www.pushplus.plus/send/{token}?template=cloudMonitor&topic=XXX

参数名称 | 是否必填 | 说明
---|--- | ---
token | 是  | 自己的用户token或消息token
topic | 否 | 群组编码，仅在需要推送给多人的时候填写
template | 是 | 固定填写cloudMonitor

![callback](./images/c31.png)

4. 然后就不需要任何操作了。当发生报警的时候pushplus就会自动推送到您的微信上，就这么简单！\
效果如图：\
![result](./images/c4.png)

## 实现原理
#### 基本原理
　&emsp;&emsp;阿里云监控会在发生报警的时候主动推送消息到回调地址，pushplus的回调地址在接收到请求报文后解析内容，使用专用的监控报警模板，调用微信模板消息接口推送到用户的微信上。\
整个过程相当于执行了如下一个POST请求。
- 请求地址：http://www.pushplus.plus/send/{token}?template=cloudMonitor
- 请求方式：post
- Content-Type: application/json
- 请求报文：

```
{  
   "alertName": "基础监控-ECS-内存使用率", 
   "alertState": "ALERT", 
   "curValue": "97.39", 
   "dimensions": "{userId=12****, instanceId=i-12****}", 
   "expression": "$Average>=95",
   "instanceName": "instance-name-****", 
   "metricName": "Host.mem.usedutilization", 
   "metricProject": "acs_ecs", 
   "namespace": "acs_ecs",  
   "preTriggerLevel": "WARN",  
   "ruleId": "applyTemplateee147e59-664f-4033-a1be-e9595746****", 
   "signature": "eEq1zHuCUp0XSmLD8p8VtTKF****", 
   "timestamp": "1508136760",
   "triggerLevel": "WARN", 
   "userId": "12****"
}
```
具体报文含义参考阿里云文档：<a href="https://help.aliyun.com/document_detail/60714.html?spm=a2c4g.11186623.6.593.c7f571f4mrt11b" target="_blank">https://help.aliyun.com/document_detail/60714.html?spm=a2c4g.11186623.6.593.c7f571f4mrt11b</a>

#### 主机监控和事件监控
　&emsp;&emsp;阿里云的监控有主机监控和事件监控。它们回调的报文内容格式是两种完全不同的内容。

　&emsp;&emsp;事件监控中阿里云下属产品品类多且形态差异大，所以目前就阿里云自身报警也没有很好的语义化表达出来其中的含义。pushplus在推送的报文中仅最大化的优化了内容的展示，部分内容细节涉及的太多没有全部语义化。

![result](./images/c5.png)

　&emsp;&emsp;事件监控参考阿里云文档：<a href="https://help.aliyun.com/document_detail/87929.html?spm=a2c4g.11186623.6.658.
180d2d5aPpX6Jm" target="_blank">https://help.aliyun.com/document_detail/87929.html?spm=a2c4g.11186623.6.658.
180d2d5aPpX6Jm </a>