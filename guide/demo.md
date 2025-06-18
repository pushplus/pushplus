# Demo代码

## 在线测试页面
可以访问[https://pushplus.apifox.cn/](https://pushplus.apifox.cn/)，在线的测试接口。也可以直接使用页面上生成的代码示例，支持多种语言。

## Shell代码示例
> 使用Shell脚本演示具体如何发送消息

- 获取自己的token。\
可到pushplus的官网登录获取下自己的token。pushplus的网址是：[http://www.pushplus.plus](http://www.pushplus.plus)
- 确保服务器中已安装curl和jq两个工具。curl用于发送http请求，jq用于解析json格式。
- POST请求方式代码

```shell
#!/bin/bash

#pushplus的相关参数
TOKEN="你的token"
TITLE="测试工单"
CONTENT="消息的内容<br/>![](./images/push.png)"
URL="https://www.pushplus.plus/send/"

# 定义文件用于记录是否已经发送过通知
SENT_FLAG_FILE="sent.flag"

# 判断文件是否存在
if [ -e "$SENT_FLAG_FILE" ]; then
    # 获取文件的创建时间（秒级时间戳）
    file_creation_time=$(stat -c %Y "$SENT_FLAG_FILE")

    # 获取第二天的0点时间（秒级时间戳）
    next_day_start_time=$(date -d "tomorrow" +%s)

    # 判断文件的创建时间是否大于等于第二天的0点时间
    if [ "$file_creation_time" -ge "$next_day_start_time" ]; then
        # 删除标志文件
        rm "$SENT_FLAG_FILE"
    fi
fi

# 检查是否已经发送过通知
if [ ! -e "$SENT_FLAG_FILE" ]; then
    # 发送HTTP POST请求
    response=$(curl -s -X POST -d "token=$TOKEN&title=$TITLE&content=$CONTENT" "$URL")

    # 解析响应JSON，您需要根据实际情况来提取返回码
    code=$(echo "$response" | jq -r '.code')
    echo $response

    # 判断返回码是否为900（用户账号使用受限）
    if [ "$code" -eq 900 ]; then
        # 创建标志文件，表示已经发送过通知
        touch "$SENT_FLAG_FILE"
    fi
fi
```
- 说明\
示例用使用sent.flag文件来判断是否超过正常请求次数，以防止超额后还继续请求造成封号。您可以自行选择使用其他方式来替代判断。

## python代码示例
> 使用python语言演示具体如何发送消息

- 获取自己的token。\
可到pushplus的官网登录获取下自己的token。pushplus的网址是：[http://www.pushplus.plus](http://www.pushplus.plus)
- GET请求方式代码
```python
# encoding:utf-8
import requests
token = '你的token' #在pushplus网站中可以找到
title= '标题' #改成你要的标题内容
content ='内容' #改成你要的正文内容
url = 'http://www.pushplus.plus/send?token='+token+'&title='+title+'&content='+content
requests.get(url)

```


- POST请求方式代码

```python
# encoding:utf-8
import requests
import json
token = '你的token' #在pushpush网站中可以找到
title= '标题' #改成你要的标题内容
content ='内容' #改成你要的正文内容
url = 'http://www.pushplus.plus/send'
data = {
    "token":token,
    "title":title,
    "content":content
}
body=json.dumps(data).encode(encoding='utf-8')
headers = {'Content-Type':'application/json'}
requests.post(url,data=body,headers=headers)
```

- 运行后效果\
![效果1](./images/message.jpg)

![效果2](./images/message2.jpg)

- 说明\
更多参数用法请查看pushplus接口文档

## java代码示例
> 考虑请求次数限制，根据返回码做了是否继续请求的判断，防止账号被封

- GET请求方式代码\
使用的hutools工具类，自定义了redis操作类，ResultT请求响应对象。正式使用的时候改成自己的封装的。

```java
//写在SpringBoot项目中的测试类，演示通过get方式发送消息
@SpringBootTest
public class PushControllerTest {
    //自己写的redis操作类
    @Autowired
    private RedisService redisService;

    @Test
    public void send(){
        //redis的key，可以自己随便命名
        String redisKey= "pushplus:canSend";
        //读取redis里面的值，是否为1，不为1的才能请求pushplus接口
        Integer limit = redisService.get(redisKey)!= null ? (Integer) redisService.get(redisKey):0;
        if(limit!=1){
            String token= "您的token"; //您的token
            String title= "标题";  //消息的标题
            String content= "内容<br/>![](./images/push.png)";  //消息的内容,包含文字、换行和图片
            String url = "https://www.pushplus.plus/send?title="+ title +"&content="+ content +"&token=" + token;

            //服务器发送Get请求，接收响应内容
            String response = HttpUtil.get(url);
            //把返回的字符串结果变成对象
            ResultT resultT = JSONUtil.toBean(response,ResultT.class);

            //判断返回码是否为900（用户账号使用受限），如果是就修改redis对象，下次请求不在发送
            if(resultT.getCode()==900){
                //使用redis缓存做全局判断，设置到第二天凌点自动失效
                redisService.set(redisKey,1, TimeUtil.getSecondsNextEarlyMorning());
            }
        }
    }
}
```

- POST请求方式代码
```java
public class PushControllerTest {
    //自己写的redis操作类
    @Autowired
    private RedisService redisService;

    @Test
    public void send(){
        //redis的key，可以自己随便命名
        String redisKey= "pushplus:canSend";
        //读取redis里面的值，是否为1，不为1的才能请求pushplus接口
        Integer limit = redisService.get(redisKey)!= null ? (Integer) redisService.get(redisKey):0;
        if(limit!=1){
            String token= "您的token"; //您的token
            String title= "标题";  //消息的标题
            String content= "内容<br/>![](./images/push.png)";  //消息的内容
            String url = "https://www.pushplus.plus/send/";

            Map<String,Object> map = new HashMap<>();
            map.put("token",token);
            map.put("title",title);
            map.put("content",content);

            //服务器发送POST请求，接收响应内容
            String response = HttpUtil.post(url,map);
            //把返回的字符串结果变成对象
            ResultT resultT = JSONUtil.toBean(response,ResultT.class);

            //判断返回码是否为900（用户账号使用受限），如果是就修改redis对象，下次请求不在发送
            if(resultT.getCode()==900){
                //使用redis缓存做全局判断，设置到第二天凌点自动失效
                redisService.set(redisKey,1, TimeUtil.getSecondsNextEarlyMorning());
            }
        }
    }
}

```

- 说明\
示例用使用redis来做全局变量判断是否超过正常请求次数，以防止超额后还继续请求造成封号。您可以自行选择使用其他方式（如memoryCache）来替代全局判断。