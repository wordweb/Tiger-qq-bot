登陆协议选 ANDROID_PAD
例如
login 123456 password ANDROID_PAD

原理是回退到风控较轻的 旧版本协议 8.8.88，顺便这个 8.8.88 的信息实际上是 ANDROID_PHONE 的，所以会顶号

这是独立的开发版本整合包，不能替换 mcl 的文件来使用

如果出现 'java' 不是内部或外部命令，也不是可运行的程序
说明你没有安装好 Java，你可以选择本地补充安装

本地补充安装（Windows）：

自行二选一下载，然后解压全部文件 到 start.cmd 同目录，并将 jdk-17.0.7+7-jre 重命名为 java-home

windows x64 版本
https://mirrors.tuna.tsinghua.edu.cn/Adoptium/17/jre/x64/windows/OpenJDK17U-jre_x64_windows_hotspot_17.0.7_7.zip

windows x86 版本
https://mirrors.tuna.tsinghua.edu.cn/Adoptium/17/jre/x32/windows/OpenJDK17U-jre_x86-32_windows_hotspot_17.0.7_7.zip

目录结构如下
├───java-home (本地java目录，注意要解压全部文件，这里仅列出部分目录结构)
│   └───bin
│       └───java.exe
├───start.cmd (WIN启动脚本)
├───start.sh (Linux/MACOS启动脚本)
├───libs (库目录，里面有mirai本体)
├───logs (日志目录，里面有日志文件)
├───plugins (插件目录)
└───android_pad.json (协议版本信息)

整合包 by https://github.com/cssxsh