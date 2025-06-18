# 消息回调说明

## 使用说明
&nbsp;&nbsp;&nbsp;&nbsp;pushplus提供了三个事件的回调，分别是消息回调、群组新增用户回调、新增好友回调。配置后会在触发事件的时候，把内容回调到配置的地址上。\
&nbsp;&nbsp;&nbsp;&nbsp;也就是当发送消息真正推送完成的时候（而不是请求接口同步返回成功，请求返回的成功只是代表服务端收到了推送的请求，排队等待推送，而推送完成后才叫是真正的推送完成），服务端会主动的发送一个请求给到用户，用户可以根据请求的来自行处理业务逻辑。比如判断是否推送成功，从而是否进行重新推送。

## 回调设置
&nbsp;&nbsp;&nbsp;&nbsp;在公众号“pushplus 推送加”的菜单“功能”->“个人中心”->"功能设置"->"回调地址"，可以设置接收回调消息的地址。

## 回调内容
&nbsp;&nbsp;&nbsp;&nbsp;如请求时带有callbackUrl参数，异步发送消息完成后将会发送一个post请求到回调地址上。

#### 消息完成回调post请求的body内容如下：
```
{
	"event": "message_complate",  //回调事件名称;message_complate - 消息完成，add_topic_user - 群组新增用户，add_friend - 新增好友
	"messageInfo": {
		"message": "",  //推送错误内容（如有）
		"shortCode": "88*********50fe",  //消息流水号
		"sendStatus": 2  //发送状态；0-未发送，1-发送中，2-发送成功，3-发送失败
	}
}
```

#### 群组新增用户回调的body内容如下：
```
{
	"event": "add_topic_user",  //回调事件名称;message_complate - 消息完成，add_topic_user - 群组新增用户，add_friend - 新增好友
	"topicUserInfo": {
		"id": 25,     //新增用户编号
		"openId": "oEdHX******aWDg", //新增用户OpenId
		"topicId": 2,   //群组编号
		"userSex": 1,   //性别
		"isFollow": 1,  //是否关注微信公众号
		"nickName": "陈大人",  //昵称
		"havePhone": 1,   //是否绑定手机
		"topicCode": "123",  //群组编码
		"topicName": "123",  //群组名称
		"headImgUrl": "https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIO******Luew/132",  //头像
		"emailStatus": 2  //是否绑定邮箱
	}
}
```

#### 新增好友回调的body内容如下：
```
{
	"event": "add_friend",  //回调事件名称;message_complate - 消息完成，add_topic_user - 群组新增用户，add_friend - 新增好友
    "qrCode": "自定义参数",  //自定义二维码参数
	"friendInfo": {
		"token": "5709******ddf",  //好友令牌
		"friendId": 5,      //好友Id
		"isFollow": 1,       //是否关注微信公众号
		"nickName": "",      //好友昵称
		"havePhone": 0,      //是否绑定手机
		"createTime": "2022-09-23 17:02:21", //创建时间
		"emailStatus": 0     //是否绑定邮箱
	}
}
```