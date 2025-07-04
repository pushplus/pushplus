# 预处理信息配置

## 一. 场景说明
　&emsp;&emsp;有一些场景消息内容是第三方返回的，无法直接修改。比如阿里云监控报警，仅是配置一个webhook的地址。但是又想自己对消息内容进行微调修改。原本做法需要自己写一段逻辑，先webhook到自己程序的地址上，然后处理好以后在服务端请求pushplus的发送消息接口。一是需要自行开发，二是还需要有服务器进行部署。为了方便处理这种场景，新增加了一个预处理(pre)的字段，可提前在页面上配置对消息内容的处理代码，发送消息的时候直接带上编码参数即可。相当于把原本自己编码的逻辑放在pushplus服务器上，在发消息的时候一并给处理了。

　&emsp;&emsp;当然这么强大的功能还是有一些限制的。

- 1. 仅提供会员使用。
- 2. 对于脚本代码性能上有所限制，防止死循环、异常逻辑、挖矿等恶意行为。
- 3. 暂时支持原生JavaScript语言。

## 二. 配置操作
配置之前请确保您已经开通会员。在"我的"-> "个人中心" -> "预处理信息" 中新增一条预处理信息。

![](../images/pre3.png)
 
- 预处理名称：方便用户自己查看的，随便定义。
- 预处理编码：在发送消息接口中有一个pre字段，就需要填写这个值。用户自定义。
- 预处理代码：针对消息内容的处理代码逻辑。

![](../images/pre4.png)
 
在填写完成以后，可以点击测试按钮来检测编写的预处理代码是否有问题。\
在弹框中的消息内容填写原本收到的消息内容，然后点击确认后会看到预处理代码执行后的结果。如有报错也会显示在结果框内。

![](../images/pre1.png)
 
## 三. 预处理代码示例
代码中内置了一个全局上下文变量content，这个变量来指代“消息内容”。所以你要改变消息内容就需要重新给这个变量赋值。

### 1. 重新自定义消息内容
```
content = '新定义的消息内容'
```

### 2. 追加内容
```
content += '追加的内容'
```

### 3. 替换内容
```
//把消息内容中的a替换成b

content = content.replace('a','b')
```

### 4. 正则表达式
```
//验证消息内容是否是手机号码，返回true或false

const regex = /^1[3-9]\d{9}$/;
content = regex.test(content).toString();
```

## 三. 发送消息中使用
### 1. 官网“试一试”中使用
可以直接在官网的 “发消息”-> "一对一消息" -> "试一试"中。预处理编码下拉框中选择之前录入好的信息，点击发送即可。

![](../images/pre6.png)


### 2. 发送消息接口中使用
发送消息接口中新增了pre参数，只需要将预处理编码填到pre字段中即可。以下示例，其中appendMsg就是用户自定义的预处理编码。

- 请求地址：http://www.pushplus.plus/send
- 请求方式：POST
- 请求内容：

```
{
    "token":"{token}",
    "title":"这是标题",
    "content":"消息内容正文",
    "pre": "appendMsg"
}
```

![](../images/pre5.jpg)

可以看到收到的消息内容已经追加，并不是接口报文中的content字段内容了。