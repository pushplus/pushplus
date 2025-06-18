# curl中发送json格式数据没有展示成json格式怎么办？

请尝试在content中增加"转义符处理。

例如：

```
curl -H "Content-Type: application/json" 
-X POST 
-d '{"token":"xxxxxxxxxx","title":"标题","content":"{'''name''':'''名称'''}","topic":"neupals","template":"json"}'
 http://www.pushplus.plus/send
```