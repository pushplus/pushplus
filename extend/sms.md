# 短信渠道使用说明

## 一、使用说明
1. 使用短信渠道推送消息需要消息的接收方配置好自己的手机号码，否则将无法推送消息。
2. 在一对多的群组中只会推送给已配置手机号码的用户，未配置的用户无法收到。
3. 短信功能需要收费使用，1条短信需要10积分（0.1元）。注意：一对多消息群组中有多人接收的按多条计算，不会只按一条计费！
4. 为了防止用户被垃圾短信的骚扰，运营商会对每日相同内容的短信进行屏蔽，请勿重复发送相同标题和内容的短信消息。
5. 短信本身有字数限制，故只会显示标题，不展示消息内容。

![](../images/sms3.jpg)

## 二、扣费说明
1. 每推送一条短信会扣减10积分，会提前判断账户中积分是否足够抵扣，如果积分不足将会发送失败。
2. 短信发送失败，如因为手机号码异常等其他短信通道原因造成的失败，将会自动退还消费的积分。由于短信发送会有延迟，退还时间会有相应的延迟周期。
3. 推送一对多消息，因为是多人，群发给不同的手机号码，所以会按群组中用户数量进行扣减。不会只按照一条短信来扣费。
4. 短信有概率被手机安全软件定义为垃圾短信从而拦截，或者运营商进行了拦截。这些情况不属于未发送成功，不会退还积分。

## 三、手机号码配置方式
想要接收到短信渠道的消息，需要提前配置好自己的手机号码。
- 点击在“pushplus 推送加”公众号菜单里面的“功能”->“个人中心”。
- 在打开的“pushplus推送加”小程序中点击“个人资料”。\
![](../images/mail1.jpg)

- 在“个人资料”中点击“手机号”，打开绑定手机号页面。\
![](../images/sms1.png)

- 输入自己的“手机号码”和“图形验证码”，点击“发送验证码”，系统会发送一条验证码短信到手机上。\
![](../images/sms2.jpg)

- 填入接收到的短信验证码，点击“确认”即绑定完成。


## 四、接口请求示例
- 请求地址：http://www.pushplus.plus/send/{token}
- 请求方式：POST
- 请求内容：

```
{
    "token":"{token},
    "title":"短信标题",
    "content":"短信正文内容",
    "channel":"sms",
}
```
- 说明：短信本身有字数限制，故无法直接展示内容，只展示标题。

