# 华硕路由器插件

> 0.5 版本 - 2022年3月3日\
> 更新内容：\
> 更新了接口地址和插件图标。可以正常使用各项目功能。

## 引言

　&emsp;&emsp;华硕路由器在家用路由器中属于高端产品。其用料十足、性能强大以外还支持刷第三方梅林固件，并可以安装第三方开发的插件来丰富路由器的功能。pushplus的路由器插件功能实现了在网络重联、客户端上线等情况下主动推送相关信息到微信上，方便用户查看路由器状态。\
　&emsp;&emsp;本插件由koolshare论坛的 **[囍冯总囍]** 开发，在此特别感谢！

## 离线安装包下载
- 0.5版本离线安装包

hnd平台：[https://image.pushplus.plus/route/hnd/pushplus.tar.gz](https://image.pushplus.plus/route/hnd/pushplus.tar.gz) \
arm384平台：[https://image.pushplus.plus/route/arm384/pushplus.tar.gz](https://image.pushplus.plus/route/arm384/pushplus.tar.gz)

官方商城上架视审批情况而定（比较慢），可以提前离线下载自行安装。

## 使用步骤
　&emsp;&emsp;插件已上架rogsoft和armsoft，源码开放。\
&emsp;&emsp;rogsoft是基于梅林hnd/axhnd平台路由器的软件中心，其与梅林arm380/arm380软件中心的插件不兼容！rogsoft仅适用于koolshare 梅林/官改平台，且linux内核为4.1.27/4.1.51的armv8架构（aarch64）的路由器！\
&emsp;&emsp;armsoft是基于梅林384的软件中心，其与梅林380软件中心的插件不兼容！armsoft仅适用于koolshare 梅林384平台，且linux内核为2.6.36.4的armv7l架构的路由器！\

rogsoft开源项目地址：<a href="https://github.com/koolshare/rogsoft" target="_blank">https://github.com/koolshare/rogsoft</a> \
armsoft开源项目地址：[https://github.com/koolshare/armsoft](https://github.com/koolshare/armsoft)


1. 在软件中心里面找到并安装“pushplus全能推送”。


![](../images/r1.jpg)

2. 在软件的基础设置中开启pushplus，然后填入自己的用户token或消息token，点击“提交”保存配置。


![](../images/r2.jpg)

3. 配置完成，可以点击“手动推送”进行测试是否可以正常收到路由器的推送消息。


![](../images/r3.jpg)


## 实现原理
　&emsp;&emsp;路由器对网络重启，DHCP分配新客户端，手动推送，定时推送这几个事件使用shell脚本进行了逻辑处理。通过HTTP POST方式将路由器信息推送到pushplus上，pushplus使用定制模板将消息发送到用户微信上。\
　&emsp;&emsp;不同的事件推送的内容是完全不同，根据内容中的msgTYPE字段来区分不同的事件类型。
1. 网络重启 ifUP
- 请求地址：http://www.pushplus.plus/send/{token}
- 请求方式：POST
- Content-Type: application/json
- 请求报文：
```
{
	'title':'网络重启',
	'template':'route',
	'topic':'',
	'content':'{
                    "upTIME": "2天 21小时 22分钟 58秒",
                    "netSTATE": [{
                        "wanRX": "23.5 GiB",
                        "wanTX": "10.6 GiB",
                        "wanIPv4": "114.218.254.88",
                        "proto": "pppoe",
                        "pubIPv4": "114.218.254.88",
                        "pubIPv6": "",
                        "wanDNS": ["218.4.4.4", "218.2.2.2"]
                    }],
                    "msgTYPE": "ifUP",
                    "rebootTIME": "2020年05月22日 17点34分38秒"
                }'
}
```

2. DHCP分配新客户端 newDHCP
- 请求地址：http://www.pushplus.plus/send/{token}
- 请求方式：POST
- Content-Type: application/json
- 请求报文：
```
{
	'title':'有新客户端上线',
	'template':'route',
	'topic':'',
	'content':'{
                    "upTIME": "2020年05月22日 17点39分44秒",
                    "cliIP": "192.168.199.202",
                    "expTIME": "2020年05月23日 17点39分44秒",
                    "cliLISTS": [{
                        "ip": "192.168.199.71",
                        "name": "zimi-powerstrip-v2_miio94513445"
                    }, {
                        "ip": "192.168.199.73",
                        "name": "bin"
                    }],
                    "cliNAME": "MiAiSoundbox",
                    "msgTYPE": "newDHCP",
                    "cliMAC": "50:a0:09:db:99:28"
                }'
}
```

3. 手动推送和定时推送 manuINFO和cronINFO
- 请求地址：http://www.pushplus.plus/send/{token}
- 请求方式：POST
- Content-Type: application/json
- 请求报文：
```
{
	'title':'路由器状态',
	'template':'route',
	'topic':'',
	'content':'{
                "netINFO": {
                    "wifiINFO": {
                        "SmartConnect": "TEST"
                    },
                    "WAN": [{
                        "wanRX": "23.5 GiB",
                        "wanTX": "10.6 GiB",
                        "wanIPv4": "114.218.254.88",
                        "proto": "pppoe",
                        "pubIPv4": "114.218.254.88",
                        "pubIPv6": "",
                        "wanDNS": ["218.4.4.4", "218.2.2.2"]
                    }],
                    "DDNS": "",
                    "routerLANIP": "192.168.199.1",
                    "guestINFO": {"24G1":"ASUS_40_2G_Guest"}
                },
                "cliINFO": [{
                    "ip": "192.168.199.250",
                    "name": "MEIZU-PRO-6.lan"
                }, {
                    "ip": "192.168.199.121",
                    "name": "?"
                }],
                "dhcpINFO": [{
                    "ip": "192.168.199.73",
                    "name": "base.sh"
                }, {
                    "ip": "192.168.199.250",
                    "name": "MEIZU-PRO-6"
                }],
                "sysINFO": {
                    "routerFIRMWARE": "384.17_0",
                    "routerTIME": "2020年05月22日 17点31分53秒",
                    "routerUPSECONDS": 249614,
                    "routerNAME": "RT-AC86U-5E40",
                    "routerMEM": {
                        "all": 429.99,
                        "unit": "MB",
                        "free": 101.07
                    },
                    "routerAVGLOAD": [2.33, 2.39, 2.36],
                    "routerMODE": "无线路由器",
                    "routerJFFS": {
                        "total": "48.0M",
                        "use": "9%",
                        "available": "43.7M",
                        "used": "4.3M"
                    },
                    "routerUPTIME": "2天21时20分14秒",
                    "routerSWAP": {
                        "total": 512,
                        "free": 512
                    }
                },
                "tempINFO": {
                    "unit": "°C",
                    "24G": 54,
                    "CPU": 75.3,
                    "5G1": 59
                },
                "msgTYPE": "manuINFO",
                "usbINFO": [{
                    "total": "0",
                    "use": "10%",
                    "name": "Toshiba External USB 3.0",
                    "used": "0",
                    "free": "0",
                    "status": "mounted"
                }, {
                    "total": "0",
                    "use": "7%",
                    "name": "Generic Mass Storage",
                    "used": "0",
                    "free": "0",
                    "status": "mounted"
                }]
            }'
}
```