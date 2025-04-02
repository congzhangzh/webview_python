#!/bin/bash

# 确保脚本在任何错误时退出
set -e

# 定义目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 定义库和URL (使用正确的浏览器版本)
LIBS=(
    "preact.min.js:https://cdn.jsdelivr.net/npm/preact@10.15.1/dist/preact.min.js"
    "hooks.min.js:https://cdn.jsdelivr.net/npm/preact@10.15.1/hooks/dist/hooks.umd.min.js"
    "htm.min.js:https://cdn.jsdelivr.net/npm/htm@3.1.1/dist/htm.min.js"
)

echo "开始下载Preact相关库文件..."

# 使用curl或wget下载文件
for lib in "${LIBS[@]}"; do
    # 分割库名和URL
    LIB_NAME="${lib%%:*}"
    URL="${lib#*:}"
    
    echo "下载 $LIB_NAME 从 $URL"
    
    # 尝试使用curl，如果不可用则尝试wget
    if command -v curl > /dev/null; then
        curl -L -o "$SCRIPT_DIR/$LIB_NAME" "$URL"
    elif command -v wget > /dev/null; then
        wget -O "$SCRIPT_DIR/$LIB_NAME" "$URL"
    else
        echo "错误: 需要curl或wget来下载文件"
        exit 1
    fi
    
    # 检查文件是否下载成功
    if [ ! -s "$SCRIPT_DIR/$LIB_NAME" ]; then
        echo "错误: 下载 $LIB_NAME 失败"
        exit 1
    fi
    
    echo "$LIB_NAME 下载完成"
done

echo "所有库文件已成功下载到 $SCRIPT_DIR"
echo "现在可以运行 'python preact_offline_example.py' 启动应用" 