# 用户token和消息token有什么区别？

## 相同点
用户token和消息token均可以用于发送消息，填写在“token”参数上。

## 不同点
1. 用户token代表具体您是哪个用户，有且仅有一个，无法删除。消息token可以自行创建和删除，支持多个。
2. 开放接口调用需要使用用户token，不支持消息token。

## 使用场景
消息token可创建多个，可自行标识使用的场景，方便管理和维护。主要用在第三方开发的脚本、程序或系统上。