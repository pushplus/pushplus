# pushplus MCP Server 使用说明

## MCP Server简介
&nbsp;&nbsp;&nbsp;&nbsp;MCP简单来说是一个协议，让各家的大模型能够通过这个统一的标准协议跟外部能力去通讯。从而让大模型来调用各种工具，比如让大模型操作浏览器、控制Windows系统，当然也可以直接让大模型来调用pushplus推送消息。\
&nbsp;&nbsp;&nbsp;&nbsp;MCP分为客户端和服务端。客户端就是用户自己使用的工具，比如Claude Desktop,Cursor,Cline等。服务端就是由开发者提供的程序或接口服务。\
&nbsp;&nbsp;&nbsp;&nbsp;MCP服务端分为两种方式，一种是本地运行的程序，程序来作为中转，一方面跟大模型通讯，另外一方面调用具体的功能。另外一种是远程的接口服务，相当于把本来运行在本地的程序部署在服务器上，然后通过HTTP接口通讯。

## 项目地址
&nbsp;&nbsp;&nbsp;&nbsp;目前pushplus MCP Server是提供本地运行的程序这种常用方式。开发了TypeScript版本和Java版本。推荐使用TypeScript版本，启动速度快，资源占用小。

### 1. TypeScript版本
TypeScript版本需要本地安装node，版本18及以上。

项目地址：
- github：[https://github.com/pushplus/pushplus-MCP-Server-TypeScript](https://github.com/pushplus/pushplus-MCP-Server-TypeScript)
- gitee：[https://gitee.com/pushplus/pushplus-MCP-Server-TypeScript](https://gitee.com/pushplus/pushplus-MCP-Server-TypeScript)


配置说明，详细说明查看项目地址中的README.md：

Linux/Mac
```
{
  "mcpServers": {
    "pushplus": {
      "command": "npx",
      "args": [
        "-y",
        "@perk-net/pushplus-mcp-server"
      ],
      "env": {
        "PUSHPLUS_TOKEN": "您的Token",
        "PUSHPLUS_SECRET_KEY": "您的SecretKey"
      }
    }
  }
}
```

Windows
```
{
  "mcpServers": {
    "pushplus": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@perk-net/pushplus-mcp-server"
      ],
      "env": {
        "PUSHPLUS_TOKEN": "您的Token",
        "PUSHPLUS_SECRET_KEY": "您的SecretKey"
      }
    }
  }
}
```

- PUSHPLUS_TOKEN 替换为从pushplus官网上获取到的消息token或用户token
- PUSHPLUS_SECRET_KEY 替换为pushplus开发设置中的SecretKey

### 2. Java版本
Java版本需要本地安装JDK21。

项目地址：
- github：[https://github.com/pushplus/pushplus-mcp-server-Java](https://github.com/pushplus/pushplus-mcp-server-Java)
- gitee：[https://gitee.com/pushplus/pushplus-mcp-server](https://gitee.com/pushplus/pushplus-mcp-server)

配置说明，详细说明查看项目地址中的README.md：
```
{
  "mcpServers": {
    "pushplus-mcp-server": {
      "command": "java",
      "args": [
        "-Dlogging.pattern.console=",
        "-jar",
        "yourFilePath\\pushplus-mcp-1.0.5.jar"
      ],
      "env": {
        "PUSHPLUS_TOKEN": "替换为自己的token",
        "PUSHPLUS_SECRET_KEY": "替换为secretKey"
      }
    }
  }
}
```

- PUSHPLUS_TOKEN 替换为从pushplus官网上获取到的消息token或用户token
- PUSHPLUS_SECRET_KEY 替换为pushplus开发设置中的SecretKey
- yourFilePath\\pushplus-mcp-1.0.5.jar 修改为自己本地的文件路径
