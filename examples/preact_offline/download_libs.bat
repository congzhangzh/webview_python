@echo off
setlocal enabledelayedexpansion

:: 确定脚本所在目录
set "SCRIPT_DIR=%~dp0"

echo 开始下载Preact相关库文件...

:: 定义库和URL (使用正确的浏览器版本)
set "LIBS[1]=preact.min.js:https://cdn.jsdelivr.net/npm/preact@10.15.1/dist/preact.min.js"
set "LIBS[2]=hooks.min.js:https://cdn.jsdelivr.net/npm/preact@10.15.1/hooks/dist/hooks.umd.min.js"
set "LIBS[3]=htm.min.js:https://cdn.jsdelivr.net/npm/htm@3.1.1/dist/htm.min.js"

:: 下载文件
for /L %%i in (1,1,3) do (
    for /F "tokens=1,2 delims=:" %%a in ("!LIBS[%%i]!") do (
        set "LIB_NAME=%%a"
        set "URL=%%b"
        
        echo 下载 !LIB_NAME! 从 !URL!
        
        :: 使用PowerShell下载文件
        powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '!URL!' -OutFile '%SCRIPT_DIR%\!LIB_NAME!' }"
        
        :: 检查文件是否下载成功
        if not exist "%SCRIPT_DIR%\!LIB_NAME!" (
            echo 错误: 下载 !LIB_NAME! 失败
            exit /b 1
        )
        
        echo !LIB_NAME! 下载完成
    )
)

echo 所有库文件已成功下载到 %SCRIPT_DIR%
echo 现在可以运行 'python preact_offline_example.py' 启动应用 