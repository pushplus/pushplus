# 收不到消息如何排查？

**&emsp;&emsp;<font color=#FF0000>收不到消息不要着急，不一定是pushplus程序的问题！</font>** 

## 简单来说

- 直接访问官网上的“<a href="//www.pushplus.plus/use.html" target="_blank">额度说明</a>”页面，账户状态会直接返回可能的问题。
- 确保已完成<a href="http://verify.pushplus.plus/" target="_blank">实名认证</a>。未实名用户无法发送消息，也就收不到自己发的消息（但可接收别人发的消息）。
- 看响应报文，具体是什么问题在响应报文中会写。大部分原因就是请求次数的太多被限制了。
- 不知道怎么看响应报文的，官网上“发送消息”->“<a href="//www.pushplus.plus/log.html" target="_blank">最新的请求</a>”页面。里面有展示响应报文。
- 在官网<a href="//www.pushplus.plus/push1.html" target="_blank">试一试</a>功能中测试是否可以正常发送。如可正常发送，说明问题出在您使用的程序上。
- 可以提前<a href="//www.pushplus.plus/vip.html" target="_blank">开通会员</a>来增加更多请求次数。

## 展开来说

&emsp;&emsp;未实名的用户将会无法调用发送消息接口，请先完成<a href="http://verify.pushplus.plus/" target="_blank">实名认证</a>。

![](./images/v3.png)

&emsp;&emsp;发送消息接口有请求次数限制，可以在官网上的“<a href="//www.pushplus.plus/use.html" target="_blank">额度说明</a>”中查看。

![](./images/limit.png)
 
&emsp;&emsp;在<a href="//www.pushplus.plus/push1.html" target="_blank">pushplus官网</a>上手动发送消息测试是否可以正常收到。如果可以正常收到消息，那么就说明pushplus在正常提供服务，没有问题。 

![](./images/l2.png)

&emsp;&emsp;如果没有收到消息或者直接提示错误，请查看响应内容，响应报文中会直接返回具体错误的原因，排查是否是超过发送限制了。如提示系统异常等错误，请联系官方，我们将第一时间进行处理。

![](./images/l1.png)

为了方便排查官网在“发送消息”->“<a href="//www.pushplus.plus/log.html" target="_blank">最新请求</a>”页面列出了24小时内的最新的一次请求记录。里面展示了请求参数和响应报文，可以根据响应报文的具体错误内容去自行处理。

![最新请求](./images/news.png)

&emsp;&emsp;当pushplus服务正常，但是自己却收不到消息，那么请您重点排查下您写的程序是否正常。重点排查下token是否正确，请求的报文参数是否与文档相符。如是使用的第三方提供的程序，请联系第三方开发者进行排查！pushplus官方不对第三方程序提供技术支持。 \
&emsp;&emsp;在公众号菜单中->"功能"->"<a href="//www.pushplus.plus/m/settings" target="_blank">消息开关</a>"中排查是否禁用了“接收消息”选项。 

![](./images/l3.jpg)

&emsp;&emsp;对于调用接口上的问题，如需要联系pushplus作者，请提供您的请求报文和响应报文，方便快速排查。 \
&emsp;&emsp;如果您根本不知道什么请求报文，请求地址，那么说明您只是在使用第三方开发好的程序，碰到问题请与第三方开发者联系~