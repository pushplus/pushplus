# 是否支持发送图片？

pushplus支持在内容中发送图片信息。具体方式通过html的\<img\>标签来实现。

例如：
```
{
    "token":"{token},
    "title":"标题",
    "content":"内容<br/>![](./images/push.png)",
    "topic":"test"
}
```

注意：
1. 请勿使用base64编码的方式把本地图片放到内容中，您可以将本地的图片上传到七牛云等云存储空间上来获取图片的外链地址。
2. img标签中如直接使用第三方网站的图片不显示，是因为第三方网站做了防盗链处理，请使用自己的图床。

#### 推荐使用七牛云，免费10G空间：<a href="https://s.qiniu.com/6BBFNv" target="_blank">点击获取</a>