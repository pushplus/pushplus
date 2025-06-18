# 常用问题

### 一. 是否支持https请求?
目前的接口地址支持http和https了

### 二. 在url上和body中同时传递相同参数会取哪个?
参数取值优先取body上的参数，如body上不存在则取url上的，如url上不存在则会取默认值。

### 三. 在消息内容中如何换行？
可以使用HTML语言中的&lt;br/&gt;标签来换行。txt模板可以使用\n来换行。

### 四. curl中发送json格式数据没有展示成json格式怎么办？
请尝试在content中增加\"转义符处理。例如：\
curl -H "Content-Type: application/json" 
-X POST 
-d '{"token":"xxxxxxxxxx","title":"标题","content":"{'\''name'\'':'\''名称'\''}","topic":"neupals","template":"json"}' 
http://www.pushplus.plus/send

### 五. 发送消息接口有什么限制吗？
1. 使用微信模板消息，微信官网有限制，一天最多100万次
2. pushplus为了防止恶意的大量推送消耗整体用户的推送量，限制了每个用户每天最多推送200条微信模板消息。超过条数后当日将无法推送。 
3. 其他渠道（企业微信，钉钉等）暂未限制。

### 六. 用户信息状态不合法是怎么回事？ 
首先，请检查您的请求地址和token是否正确。
请确保您的请求地址是 http://www.pushplus.plus/send
您可以登录官网或在“pushplus 推送加”微信公众号上回复“token”来获取您的token值。

### 更多问题
请查看：[https://support.qq.com/products/315690/faqs-more/](https://support.qq.com/products/315690/faqs-more/)