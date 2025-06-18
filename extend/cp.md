# 通过企业微信应用给微信发送消息教程

## 引言
　&emsp;&emsp;pushplus已经实现通过企业微信应用给微信发送消息了。整体使用体验上会更加的贴近于微信公众号，灵活度玩法也会更多。

## 企业可信IP
　&emsp;&emsp;2022年6月20日开始在企业微信中创建的第三方应用需要填写企业可信IP地址和信任域名。历史老应用不受影响无需配置，可以直接使用。
针对新创建的应用，需要使用代理地址来让pushplus发送企业微信消息，需要您有一个公网ip地址，具体配置方式见第三步。

![](./images/cp0.png)

## 会员特权
#### 直接显示纯文本内容
会员用户在发送模板为txt的情况下，如果消息标题+消息内容文字小于1900个字的话，消息会直接以文字的形式发送。其他情况下会使用图文的方式发送。\
效果如下：

![](./images/txt.png)

## 具体步骤如下：
#### 一、注册企业微信
　&emsp;&emsp;个人用户也可以免费注册。注册地址：https://work.weixin.qq.com/wework_admin/register_wx?from=loginpage

#### 二、在企业微信中创建应用
1. 打开企业微信管理后台，在应用管理中创建应用。

![](./images/cp1.webp)
 
2. 创建应用
应用logo上传下图；

![](./images/logo2.png)

应用名称填写：pushplus；
可见范围选择公司名；

![](./images/cp31.png)
 
3. 创建应用后进入应用详情页面。记录并保持AgentId（应用ID）和Secret（应用密钥），后面在pushplus配置中会用到。

![](./images/cp41.png)
 
1. 在我的企业中获取企业ID

![](./images/cp5.webp)
 
5. 在“pushplus 推送加”公众号的菜单中点击“功能”->“个人中心”->“第三方配置”。选择“企业微信应用”标签，点击右上角的新增按钮，新增一个企业微信应用配置。

![](./images/cp6.webp)
 
- 应用名称：随便填写，方便自己区分；
- 应用编码：随便填写，发送接口中使用，用于webhook参数；
- 应用ID：对应自己创建应用中的AgentId
- 应用密钥：对应自己创建应用中的Secret
- 企业ID：对应“我的企业”中的企业ID
- 推送用户列表：如推送给所有人可以填写 @all，多个接收者用‘|’分隔；具体id可以在企业微信管理后台的通讯录中找到。

![](./images/cp7.webp)
 
#### 三、代理地址和可信IP设置
1. 自有服务器

最简单的方式在自有服务器上运行docker容器，请预期安装好docker环境。\
容器启动命令：`docker run -d -p 9000:9000 --restart=unless-stopped --name cp-agent pushplus/cp-agent:latest`\
考虑到国内dockerhub无法正常访问下载，提供了离线镜像文件，下载后解压缩.zip，然后使用`docker load -i cp-agent.tar`命令来导入镜像。\
启动后：企业微信可信IP中填写自有服务器的ip地址；pushplus企业微信应用设置中代理地址填写 自有服务器ip:9000

离线镜像文件下载地址：<a href="https://pan.baidu.com/s/1Z2pYgl7BZ9_l1nGtHrPqjA?pwd=byus" target="_blank">https://pan.baidu.com/s/1Z2pYgl7BZ9_l1nGtHrPqjA?pwd=byus</a>

2. 使用腾讯云函数
1) 访问<a href="https://console.cloud.tencent.com/scf/list" target="_blank">腾讯云函数</a>，开通并新建一个函数。

![](./images/1.png)

2) 选择“从头开始”，函数类型选择“Web函数”，运行环境选择“Nodejs 18.15”

![](./images/2.png)

3) 函数代码中，修改“app.js”填入以下代码：
```
const gateway = require('fast-gateway')
const port = 9000;
gateway({
    routes: [{
      prefix: '/cgi-bin',
      prefixRewrite: '/cgi-bin',
      target: 'https://qyapi.weixin.qq.com'
    }]
}).start(port).then(server => {
    console.log(`agent server started on port ${port}`)
})
```

![](./images/32.png)

4)  函数代码中，修改“package.json”填入以下代码：
```
{
  "name": "perk-cp-agent",
  "version": "1.0.0",
  "description": "企业微信发送消息代理服务",
  "main": "app.js",
  "scripts": {
    "start": "node ./bin/www"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "fast-gateway": "^3.4.7"
  }
}
```

![](./images/4.png)

5) 函数URL配置中勾选“公网访问”，然后点击完成。

![](./images/5.png)

6) 打开刚创建的函数服务，在“函数管理”—>“函数代码”中修改编辑器的“自动安装依赖”为打开状态。

![](./images/7.png)

7) 在“函数配置”中点击“编辑”

![](./images/6.png)

8) 在编辑界面中勾选“固定公网出口IP”，以此来获取公网IP。

![](./images/8.png)

9) 等待一会就会生成出来固定公网IP了。复制这个IP，填入到企业微信的可信IP中。

![](./images/9.png)
 
10) 点击“函数URL”，复制访问路径中的公网地址，填入到pushplus企业微信应用配置的代理地址中去。

![](./images/11.png)
 
11) 保存后，即可正常使用企业微信渠道来发送消息了。

#### 四、在我的企业->微信插件->微信扫码关注
　&emsp;&emsp;成功关注后就可以在微信中收到企业微信的消息了。

![](./images/cp8.webp)
 
#### 五、发送企业微信应用消息
　&emsp;&emsp;接口上需要额外使用到两个参数。channel参数，填写固定值cp；webhook参数，填写上一步配置中自己定义的应用编码。
　&emsp;&emsp;具体示例如下：
- 请求地址：http://www.pushplus.plus/send
- 请求方式：POST
- Content-Type: application/json
- 请求内容：
```
{
    "token":"{token}",
    "title":"标题",
    "content":"消息内容",
    "channel":"cp",
    "webhook":"自定义的应用编码"
}
```

#### 六、企业微信应用和企业微信机器人的差异
- 企业微信机器人利用的是群聊的功能，群聊本身是一种多对多的场景，所以用来接收推送消息并不纯粹，群成员多了以后会有很多干扰信息。
- 企业微信应用就跟微信公众号一样，仅处理下发消息，没有其他消息打扰。这也是pushplus比较推荐的一种方式。
- 相对的企业微信应用配置步骤相比机器人步骤较多一点，填写的参数更多一点，但是一次配置后体验上更加贴近于微信公众号。具体是使用机器人还是应用视大家情况而定。

- 如需要配置企业微信机器人，可以参考这篇文章：pushplus推送到企业微信机器人教程