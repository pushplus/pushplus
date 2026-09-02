# pushplus 开放接口文档 V1.17

::: details 点击展开版本更新日志

> 1.17 接口更新日期：2026-08-26\
> 增加QQ机器人渠道相关接口
>
> 1.16 接口更新日期：2026-08-17\
> 增加好友黑名单和群组订阅人黑名单相关接口
>
> 1.15 接口更新日期：2026-08-07\
> 个人资料详情接口返回会员信息和是否实名
>
> 1.14 接口更新日期：2026-05-09\
> 增加图片服务相关接口
>
> 1.13 接口更新日期：2026-04-14\
> 完善群组接口字段，增加群组修改相关接口
>
> 1.12 接口更新日期：2026-03-27\
> 增加微信ClawBot渠道相关接口
>
> 1.11 接口更新日期：2026-01-27\
> 群组二维码和个人二维码增加可扫码次数参数
>
> 1.10 接口更新日期：2025-12-08\
> 默认渠道接口修改，根据消息token来配置不同的默认渠道
>
> 1.9 接口更新日期：2025-12-01\
> 增加删除消息接口
>
> 1.8 接口更新日期：2025-11-23\
> 增加删除群组接口
>
> 1.7 接口更新日期：2025-11-18\
> webhook类型支持自定义\
> 默认渠道枚举完善
>
> 1.6 接口更新日期：2025-10-10\
> 增加插件转发设置接口
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

:::

::: details 点击查看目录

[[toc]]

:::

## 文档说明
&nbsp;&nbsp;&nbsp;&nbsp;为了更方便的让用户使用pushplus功能，现将原本需要在界面上操作的功能开放出来，包括消息、用户、群组、设置等能力。原本发送消息的接口是通过用户token来调用的，考虑到这种方式安全性较低，容易泄露，所以本次开放的接口采用AccessKey的校验方式。在请求接口的时候，需要在header中带上key名为“access-key”的内容，否则会请求失败。

&nbsp;&nbsp;&nbsp;&nbsp;由于开放接口权限较高，泄露后会给用户造成严重后果，所以默认是禁用状态，需要用户手动的在开发设置中开启，并在调用AccessKey接口之前配置好secretKey和安全IP地址。

&nbsp;&nbsp;&nbsp;&nbsp;推荐优先使用官方 [pushplus SDK](sdk.md)，而不是自行编写 HTTP 请求代码。SDK 已封装 AccessKey 刷新、发送频率控制、回调等常见场景，可降低开发成本和出错概率。如需了解接口参数，可参考下文接口说明。

## 接口在线测试页面
可以访问[https://api.pushplus.plus/doc-6905395](https://api.pushplus.plus/doc-6905395)，在线的测试接口。可以直接使用页面上生成的代码示例，支持多种语言。

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
channel | 字符串 | 消息发送渠道；<br/>wechat-微信公众号,mail-邮件,cp-企业微信应用,webhook-第三方webhook,qq-QQ机器人
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

### 3. 删除消息
注：删除后所有接收人均无法查看，且无法撤销。

- 请求地址：https://www.pushplus.plus/api/open/message/deleteMessage?shortCode=a018***648
- 请求方式：DELETE
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
  "msg": "请求成功"
}
```

### 4. 消息详情
- 请求地址：https://www.pushplus.plus/shortMessage/a018***648
- 请求方式：GET
- content-type: text/html;charset=UTF-8
- 请求参数，url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
a018***648 | 是 | 无 | 消息短链码,替换成发送消息同步返回的短链码

- 响应内容

消息内容html。不直接提供消息内容、标题、发送人等json格式的接口。

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
    "points": 2,
    "verifyStatus": 1,
    "vipInfo": {
      "isVip": 1,
      "lastDay": "2030-10-02"
    }
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
verifyStatus | 数字 | 实名状态：0-未实名，1-已实名
vipInfo | 对象 | 会员信息

- 会员信息对象说明

参数名称 | 类型 | 说明
---|--- | ---
isVip | 数字 | 是否会员；0-否，1-是
lastDay | 字符串 | 会员到期日


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
    "mailSendCount": 0,
    "qqBotSendCount": 0
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
qqBotSendCount | 数字 | QQ机器人渠道请求次数

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

### 5. 消息token下拉选择列表
- 请求地址：https://www.pushplus.plus/api/open/token/selectTokenList?type=0
- 请求方式：GET
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
type | 否 | 0 | 0-返回所有消息token；1-返回未配置默认推送渠道的消息token；

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": [
        {
            "id": 1,
            "name": "token1"
        },
        {
            "id": 2,
            "name": "token2"
        }
    ]
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 消息令牌编号
name | 字符串 | 消息令牌名称

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
        "icon": "群组图标地址",
        "topicId": 4,
        "topicCode": "群组编码",
        "topicName": "群组名称",
        "nickName": "所属微信公众号名称",
        "createTime": "2021-12-24 01:19:15",
        "topicUserCount": 1,
        "topicType": 2,
        "isApproved": 2,
        "firstIsApproved": 2,
        "approveReason": "审批拒绝理由",
        "isOpen": 1
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
icon | 字符串 | 群组图标
topicId | 数字 | 群组编号
topicCode | 字符串 | 群组编码
topicName | 字符串 | 群组名称
nickName | 字符串 | 所属微信公众号名称
createTime | 日期 | 创建时间
topicUserCount | 数字 | 群组订阅人总数
topicType |数字 | 群组类型；0普通群组；1积分群组；2公开群组
isApproved | 数字 | 是否审核通过；0未审核，1审核不通过，2审核通过
firstIsApproved |数字 | 创建时是否审核通过；0未审核，1审核不通过，2审核通过
approveReason | 字符串 | 审批拒绝理由
isOpen | 数字 | 是否上架(仅积分群组)；0否，1是

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
    "topicUserCount": 1,
    "icon": "群组图标地址",
    "appId": "服务号appId",
    "topicType": 2,
    "price": 0.00,
    "topicDescribe": "一句话介绍",
    "userNickName": "创建人昵称",
    "isApproved": 2,
    "firstIsApproved": 2,
    "approveReason": "审批拒绝理由",
    "isOpen": 1
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
icon | 字符串 | 群组图标
appId | 字符串 | 服务号appId
topicType |数字 | 群组类型；0普通群组；1积分群组；2公开群组
price | 数字 | 积分群组订阅积分；按月
topicDescribe | 字符串 | 一句话介绍
userNickName | 字符串 | 创建人昵称
isApproved | 数字 | 是否审核通过；0未审核，1审核不通过，2审核通过
firstIsApproved |数字 | 创建时是否审核通过；0未审核，1审核不通过，2审核通过
approveReason | 字符串 | 审批拒绝理由
isOpen | 数字 | 是否上架(仅积分群组)；0否，1是

### 3. 获取我加入的群详情
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
    "createTime": "2021-03-29 20:11:50",
    "icon": "群组图标",
    "topicUserCount": 1,
    "topicType": 1,
    "price": 100.00,
    "topicDescribe": "一句话介绍",
    "userNickName": "创建者昵称"
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
icon | 字符串 | 群组图标
topicUserCount| 数字 | 已订阅人数
topicType |数字 | 群组类型；0普通群组；1积分群组；2公开群组
price | 数字 | 积分群组订阅积分；按月
topicDescribe | 字符串 | 一句话介绍
userNickName | 字符串 | 创建人昵称

### 4. 新增群组
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
  "appId": "微信公众号Id",
  "icon": "群组图标",
  "topicType": 0,
  "price": 0,
  "topicDescribe": "一句话简介"
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
icon | 否  | 无 | 群组图标
topicType | 否 | 0 | 群组类型；0普通群组；1积分群组；2公开群组
price | 否 | 0.00 | 积分群组订阅积分；按月
topicDescribe | 否 | 无 | 一句话介绍

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

### 5. 修改群组
- 请求地址：https://www.pushplus.plus/api/open/topic/editTopic
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "topic": 1,
  "topicCode": "pushplus",
  "topicName": "推送加",
  "contact": "联系方式",
  "introduction": "群组简介",
  "receiptMessage": "关注后回复",
  "icon": "群组图标",
  "price": 0,
  "topicDescribe": "一句话简介"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topic | 是 | 无 | 群组编号
topicCode | 是 | 无 | 群组编码
topicName | 是 | 无 | 群组名称
contact | 否 | 无| 联系方式
introduction | 否 | 无| 群组简介
receiptMessage | 否 | 无| 加入后回复内容
icon | 否 | 无 | 群组图标
price | 否 | 0.00 | 积分群组订阅积分；按月
topicDescribe | 否 | 无 | 一句话介绍

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": "修改成功"
}
```

### 6. 获取群组二维码
- 请求地址：https://www.pushplus.plus/api/open/topic/qrCode?topicId=1&second=604800&scanCount=-1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicId | 是 | 无 | 群组编号
second | 否 | 604800 | 二维码有效期（单位秒）；不传默认7天，最长30天。
scanCount | 否 | -1 | 可扫码次数；范围1-999次，-1代表无限次

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

### 8. 删除群组
- 请求地址：https://www.pushplus.plus/api/open/topic/delete?topicId=1
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
  "data": "群组删除成功"
}
```

### 9. 上下架积分群组
- 请求地址：https://www.pushplus.plus/api/open/topic/isOpen
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "topic": 1,
  "isOpen": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topic | 是 | 无 | 群组编号
isOpen | 是 | 无 | 是否上架；1是，0否

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "操作成功"
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

### 3. 修改订阅人备注
- 请求地址：https://www.pushplus.plus/api/open/topicUser/editRemark
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1,
  "remark": "订阅人备注"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 用户编号
remark |  是 | 无 | 订阅人备注信息；20个字以内

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功"
}
```

### 4. 将订阅人加入黑名单
注：加入后将移出群组，对方无法再加入该群组。积分群组不支持黑名单。不能将自己加入黑名单。

- 请求地址：https://www.pushplus.plus/api/open/topicUser/addBlacklist?topicRelationId=1
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
topicRelationId | 是 | 无 | 用户编号（订阅人列表中的 id 字段）

- 响应内容
```
{
  "code": 200,
  "data": null,
  "msg": "执行成功"
}
```

### 5. 订阅人黑名单列表
- 请求地址：https://www.pushplus.plus/api/open/topicUser/blacklistList
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
topicId | 是 | 无 | 群组编号

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
        "userId": 1322,
        "nickName": "昵称",
        "openId": "o0a******wZo",
        "headImgUrl": "http://thirdwx.qlogo.cn/mmopen/Q3a******32",
        "createTime": "2026-08-17 10:00:00"
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
list | 数组 | 黑名单列表

- 黑名单列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 黑名单记录ID；解除黑名单时使用
userId | 数字 | 被拉黑用户ID
nickName | 字符串 | 昵称
openId | 字符串 | 用户微信openId
headImgUrl | 字符串 | 头像url地址
createTime | 日期 | 拉黑时间

### 6. 解除订阅人黑名单
注：解除后不会自动恢复群组订阅，对方可重新加入该群组。

- 请求地址：https://www.pushplus.plus/api/open/topicUser/removeBlacklist?id=1
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 黑名单记录ID（黑名单列表中的 id 字段）

- 响应内容
```
{
  "code": 200,
  "data": null,
  "msg": "执行成功"
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
        "webhookTypeName": "企业微信机器人",
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
webhookType | 数字 | webhook类型；1-企业微信机器人，2-钉钉机器人，3-飞书机器人，4-Server酱，50-bark，6-企业微信应用，7-腾讯轻联，8-IFTTT，9-集简云，10-Gotify，11-WxPusher，12-自定义
webhookTypeName | 字符串 | webhook类型名称
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
    "webhookTypeName": "企业微信机器人",
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
webhookType | 数字 | webhook类型；1-企业微信机器人，2-钉钉机器人，3-飞书机器人，4-Server酱，50-bark，6-企业微信应用，7-腾讯轻联，8-IFTTT，9-集简云，10-Gotify，11-WxPusher，12-自定义
webhookTypeName | 字符串 | webhook类型名称
webhookUrl | 字符串 | 调用的url地址
createTime | 日期 | 创建日期
httpMethod | 字符串 | 请求方法（仅自定义类型中返回）
headers | 字符串 | 请求头（仅自定义类型中返回）
body | 字符串 | body内容（仅自定义类型中返回）

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
webhookType | 是 | 无| webhook类型；1-企业微信机器人，2-钉钉机器人，3-飞书机器人，4-Server酱，50-bark，6-企业微信应用，7-腾讯轻联，8-IFTTT，9-集简云，10-Gotify，11-WxPusher，12-自定义
webhookUrl | 是 | 无| 调用的url地址
httpMethod | 否 | 无 | 请求方法（仅自定义类型中需要）
headers | 否 | 无 | 请求头（仅自定义类型中需要）
body | 否 | 无 | body内容（仅自定义类型中需要）

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
webhookType | 是 | 无| webhook类型；1-企业微信机器人，2-钉钉机器人，3-飞书机器人，4-Server酱，50-bark，6-企业微信应用，7-腾讯轻联，8-IFTTT，9-集简云，10-Gotify，11-WxPusher，12-自定义
webhookUrl | 是 | 无| 调用的url地址
httpMethod | 否 | 无 | 请求方法（仅自定义类型中需要）
headers | 否 | 无 | 请求头（仅自定义类型中需要）
body | 否 | 无 | body内容（仅自定义类型中需要）

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

## 八. 微信ClawBot接口
### 1. 获取二维码
- 请求地址：https://www.pushplus.plus/api/open/clawBot/getBotQrcode
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": {
        "url": "https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=904f3f50d55baaa2738a004588babdea&bot_type=3",
        "qrcode": "904f3f50d55baaa2738a004588babdea"
    }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
url | 字符串 | 二维码地址
qrcode | 字符串 | 二维码编号

### 2. 扫码结果查询
- 请求地址：https://www.pushplus.plus/api/open/clawBot/getQrcodeStatus
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
getQrcodeStatus | 是 | 无 | 二维码编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 3. 绑定详情
- 请求地址：https://www.pushplus.plus/api/open/clawBot/botInfo
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": {
        "createTime": "2026-03-26 23:14:23",
        "haveContextToken": 1
    }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
createTime | 字符串 | 绑定时间
haveContextToken | 字符串 | 是否有对话令牌

### 4. 解绑
- 请求地址：https://www.pushplus.plus/api/open/clawBot/unbind
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功"
}
```

### 5. 获取发送消息
- 请求地址：https://www.pushplus.plus/api/open/clawBot/getMsg
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": [
        {
            "type": 1,
            "text": "文字消息"
        },
        {
            "type": 3,
            "text": "语音消息"
        }
    ]
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
type | 字符串 | 消息类型；1-文字，3-语音
text | 字符串 | 消息内容

## 九. QQ机器人接口
注：需先在个人中心->渠道配置->QQ机器人中完成绑定。发送消息时 channel 传 `qq`，option 不填发给自己，填写配置编码则发送到对应QQ群。

### 1. 获取绑定链接
- 请求地址：https://www.pushplus.plus/api/open/qqBot/getBindLink
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
refresh | 否 | false | 是否强制刷新；true 时会使旧绑定码失效并重新生成

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": {
        "url": "https://qun.qq.com/q/xxxx",
        "bindCode": "A3K7M2",
        "expireSeconds": 300,
        "botAppId": "1020******",
        "botName": "pushplus机器人",
        "botAvatar": "https://xxx/avatar.png"
    }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
url | 字符串 | 带参分享链接，用于生成扫码二维码。已绑定用户再次获取时可能为空
bindCode | 字符串 | 绑定码。已是好友时扫码不会触发加好友事件，需私聊发送该绑定码；认领QQ群也使用此码
expireSeconds | 数字 | 有效期秒数，默认300秒
botAppId | 字符串 | 为当前用户分配的官方机器人appId
botName | 字符串 | 机器人名称，用于提示用户添加哪一个机器人
botAvatar | 字符串 | 机器人头像

### 2. 查询绑定状态
- 请求地址：https://www.pushplus.plus/api/open/qqBot/botInfo
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": {
        "isBind": 1,
        "receiveStatus": 1,
        "createTime": "2026-08-26 10:00:00",
        "botInfo": {
            "botId": "12345678",
            "username": "pushplus机器人",
            "avatar": "https://xxx/avatar.png",
            "appId": "1020******",
            "shareUrl": "https://qun.qq.com/q/xxxx"
        }
    }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
isBind | 数字 | 是否已绑定；0-未绑定，1-已绑定
receiveStatus | 数字 | 单聊接收状态；1-可接收，0-用户已关闭单聊接收
createTime | 日期 | 绑定时间
botInfo | 对象 | 机器人详情，取不到时为空

- 机器人详情字段说明

参数名称 | 类型 | 说明
---|--- | ---
botId | 字符串 | 机器人ID
username | 字符串 | 机器人昵称
avatar | 字符串 | 机器人头像
appId | 字符串 | 机器人appId
shareUrl | 字符串 | 官方分享链接，可用于拉机器人进群

### 3. 解绑QQ机器人
- 请求地址：https://www.pushplus.plus/api/open/qqBot/unbind
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功"
}
```

### 4. 获取已加入的QQ群列表
- 请求地址：https://www.pushplus.plus/api/open/qqBot/groupList
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 无

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": [
        {
            "id": 1,
            "groupOpenId": "C4******ab",
            "groupRemark": "",
            "status": 1,
            "groupName": "pushplus交流群",
            "groupFingerMemo": "群简介",
            "groupClassText": "兴趣爱好",
            "groupTags": ["推送"],
            "groupMemberNum": 128,
            "createTime": "2026-08-26 10:12:00"
        }
    ]
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | QQ群编号；新增群配置时作为 qqGroupId 使用
groupOpenId | 字符串 | 群openid
groupRemark | 字符串 | 群备注
status | 数字 | 群状态；1-在群，2-群消息接收关闭
groupName | 字符串 | 群名称，接口未授权时为空
groupFingerMemo | 字符串 | 群简介
groupClassText | 字符串 | 群分类
groupTags | 数组 | 群标签
groupMemberNum | 数字 | 群成员人数
createTime | 日期 | 创建时间

### 5. 获取QQ机器人配置列表
- 请求地址：https://www.pushplus.plus/api/open/qqBot/list
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
    "total": 1,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "qqName": "交流群推送",
        "qqCode": "qqgroup",
        "sendType": 2,
        "qqGroupId": 1,
        "groupRemark": "",
        "groupOpenId": "C4******ab",
        "groupName": "pushplus交流群",
        "updateTime": "2026-08-26 11:00:00"
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
list | 数组 | 配置列表

- 配置列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 配置编号
qqName | 字符串 | 配置名称
qqCode | 字符串 | 配置编码；发送消息时作为 option 传入
sendType | 数字 | 发送类型；2-发到QQ群
qqGroupId | 数字 | QQ群编号
groupRemark | 字符串 | 群备注
groupOpenId | 字符串 | 群openid
groupName | 字符串 | 群名称，接口未授权时为空
updateTime | 日期 | 更新时间

### 6. 新增QQ机器人配置
注：配置用于把消息发送到指定QQ群。发给自己无需创建配置。普通用户最多5个，会员最多30个。同一QQ群不可重复创建。配置编码创建后不可修改。

- 请求地址：https://www.pushplus.plus/api/open/qqBot/add
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "qqName": "交流群推送",
  "qqCode": "qqgroup",
  "qqGroupId": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
qqName | 是 | 无 | 配置名称；最多64个字符
qqCode | 是 | 无 | 配置编码；最多32个字符，仅支持字母、数字、下划线和中划线
qqGroupId | 是 | 无 | QQ群编号，取自群列表接口中的 id。该群需在群内允许机器人主动消息

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功"
}
```

### 7. 修改QQ机器人配置
注：配置编码(qqCode)不允许修改，避免已在使用的 option 失效。

- 请求地址：https://www.pushplus.plus/api/open/qqBot/edit
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "id": 1,
  "qqName": "交流群推送",
  "qqGroupId": 1
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 配置编号
qqName | 是 | 无 | 配置名称；最多64个字符
qqGroupId | 是 | 无 | QQ群编号

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功"
}
```

### 8. 删除QQ机器人配置
- 请求地址：https://www.pushplus.plus/api/open/qqBot/delete?id=1
- 请求方式：DELETE
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 配置编号

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功"
}
```

## 十. 功能设置接口
### 1. 获取默认配置列表
- 请求地址：https://www.pushplus.plus/api/open/setting/listUserDefault
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
  "msg": "请求成功",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 5,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "channel": "wechat",
        "channelTxt": "微信公众号",
        "updateTime": "2025-12-08 09:32:06",
        "name": "用户token"
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
id | 数字 | 默认配置编号
channel | 字符串 | 渠道编码；wechat-微信公众号,cp-企业微信应用,webhook-第三方webhook,mail-邮件,sms-短信,voice-语音,extension-插件,qq-QQ机器人
channelTxt | 字符串 | 渠道名称
updateTime | 字符串 | 更新时间
name | 字符串 | 令牌名称

### 2. 默认配置详情
- 请求地址：https://www.pushplus.plus/api/open/setting/detailUserDefault?id=1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 默认配置编号

- 响应内容
```
{
    "code": 200,
    "msg": "执行成功",
    "data": {
        "id": 1,
        "channel": "wechat",
        "option": "wx3b5738b0e92dc180",
        "pre": "",
        "updateTime": "2025-12-08 09:32:06",
        "name": "用户token",
        "tokenId": 0
    }
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 默认配置编号
channel | 字符串 | 渠道编码；wechat-微信公众号,cp-企业微信应用,webhook-第三方webhook,mail-邮件,sms-短信,voice-语音,extension-插件,qq-QQ机器人
option | 字符串 | 渠道参数
pre | 字符串 | 预处理编码
updateTime | 字符串 | 更新时间
name | 字符串 | 令牌名称
tokenId | 数字 | 消息令牌id；用户令牌为0

### 3. 新增默认配置
- 请求地址：https://www.pushplus.plus/api/open/setting/addUserDefault
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "channel": "wechat",
  "option": "wxa551176bf758ffc7",
  "pre": "test",
  "tokenId": "1"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
channel | 是 | 无 | 渠道编码；wechat-微信公众号,cp-企业微信应用,webhook-第三方webhook,mail-邮件,sms-短信,voice-语音,extension-插件,qq-QQ机器人
option | 是 | 无 | 渠道参数
pre | 是 | 无| 预处理编码
tokenId | 是 | 无| 消息令牌id；用户令牌为0


- 响应内容
```
{
  "code": 200,
  "msg": "请求成功"
}
```

### 4. 修改默认配置
- 请求地址：https://www.pushplus.plus/api/open/setting/editUserDefault
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "channel": "wechat",
  "option": "wxa551176bf758ffc7",
  "pre": "",
  "tokenId": "15",
  "id": "2114"
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 默认配置编号
channel | 是 | 无 | 默认渠道；wechat-微信公众号,cp-企业微信应用,webhook-第三方webhook,mail-邮件,sms-短信,voice-语音,extension-插件,qq-QQ机器人
option | 否 | 无 | 渠道参数；webhook和cp渠道需要填写具体的webhook编号或自定义编码
pre | 否 | 无 | 预处理编码
tokenId | 是 | 无 | 消息令牌id；用户令牌为0


- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": "修改成功"
}
```

### 5. 删除默认配置
- 请求地址：https://www.pushplus.plus/api/open/setting/deleteUserDefault?id=1
- 请求方式：DELETE
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 默认配置编号

- 响应内容
```
{
  "code": 200,
  "msg": "请求成功",
  "data": "默认配置删除成功"
}
```

### 6. 修改接收消息限制
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

### 7. 开启/关闭发送消息功能
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

### 8. 修改打开消息方式
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

### 9. 修改插件渠道转发
- 请求地址：https://www.pushplus.plus/api/open/setting/extension?forward=0
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
forward | 是 | 无 | 微信渠道消息是否同步浏览器扩展插件接收和桌面应用程序；0:否，1:是

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": null
}
```

## 十一. 好友功能接口
### 1. 获取个人二维码
- 请求地址：https://www.pushplus.plus/api/open/friend/getQrCode?appId=wx3b5738bdds3c180&content=123&second=604800&scanCount=-1
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: 

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
appId | 否 | 无 | 微信公众号Id
content | 否 | 无 | 自定义参数，扫描后回调（可用于区分扫描渠道）
second | 否 | 604800 | 二维码有效期（单位秒）；不传默认7天，最长30天
scanCount | 否 | -1 | 可扫码次数；范围1-999次，-1代表无限次

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

### 5. 将好友加入黑名单
注：加入后将解除双方好友关系，对方无法再添加你。不能将自己加入黑名单，仅可将已有好友加入黑名单。

- 请求地址：https://www.pushplus.plus/api/open/friend/addBlacklist?friendId=1
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
friendId | 是 | 无 | 好友id（好友列表中的 friendId 字段）

- 响应内容
```
{
  "code": 200,
  "data": null,
  "msg": "执行成功"
}
```

### 6. 好友黑名单列表
- 请求地址：https://www.pushplus.plus/api/open/friend/blacklistList
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
  "data": {
    "list": [
      {
        "id": 4,
        "friendId": 1322,
        "nickName": "昵称",
        "headImgUrl": "",
        "createTime": "2026-08-17 10:00:00"
      }
    ],
    "pageNum": 1,
    "pageSize": 20,
    "pages": 1,
    "total": 1
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
list | 数组 | 黑名单列表

- 黑名单列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 黑名单记录ID；解除黑名单时使用
friendId | 数字 | 被拉黑好友ID
nickName | 字符串 | 昵称
headImgUrl | 字符串 | 头像
createTime | 日期 | 拉黑时间

### 7. 解除好友黑名单
注：解除后不会自动恢复好友关系，需重新扫码添加。

- 请求地址：https://www.pushplus.plus/api/open/friend/removeBlacklist?id=1
- 请求方式：POST
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数: url传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
id | 是 | 无 | 黑名单记录ID（黑名单列表中的 id 字段）

- 响应内容
```
{
  "code": 200,
  "data": null,
  "msg": "执行成功"
}
```

## 十二. 预处理信息接口
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

## 十三. 图片服务接口

&nbsp;&nbsp;&nbsp;&nbsp;用于获取七牛云上传凭证、上传图片、查询已上传列表及主动删除。上传时使用「获取上传凭证」返回的 `uploadUrl` 与 `uploadToken`，按七牛云表单上传规范提交文件。仅支持图片类型，30 天有效期。

### 1. 获取上传凭证
- 请求地址：https://www.pushplus.plus/api/open/userImage/uploadToken
- 请求方式：GET
- (header) access-key: d7b******62f(获取到的AccessKey)
- 说明：返回七牛云表单上传所需的 token 及上传域名、存储桶等信息，用于调用七牛上传接口完成图片上传。

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": {
    "uploadToken": "dk2Xhd322ds-ODYNXBq15gHdUAT4N3MKVmEIp2:...",
    "uploadHost": "https://upload.qiniup.com",
    "uploadUrl": "https://upload.qiniup.com/",
    "bucket": "pushplus-img",
    "expiresIn": 600
  }
}
```
- 响应字段说明（data）

参数名称 | 类型 | 说明
---|--- | ---
uploadToken | 字符串 | 七牛云上传凭证
uploadHost | 字符串 | 七牛云上传域名
uploadUrl | 字符串 | 七牛云上传地址
bucket | 字符串 | 七牛云存储桶名称
expiresIn | 数字 | 凭证有效时间（秒）

### 2. 上传图片
- 请求地址：取「获取上传凭证」响应中的 **uploadUrl**（一般为 `https://upload.qiniup.com/`）
- 请求方式：POST
- Content-Type：multipart/form-data
- 说明：七牛云表单上传，无需携带 `access-key`

- 请求参数（form-data）

参数名称 | 是否必填 | 说明
---|--- | ---
token | 是 | 上传凭证，即「获取上传凭证」返回的 `uploadToken`
file | 是 | 待上传的图片文件（二进制）

- 响应内容
```
{
  "errno": 0,
  "ext": ".png",
  "fname": "a142bd212e4f2199e0cdc2ba62b9a441.png",
  "fsize": 112459,
  "hash": "Fh6DhVFkTz-DHzgAhcO7nd9KQKbx",
  "key": "1/Fh6DhVFkTz-DHzgAhcO7nd9KQKbx.png",
  "mimeType": "image/png",
  "msg": "ok",
  "thumbnail": "https://pic.pushplus.plus/1/Fh6DhVFkTz-DHzgAhcO7nd9KQKbx.png@s",
  "url": "https://pic.pushplus.plus/1/Fh6DhVFkTz-DHzgAhcO7nd9KQKbx.png@p"
}
```
- 响应字段说明

参数名称 | 类型 | 说明
---|--- | ---
errno | 数字 | 错误码；0 表示成功
ext | 字符串 | 文件扩展名
fname | 字符串 | 文件名
fsize | 数字 | 文件大小（字节）
hash | 字符串 | 文件 hash
key | 字符串 | 对象存储中的路径 key
mimeType | 字符串 | MIME 类型
msg | 字符串 | 响应说明
thumbnail | 字符串 | 缩略图地址
url | 字符串 | 图片访问地址

### 3. 图片列表
- 请求地址：https://www.pushplus.plus/api/open/userImage/list
- 请求方式：POST
- Content-Type: application/json
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数:
```
{
  "current": 1,
  "pageSize": 10,
  "params": {}
}
```
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- |--- | ---
current | 否 | 1 | 当前所在分页数
pageSize | 否 | 10 | 每页大小，最大值为50
params | 否 | {} | 扩展查询参数

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功",
  "data": {
    "pageNum": 1,
    "pageSize": 3,
    "total": 3,
    "pages": 1,
    "list": [
      {
        "id": 1,
        "imgUrl": "https://pic.pushplus.plus/1/Ft1kme4xCSOfBKsniVQR-WDa2wrs.png@p",
        "thumbnail": "https://pic.pushplus.plus/1/Ft1kme4xCSOfBKsniVQR-WDa2wrs.png@s",
        "createTime": "2026-05-09 14:44:40"
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
list | 数组 | 图片列表

- 图片列表字段说明

参数名称 | 类型 | 说明
---|--- | ---
id | 数字 | 图片 id
imgUrl | 字符串 | 图片地址
thumbnail | 字符串 | 缩略图地址
createTime | 字符串 | 创建时间

### 4. 删除图片
- 请求地址：https://www.pushplus.plus/api/open/userImage/delete?id=1
- 请求方式：DELETE
- (header) access-key: d7b******62f(获取到的AccessKey)
- 请求参数：url 传参
- 请求参数说明

参数名称 | 是否必填 | 默认值 | 说明
---|--- | --- | ---
id | 是 | 无 | 图片 id

- 说明：主动删除图片；未删除的图片默认 30 天后由系统自动清理。

- 响应内容
```
{
  "code": 200,
  "msg": "执行成功"
}
```
