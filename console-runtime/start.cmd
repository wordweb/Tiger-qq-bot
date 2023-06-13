@echo off
setlocal
set JAVA_BINARY="java"
if exist "java-home" set JAVA_BINARY=".\java-home\bin\java.exe"

%JAVA_BINARY% -version
%JAVA_BINARY% -D"file.encoding=utf-8" -cp "./libs/*" "net.mamoe.mirai.console.terminal.MiraiConsoleTerminalLoader"

set EL=%ERRORLEVEL%
if %EL% NEQ 0 (
    echo Process exited with %EL%
    pause
)