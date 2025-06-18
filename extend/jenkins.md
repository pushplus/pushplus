# Jenkins插件

## 引言
　&emsp;&emsp;Jenkins作为开发必备之神器，各家大小公司都在使用。Jenkins自身内置了基于邮件推送构建结果的功能。但是随着移动互联网的发展，邮件这玩意已经越来越少使用了，是否有一种办法能把Jenkins构建结果直接推送到微信上，方便查看的工具呢。找了半天并没有找到一款太理想的工具，于是便自己开发了一款Jenkins插件来实现这样的功能。分享给大家，一起来使用！

## 使用步骤
#### 1. 获取token和群组编码
&emsp;&emsp;访问网址：[http://www.pushplus.plus/push2.html](http://www.pushplus.plus/push2.html)   使用微信扫码即可登陆。

&emsp;&emsp;然后新建一个群组。群组编码作为群组的唯一标示，后续需要使用。群组名称随意填写。

&emsp;&emsp;创建成功之后点击群组上的“查看二维码”，将二维码发给需要加入群组的同事。以后推送的消息加入群组的用户都会收的到。在“订阅人”中可以主动的移除不想要的用户。
![群组](./images/group1.png)

 &emsp;&emsp;最后需要您的token和群组编码，在后续jenkins配置中使用。

#### 2. 安装jenkins插件
&emsp;&emsp;目前插件并没有发布到jenkins的官方插件库中，所以需要手动下载安装。后续我们将会推送到官方插件库中。\
&emsp;&emsp;jenkins插件下载地址：百度网盘：[https://pan.baidu.com/s/1MON44GtnTNvxnqjtkb2oJg](https://pan.baidu.com/s/1MON44GtnTNvxnqjtkb2oJg) 提取码: x2u2
 
 &emsp;&emsp;下载完成之后，到jenkins中安装插件。手动安装点击： 系统管理（Manage Jeknis）->插件管理（Manage Plugins）->高级->上传插件 ；选择刚刚下载好的插件文件，点击上传。

&emsp;&emsp;安装完成之后，需要重启jenkins，让插件生效。

![](./images/jenkins3.jpg)

&emsp;&emsp;重启jenkins后，在插件管理->已安装 中能找到“pushPlus Plugin”就代表安装成功啦！

![](./images/jenkins4.jpg)

#### 3. 配置jenkins
 &emsp;&emsp;插件安装完成之后还需要配置一些参数，才能正常推送消息。

&emsp;&emsp;到  系统管理（Manage Jeknis）-> 系统设置（Configure System）->Extended Push+ 账号信息  中设置您的Jenkins地址和您pushplus的用户token或消息token

 - 您的Jenkins URL地址 用于推送消息点击后跳转的链接地址

- 您的Token 指的是pushplus分配给您的用户token或者消息token，请到pushplus网站上获取，请务必填写正确

![](./images/jenkins5.jpg)

 &emsp;&emsp;然后就可以到您的具体构建任务中配置了。在构建后操作中把plusplus增加进来，然后填入您自己的群组编码，保存即可。

&emsp;&emsp;如果您使用的是pipeline，插件也是支持的，语法如下：

```javascript
post {
       always {         
           pushplus (
               "你的群组编码"
           )            
       }
   }
```
![](./images/jenkins6.jpg)

&emsp;&emsp;然后就可以正常使用了。jenkins构建以后，微信上就会收到构建结果的推送消息了。点击消息内容，直接打开您的jenkins构建日志，方便排查构建结果。

![](./images/jenkins7.jpg)


## 实现原理
&emsp;&emsp;Jenkins是对于插件提供了丰富的接口参数。pushplus插件本身在jenkins构建的时候触发执行，可以读取到构建有关的信息，如构建的项目名称、构建编号、构建状态等。然后在构建完成的时候将这些信息拼装后通过pushplus发送到用户的微信上。\
&emsp;&emsp;核心拼装执行了一个POST请求。pushplus接收到请求后针对性的调用了定制模板，通过微信模板消息接口发送到用户微信上。
- 请求地址：http://www.pushplus.plus/send/{token}?template=jenkins
- 请求方式：POST
- Content-Type: application/json
- 请求报文：
```
{
    "topic":"group",
    "title":"测试项目构建成功",
    "buildState":"构建成功",
    "projectName":"测试项目",
    "buildNumber":"#11",
    "buildUser":"pushplus",
    "buildLogUrl":"",
    "projectUrl":"",
    "costTime":"23"
}
```

后续会将插件代码开源出来，供大家学习参考。