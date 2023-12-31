﻿# 基于本地知识库的 TigerBot 大语言模型qq群知识库bot应用实现

## 介绍
在实际应用中，当企业或者个人，需要一款简便易用轻量的本地知识库查询系统。如果设计过重的前端ui和复杂的知识库管理系统，对个人和企业的部署成本来说都是不划算的。从使用习惯上qq的文件上传和聊天方式都是一种习以为常的操作行为，所以便有了依托于qq群作为载体，实现轻量化部署的一个本地知识库查询系统的需求。


在实际操作中，对qqbot进行了信息的一个初步过滤，仅对@后的文本和文件上传事件做出响应。且可以通过qq发送消息的方式来快捷的管理本地知识库中的文件。


这个项目是在[langchain-ChatGLM-and-TigerBot](https://github.com/wordweb/langchain-ChatGLM-and-TigerBot)已经成功部署作为基础条件的情况下来运行的。

由于时间和设备有限，仅在windows环境下做了验证测试。是可以完整跑通的。


## windows下的安装流程


链接: https://pan.baidu.com/s/11O5wnEJ7B3dkM1cvTdKMAA 提取码: 4g63 

下载Python310.zip


解压后确保Python.exe是在这个路径

c:\Tiger-qq-Bot\Python310\Python.exe



第一步确保你在本地已经成功运行langchain-ChatGLM-and-TigerBot

并用 api.py的方式启动

项目下载地址

https://github.com/wordweb/langchain-ChatGLM-and-TigerBot



修改 当前项目中的api.py(api.py) 中

langchain_tigerbot_server="http://127.0.0.1:7861/"

改为你实际服务器部署的地址，记得最后要/结尾


====================================================================

进入console-runtime目录

双击start.cmd启动qq协议

输入

/login 123456 password ANDROID_PAD

在此过程中，可能需要用到滑块验证，请在一个安卓手机上安装滑块验证工具(console-runtime/滑动验证助手_1.3.apk) ，复制控制台最后给出的链接，到安卓手机上。进入滑块验证过程。验证成功后将获得一个token
复制token在控制台中输入，并回车

接下来会提示将发送短信验证，输入yes

将手机上收到的验证码，输入到控制台，继续回车

完成登陆（只有第一次需要滑块验证和短信验证，第二次登陆则可以自动跳过此过程）


如果无法登陆qq请移步到该问答寻找答案

https://mirai.mamoe.net/topic/223/%E6%97%A0%E6%B3%95%E7%99%BB%E5%BD%95%E7%9A%84%E4%B8%B4%E6%97%B6%E5%A4%84%E7%90%86%E6%96%B9%E6%A1%88


修改 当前项目中api.py(api.py) 中

mirai_server="http://127.0.0.1:9551/"

改为你实际部署的mirai实际服务器地址，记得最后要/结尾


===================================================================


安装api.py所需的模块：

.\Python310\python.exe -m pip install flask[async] -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

.\Python310\python.exe -m pip install requests -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


.\Python310\python.exe api.py

启动mirai与langchain-tigerbot之间的通讯协议层。



将当前登陆的qq拉到群里面

向群发送文件【目前支持： md、pdf、docx、txt 文件格式】即可自动保存为本地知识库


每一个群相当于一个独立的知识库，假设公司有多个部门，例如法务部，则可单独建立一个法务部的群，将机器人拉进去，只上传法务相关文件，则只启用该群知识库内容进行回答。行政部门则可单独再建立一个群，群文件上传对应的行政部门文件，则行政部门群只回答行政部门知识信息。



可以通过以下指令 @机器人+指令 来管理机器人

@机器人昵称 关闭知识库              #该指令表示关闭本地知识库查询，直接与tigerbot对话

@机器人昵称 开启知识库              #该指令表示开启本地知识库查询，通过本地知识库向量查询之后再与tigerbot对话进行问题总结。

@机器人昵称 查看知识库              #该指令用于查询当前知识库中包含哪些文件，方便后续删除相应知识库文件操作。

@机器人昵称 删除文件 文件名      #该指令表示删除指定知识库文件，删除之后如需再次加入，可以从群文件中移除对应文件，再次上传即可

@机器人昵称 info              	   #该指令用户查询当前机器人是否开启知识库查询


向机器人提问

@机器人昵称 问题

等待片刻即可在群里收到机器人的回答


未来版本预期：

可以开关机器人回答问题的方式，语音或者文字。

支持图片ocr识别的方式增加到知识库。



以上项目仅在windows中测试通过，linux环境需要自行进行响应环境配置调整
测试运行py版本3.10.11



## 项目交流群
![二维码](img/qr_code_30.jpg.png)

🎉 Tiger-qq-Bot 项目交流群,如果遇到什么安装上的问题。可以在群里咨询。



