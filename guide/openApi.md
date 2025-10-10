# pushplus 开放接口文档 V1.6

> 1.6 接口更新日期：2025-10-10\
> 增加浏览器插件转发设置接口
>
> 1.5 接口更新日期：2025-05-09\
> 增加消息token相关接口\
> 增加预处理信息相关接口
>
> 1.4 接口更新日期：2024-04-23\
> 群组二维码支持自定义有效期
>
> 1.3.1 接口更新日期：2023-01-30\
> 获取群组内用户接口增加关注群组时间字段
>
> 1.3 接口更新日期：2022-09-17\
> 渠道配置接口增加公众号、企业微信、邮件相关接口；\
> 增加查询当日消息接口请求次数接口；\
> 增加修改消息打开方式接口；\
> 优化群组相关接口
>
> 1.2 接口更新日期：2022-09-10\
> 增加开发\禁用发送消息接口
>
> 1.1 接口更新日期：2022-09-05\
> 增加好友功能相关接口
>
> 1.0 接口更新日期：2021-12-21\
> 通过accessKey调用消息、用户、群组、渠道配置和功能设置接口

[[toc]]

## 文档说明
&nbsp;&nbsp;&nbsp;&nbsp;为了更方便的让用户使用pushplus功能，现将原本需要在界面上操作的功能开放出来，包括消息、用户、群组、设置等能力。原本发送消息的接口是通过用户token来调用的，考虑到这种方式安全性较低，容易泄露，所以本次开放的接口采用AccessKey的校验方式。在请求接口的时候，需要在header中带上key名为“access-key”的内容，否则会请求失败。

&nbsp;&nbsp;&nbsp;&nbsp;由于开放接口权限较高，泄露后会给用户造成严重后果，所以默认是禁用状态，需要用户手动的在开发设置中开启，并在调用AccessKey接口之前配置好secretKey和安全IP地址。

## 一. 获取AccessKey
### 1. 使用说明
&nbsp;&nbsp;&nbsp;&nbsp;AccessKey是开放接口的全局唯一的接口调用凭证，调用其他各接口都需要使用AccessKey。开发者需要进行妥善保存。AccessKey的存储至少要保留32个字符空间。AccessKey的有效期目前为2个小时，需定时刷新，重复获取将导致上次获取的AccessKey失效。

pushplus的开放接口调用所需的AccessKey的使用及生成方式说明：
1. 用户需要提前配置自己的secretKey，建议至少32位数字、英文大小写随机组合。将请求的服务器IP添加到安全IP列表中。接口使用的token同发送消息的token。

2. 建议第三方开发者使用中控服务器统一获取和刷新AccessKey，其他业务逻辑服务器所使用的AccessKey均来自于该中控服务器，不应该各自去刷新，否则容易造成冲突，导致AccessKey覆盖而影响业务；

3. 目前AccessKey的有效期通过返回的expireIn来传达，目前是7200秒之内的值。中控服务器需要根据这个有效时间提前去刷新新AccessKey。在刷新过程中，中控服务器可对外继续输出的老AccessKey，此时pushplus后台会保证在5分钟内，新老AccessKey都可用，这保证了第三方业务的平滑过渡；

4. AccessKey的有效时间可能会在未来有调整，所以中控服务器不仅需要内部定时主动刷新，还需要提供被动刷新AccessKey的接口，这样便于业务服务器在API调用获知AccessKey已超时的情况下，可以触发AccessKey的刷新流程。

5. 对于可能存在风险的调用，在开发者进行获取AccessKey调用时请求的服务器需要在用户设置的安全IP列表内，否则会返回编码为403的错误。

### 2. 接口调用说明
- 请求地址：https://www.pushplus.plus/api/common/openApi/getAccessKey
- 请求方式：POST
- 请求参数:
```
{
  "token": "d90******c20",
  "secretKey": "qLc******gdk"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
token | 是 | 无 | 用户token。不支持使用消息token
secretKey |  是 | 无 | 用户密钥

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "accessKey": "d7b******62f",
    "expiresIn": 7200
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
accessKey | 字符串 | 访问令牌，后续请求需加到header中
expiresIn | 数字 | 过期时间，过期后需要重新获取
 
 
## 二. 消息接口
### 1. 消息列表
- 请求地址：https://www.pushplus.plus/api/open/message/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 8,
    "pages": 1,
    "list": [
      {
        "topicName": "",
        "messageType": 1,
        "title": "XXX",
        "shortCode": "a01***648",
        "channel": "wechat",
        "updateTime": "2021-12-08 20:19:02"
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 消息列表

- 消息列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
channel | 字符串 | 消息发送渠道；<br/>wechat-微信公众号,mail-邮件,cp-企业微信应用,webhook-第三方webhook
messageType | 数字 | 消息类型;1-一对一消息,2-一对多消息
shortCode | 字符串 | 消息短链码;可用于查询消息发送结果
title | 字符串 | 消息标题
topicName | 字符串 | 群组名称，一对多消息才有值
updateTime | 日期 | 更新日期

### 2. 查询消息发送结果
- 请求地址：https://www.pushplus.plus/api/open/message/sendMessageResult?shortCode=a018***648
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
shortCode | 是 | 无 | 消息短链码

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "status": 2,
    "errorMessage": "",
    "updateTime": "2021-12-08 12:19:02"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
status | 数字 | 消息投递状态；0-未投递，1-发送中，2-已发送，3-发送失败
errorMessage | 字符串 | 发送失败原因
updateTime | 日期 | 更新时间


## 三. 用户接口
### 1. 获取用户token
- 请求地址：https://www.pushplus.plus/api/open/user/token
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数：无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "604******f0b"
}
```
- 响应内容说明

data中直接返回当前用户token。

### 2. 个人资料详情
- 请求地址：https://www.pushplus.plus/api/open/user/myInfo
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数，url传参
- 请求参数：无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "openId": "o0a******A3Y",
    "unionId": "oGV******NZg",
    "nickName": "陈大人",
    "headImgUrl": "http://thirdwx.qlogo.cn/mmopen/ajNV***gg/132",
    "userSex": 1,
    "token": "604******f0b",
    "phoneNumber": "13******4",
    "email": "admin@xxx.com",
    "emailStatus": 1,
    "birthday": "1990-01-01",
    "points": 2
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
openId | 字符串 | 用户微信的openId
unionId | 字符串 | 用户微信的unionId
nickName | 字符串 | 昵称
headImgUrl | 字符串 | 头像
userSex | 数字  | 性别；0-未设置，1-男，2-女
token | 字符串 | 用户令牌 
phoneNumber | 字符串 | 手机号
email |字符串 | 邮箱 
emailStatus | 数字 | 邮箱验证状态；0-未验证，1-待验证，2-已验证
birthday | 日期 | 生日
points | 数字 | 用户积分

### 3. 获取解封剩余时间
- 请求地址：https://www.pushplus.plus/api/open/user/userLimitTime
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "sendLimit": 1,
    "userLimitTime": ""
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
sendLimit | 数字 | 发送限制状态;1-无限制，2-短期限制，3-永久限制
userLimitTime | 字符串 | 解封时间

### 4. 查询当日消息接口请求次数
- 请求地址：https://www.pushplus.plus/api/open/user/sendCount
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "wechatSendCount": 283,
    "cpSendCount": 0,
    "webhookSendCount": 19,
    "mailSendCount": 0
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
wechatSendCount | 数字 | 微信公众号渠道请求次数
cpSendCount | 数字 | 企业微信应用渠道请求次数
webhookSendCount | 数字 | webhook渠道请求次数
mailSendCount | 数字 | 邮件渠道请求次数

## 四. 消息token接口
### 1. 获取消息token列表
- 请求地址：https://www.pushplus.plus/api/open/token/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 0,
  "pageSize": 0,
  "params": {}
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 3,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "name": "pushplus",
        "expireTime": "2035-05-09 20:44:00",
        "token": "837******46e2"
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 消息token列表

- 消息token列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 消息token编号
name | 字符串 | 令牌名称
expireTime | 日期 | 过期时间
token | 字符串 | 消息token

### 2. 新增消息token
- 请求地址：https://www.pushplus.plus/api/open/token/add
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "name": "pushplus",
  "expireTime": "2035-05-09 22:34:00"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
name | 是 | 无 | 令牌名称
expireTime | 否 | '2999-12-31' | 过期时间

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": "837******46e2"
}
```
- 响应内容说明

data中返回新建的消息token。

### 3. 修改消息token
- 请求地址：https://www.pushplus.plus/api/open/token/edit
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1,
  "name": "pushplus",
  "expireTime": "2035-05-09 22:34:00"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | webhook编号
name | 是 | 无 | 令牌名称
expireTime | 否 | '2999-12-31' | 过期时间

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "修改成功"
}
```

### 4. 删除消息token
- 请求地址：https://www.pushplus.plus/api/open/token/deleteToken?id=1
- 请求方式：DELETE
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 消息token编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "删除成功"
}
```

## 五. 群组接口
### 1. 群组列表
- 请求地址：https://www.pushplus.plus/api/open/topic/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 0,
  "pageSize": 0,
  "params": {
    "topicType": 0
  }
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50
topicType | 是 | 0 | 群组类型;0-我创建的，1-我加入的 

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 3,
    "pages": 1,
    "list": [
      {
        "topicId": 4,
        "topicCode": "群组编码",
        "topicName": "群组名称",
        "nickName": "所属微信公众号名称",
        "createTime": "2021-12-24 01:19:15"
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 群组列表

- 群组列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
topicId | 数字 | 群组编号
topicCode | 字符串 | 群组编码
topicName | 字符串 | 群组名称
nickName | 字符串 | 所属微信公众号名称
createTime | 日期 | 创建时间

### 2. 获取我创建的群组详情
- 请求地址：https://www.pushplus.plus/api/open/topic/detail?topicId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicId | 是 | 无 | 群组编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "topicId": 1,
    "topicName": "测试",
    "topicCode": "123456",
    "qrCodeImgUrl": "",
    "contact": "联系方式",
    "introduction": "群组简介",
    "receiptMessage": "关注后回复",
    "nickName": "所属微信公众号名称",
    "createTime": "2021-02-10 16:58:01",
    "topicUserCount": 1
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
topicId | 数字 | 群组编号 
topicCode | 字符串 | 群组编码
topicName | 字符串 | 群组名称
qrCodeImgUrl | 字符串 | 永久二维码图片地址
contact | 字符串 | 联系方式
introduction | 字符串 | 群组简介 
receiptMessage | 字符串 | 加入后回复内容
nickName | 字符串 | 所属微信公众号名称
createTime | 日期 | 创建时间
topicUserCount | 字符串 | 群组订阅人总数

### 4. 获取我加入的群详情
- 请求地址：https://www.pushplus.plus/api/open/topic/joinTopicDetail?topicId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicId | 是 | 无 | 群组编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "topicName": "群组名称",
    "topicCode": "123456",
    "topicId": 2, 
    "contact": "联系方式",
    "introduction": "群组简介", 
    "nickName": "所属微信公众号名称",
    "createTime": "2021-03-29 20:11:50"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
topicId | 数字 | 群组编号
topicCode | 字符串 | 群组编码
topicName | 字符串 | 群组名称
contact | 字符串 | 联系方式
introduction | 字符串 | 群组简介  
nickName | 字符串 | 所属微信公众号名称
createTime | 日期 | 加入时间

### 5. 新增群组
- 请求地址：https://www.pushplus.plus/api/open/topic/add
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "topicCode": "pushplus",
  "topicName": "推送加",
  "contact": "联系方式",
  "introduction": "群组简介",
  "receiptMessage": "关注后回复",
  "appId": "微信公众号Id"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicCode | 是 | 无 | 群组编码
topicName | 是 | 无 | 群组名称
contact | 是 | 无| 联系方式
introduction | 是 | 无| 群组简介
receiptMessage | 否 | 无| 加入后回复内容
appId | 否 | 无| 微信公众号Id；填写绑定后的公众号Id，默认使用pushplus公众号

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": 2
}
```
- 响应内容说明

data中返回新建群组的群组编号。

### 6. 获取群组二维码
- 请求地址：https://www.pushplus.plus/api/open/topic/qrCode?topicId=1&second=2592000
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicId | 是 | 无 | 群组编号
second | 否 | 无 | 二维码有效期（单位秒）；不传默认30天，最长30天。

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "qrCodeImgUrl": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQ******cA",
    "forever": 0
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
qrCodeImgUrl | 数字 | 群组二维码图片路径
forever | 字符串 | 二维码类型；0-临时二维码，1-永久二维码 

### 7. 退出群组
- 请求地址：https://www.pushplus.plus/api/open/topic/exitTopic?topicId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicId | 是 | 无 | 群组编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "退订成功"
}
```
 
## 六. 群组用户接口
### 1. 获取群组内用户
- 请求地址：https://www.pushplus.plus/api/open/topicUser/subscriberList
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20,
  "params": {
    "topicId": 1
  }
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50
topicId | 是 | 0 | 群组编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 1,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "nickName": "昵称",
        "openId": "o0a******wZo",
        "headImgUrl": "http://thirdwx.qlogo.cn/mmopen/Q3a******32",
        "userSex": -1,
        "havePhone": 0,
        "isFollow": 1,
        "emailStatus": 0,
        "followTime": "2022-04-15 09:47:25",
        "remark": "备注内容"
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 用户列表

- 用户列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 用户编号；可用于删除用户
nickName | 字符串 | 昵称
openId | 字符串 | 用户微信openId
headImgUrl | 字符串 | 头像url地址
userSex | 数字 | 性别；0-未设置，1-男，2-女
havePhone | 数字 | 是否绑定手机；0-未绑定，1-已绑定
isFollow | 数字 | 是否关注微信公众号；0-未关注，1-已关注
emailStatus | 数字 | 邮箱验证状态；0-未验证，1-待验证，2-已验证
followTime | 日期 | 关注群组时间
remark | 字符串 | 备注信息

### 2. 删除群组内用户
- 请求地址：https://www.pushplus.plus/api/open/topicUser/deleteTopicUser?topicRelationId=1
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicRelationId | 是 | 无 | 用户编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "删除成功"
}
```

## 七. 渠道配置接口
### 1. 获取webhook列表
- 请求地址：https://www.pushplus.plus/api/open/webhook/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 5,
    "pages": 1,
    "list": [
      {        
        "id": 1,
        "webhookCode": "pushplus",
        "webhookName": "webhook推送",
        "webhookType": 1,
        "webhookUrl": "url",
        "createTime": "2021-12-23 09:00:56",
      }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | webhook列表

- webhook列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | webhook编号
webhookCode | 字符串 | webhook编码
webhookName | 字符串 | webhook名称
webhookType | 数字 | webhook类型；1-企业微信，2-钉钉，3-飞书，4-server酱
webhookUrl | 字符串 | 调用的url地址
createTime | 日期 | 创建日期

### 2. webhook详情
- 请求地址：https://www.pushplus.plus/api/open/webhook/detail?webhookId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
webhookId | 是 | 无 | webhook编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 1,
    "webhookName": "推送加",
    "webhookCode": "pushplus",
    "webhookUrl": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=63******8f",
    "webhookType": 1,
    "createTime": "2021-12-23 09:00:56"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | webhook编号
webhookCode | 字符串 | webhook编码
webhookName | 字符串 | webhook名称
webhookType | 数字 | webhook类型；1-企业微信，2-钉钉，3-飞书，4-server酱
webhookUrl | 字符串 | 调用的url地址
createTime | 日期 | 创建日期

### 3. 新增webhook
- 请求地址：https://www.pushplus.plus/api/open/webhook/add
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "webhookCode": "pushplus",
  "webhookName": "推送加",
  "webhookType": 1,
  "webhookUrl": "url"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
webhookCode | 是 | 无 | webhook编码
webhookName | 是 | 无 | webhook名称
webhookType | 是 | 无| webhook类型；1-企业微信，2-钉钉，3-飞书，4-server酱
webhookUrl | 是 | 无| 调用的url地址

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": 2
}
```
- 响应内容说明

data中返回新建webhook编号。

### 4. 修改webhook配置
- 请求地址：https://www.pushplus.plus/api/open/webhook/edit
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1,
  "webhookCode": "pushplus",
  "webhookName": "企业微信",
  "webhookType": 1,
  "webhookUrl": "https://url"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | webhook编号
webhookCode | 是 | 无 | webhook编码
webhookName | 是 | 无 | webhook名称
webhookType | 是 | 无| webhook类型；1-企业微信，2-钉钉，3-飞书，4-server酱
webhookUrl | 是 | 无| 调用的url地址

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "修改成功"
}
```

### 5. 获取微信公众号渠道列表
- 请求地址：https://www.pushplus.plus/api/open/mp/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 5,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "nickName": "pushplus",
        "headImg": "http://wx.qlogo.cn/mmopen/zsQMENgVFAoAPTW/0",
        "principalName": "主体公司名称",
        "authorizationAppid": "wx3b5738bdds3c180",
        "funcInfo": "1,2,3,4,6,7,9,11,15,23,24,27,33,54,66,89,",
        "serviceType": 2,
        "verifyType": 0,
        "alias": "pushplus",
        "updateTime": "2022-08-24 11:50:40"
		  }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 公众号列表

- 公众号列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 微信公众号编号
nickName | 字符串 | 微信公众号名称
headImg | 字符串 | 微信公众号头像
principalName | 字符串 | 公众号的主体名称
authorizationAppid | 字符串 | 授权方appid
funcInfo | 字符串 | 权限集列表
serviceType | 数字 | 授权方公众号类型，0代表订阅号，1代表由历史老帐号升级后的订阅号，2代表服务号
verifyType | 数字 | 授权方认证类型，-1代表未认证，0代表微信认证
alias | 字符串 | 公众号所设置的微信号
updateTime | 日期 | 更新时间

### 6. 获取企业微信应用渠道列表
- 请求地址：https://www.pushplus.plus/api/open/cp/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 5,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "cpName": "企业微信应用名称",
        "cpCode": "c001"
		  }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 企业微信应用列表

- 企业微信应用列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 企业微信应用编号
cpName | 字符串 | 企业微信应用名称
cpCode | 字符串 | 企业微信应用编码

### 7. 获取邮箱渠道列表
- 请求地址：https://www.pushplus.plus/api/open/mail/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 5,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "mailName": "pushplus邮箱",
        "mailCode": "pushplus"
		  }
    ]
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 邮箱列表

- 邮箱列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 邮箱编号
mailName | 字符串 | 邮箱名称
mailCode | 字符串 | 邮箱编码

### 8. 邮箱渠道详情
- 请求地址：https://www.pushplus.plus/api/open/mail/detail?mailId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
mailId | 是 | 无 | 邮箱编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 1,
    "mailName": "推送加",
    "mailCode": "pushplus",
    "account": "admin@pushplus.plus",
    "password": "passwd",
    "smtpServer": "smtp.163.com",
    "smtpSsl": 1,
    "smtpPort": 465,
    "createTime": "2021-12-23 09:00:56"
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 邮箱渠道编号
mailName | 字符串 | 邮箱渠道名称
mailCode | 字符串 | 邮箱渠道编码
account | 数字 | 邮箱账户
password | 字符串 | 邮箱密码
smtpServer | 字符串 | smtp服务器地址
smtpSsl | 数字 | 是否启用SSL；1-启用，0-不启用
smtpPort | 字符串 | smtp端口
createTime | 日期 | 创建日期

## 八. 功能设置接口
### 1. 获取默认发送渠道
- 请求地址：https://www.pushplus.plus/api/open/setting/getUserSettings
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无
- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "defaultChannel": "wechat",
    "defaultChannelTxt": "微信公众号",
    "defaultWebhook": "",
    "sendLimit": 0,
    "recevieLimit": 0,
    "sendType": 0,
    "isSend": 1,
    "showIp": 0
    "extension": 0
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
defaultChannel | 字符串 | 默认渠道编码
defaultChannelTxt | 字符串 | 默认渠道名称
defaultWebhook | 字符串 | 渠道参数
sendLimit | 数字 |发送限制；0-无限制，1-禁止所有渠道发送，2-限制微信渠道，3-限制邮件渠道
recevieLimit | 数字 |接收限制；0-接收全部，1-不接收消息
sendType | 数字 | 打开消息方式；0-H5，1-小程序
isSend | 数字 |是否启用发送消息功能；1-开启，0-关闭
showIp | 数字 |消息详情底部是否展示推送方的IP地址；1-显示，0不显示
extension | 数字 | 微信公众号渠道消息同步使用浏览器插件接收；1-开启，0-关闭

### 2. 修改默认发送渠道
- 请求地址：https://www.pushplus.plus/api/open/setting/changeDefaultChannel
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "defaultChannel": "wechat",
  "defaultWebhook": ""
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
defaultChannel | 是 | 无 | 默认渠道；wechat-微信公众号,mail-邮件,cp-企业微信应用,webhook-第三方webhook
defaultWebhook | 否 | 无 | 渠道参数；webhook和cp渠道需要填写具体的webhook编号或自定义编码

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

### 3. 修改接收消息限制
- 请求地址：https://www.pushplus.plus/api/open/setting/changeRecevieLimit?recevieLimit=0
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
recevieLimit | 是 | 无 | 接收消息限制；0-接收全部，1-不接收消息

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

### 4. 开启/关闭发送消息功能
- 请求地址：https://www.pushplus.plus/api/open/setting/changeIsSend?isSend=0
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
isSend | 是 | 无 | 发送消息功能；0-禁用，1-启用

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

### 5. 修改打开消息方式
- 请求地址：https://www.pushplus.plus/api/open/setting/changeOpenMessageType?openMessageType=0
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
openMessageType | 是 | 无 | 消息打开类型；0:H5，1:小程序

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

### 6. 修改浏览器插件转发
- 请求地址：https://www.pushplus.plus/api/open/setting/extension?forward=0
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
forward | 是 | 无 | 微信渠道消息是否同步浏览器插件接收；0:否，1:是

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

## 九. 好友功能接口
### 1. 获取个人二维码
- 请求地址：https://www.pushplus.plus/api/open/friend/getQrCode?appId=wx3b5738bdds3c180&content=123
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
appId | 否 | 无 | 微信公众号Id
content | 否 | 无 | 自定义参数，扫描后回调（可用于区分扫描渠道）

- 响应内容
```
{
  "code": 200,
  "data": {
    "qrCodeImgUrl": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQHZ7zwAA******hZjAwQAjScA"
  },
  "msg": "执行成功"
}
```

### 2. 获取好友列表
- 请求地址：https://www.pushplus.plus/api/open/friend/list
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "data": {
    "list": [
      {
        "id": 4,
        "friendId": 1322,
        "token": "f6bd32c07******a076f2e89aed4e92",
        "headImgUrl": "",
        "nickName": "昵称",        
        "emailStatus": 0,        
        "havePhone": 0,               
        "isFollow": 1,        
        "remark": "备注",
        "createTime": "2022-09-06 11:15:32"
      }
    ],
    "pageNum": 1,
    "pageSize": 1,
    "pages": 1,
    "total": 10
  },
  "msg": "执行成功"
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 好友列表

- 好友列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 好友编号
token | 字符串 | 好友令牌；发送好友消息使用
headImgUrl | 字符串 | 好友头像
nickName | 字符串 | 好友昵称
isFollow | 数字 | 是否关注微信公众号；0-未关注，1-已关注
havePhone | 字符串 |是否绑定手机；0-未绑定，1-已绑定
emailStatus | 数字 | 邮箱验证状态；0-未验证，1-待验证，2-已验证
remark | 字符串 | 备注
friendId | 数字 | 好友id
createTime | 日期 | 创建日期


### 3. 删除好友
- 请求地址：https://www.pushplus.plus/api/open/friend/deleteFriend?friendId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
friendId | 是 | 无 | 好友id

- 响应内容
```
{
  "code": 200, 
  "data": null,
  "msg": "执行成功"
}
```

### 4. 修改好友备注
- 请求地址：https://www.pushplus.plus/api/open/friend/editRemark
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 
```
{
  "id": 0,
  "remark": "备注"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 好友编号
remark |  是 | 无 | 好友备注

- 响应内容
```
{
  "code": 200, 
  "data": null,
  "msg": "执行成功"
}
```

## 十. 预处理信息接口
注：预处理信息需开通会员才能使用

### 1. 获取预处理信息列表
- 请求地址：https://www.pushplus.plus/api/open/pre/list
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 20
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize |  否 | 20 | 每页大小，最大值为50

- 响应内容
```
{
  "code": 200,
  "data": {
    "list": [
      {
         "id": 1,
         "preName": "test",
         "preCode": "test",
         "contentType": 1,
         "createTime": "2025-04-28 14:08:35"
      }
    ],
    "pageNum": 1,
    "pageSize": 1,
    "pages": 1,
    "total": 10
  },
  "msg": "执行成功"
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
pageNum | 数字 | 当前页码
pageSize | 数字 | 分页大小
total | 数字 | 总行数
pages | 数字 | 总页数
list | 数组 | 预处理信息列表

- 预处理信息列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 预处理信息编号
preName | 字符串 | 预处理信息名称
preCode | 字符串 | 预处理信息编码
contentType | 字符串 | 编程语言；1-JavaScript
createTime | 日期 | 创建日期 

### 2. 预处理信息详情
- 请求地址：https://www.pushplus.plus/api/open/pre/detail?preId=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
preId | 是 | 无 | 预处理信息编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": {
    "id": 11,
    "preName": "test",
    "preCode": "test",
    "contentType": 1,
    "content": "content = content + 123",
  }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 预处理信息编号
preName | 字符串 | 预处理信息名称
preCode | 字符串 | 预处理信息编码
contentType | 字符串 | 编程语言类型；1-JavaScript
content | 字符串 | 预处理代码 

### 3. 新增预处理信息
- 请求地址：https://www.pushplus.plus/api/open/pre/add
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
	"content": "content = content + 123",
	"preName": "test",
	"preCode": "test",
	"contentType": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
content | 是 | 无 | 预处理代码
preName | 是 | 无 | 预处理名称
preCode | 是 | 无| 预处理编码
contentType | 是 | 无| 编程语言类型；1-JavaScript

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": 1
}
```

### 4. 修改预处理信息
- 请求地址：https://www.pushplus.plus/api/open/pre/edit
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1,
	"content": "content = content + 123",
	"preName": "test",
	"preCode": "test",
	"contentType": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 预处理信息编号
content | 是 | 无 | 预处理代码
preName | 是 | 无 | 预处理名称
preCode | 是 | 无| 预处理编码
contentType | 是 | 无| 编程语言类型；1-JavaScript

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "修改成功"
}
```

### 5. 删除预处理信息
- 请求地址：https://www.pushplus.plus/api/open/pre/delete?preId=1
- 请求方式：DELETE
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
preId | 是 | 无 | 好友id

- 响应内容
```
{
  "code": 200, 
  "data": "删除成功",
  "msg": "执行成功"
}
```

### 6. 测试预处理代码
- 请求地址：https://www.pushplus.plus/api/open/pre/test
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
	"content": "content = content + 123",
	"contentType": 1,
  "message": "this is content"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
content | 是 | 无 | 预处理代码
contentType | 是 | 无| 编程语言类型；1-JavaScript
message | 是 | 无 | 测试消息内容

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "this is content123"
}
```

- 响应内容说明

data中返回预处理后的消息内容。