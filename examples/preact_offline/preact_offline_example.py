from webview.webview import Webview, Size, SizeHint
import os
import sys

# 创建Webview实例
webview = Webview(debug=True)
webview.title = "离线Preact示例"
webview.size = Size(800, 600, SizeHint.NONE)

# 初始计数器值
count = 0

# Python函数: 获取当前计数
def get_count():
    return count

# Python函数: 增加计数
def increment():
    global count
    count += 1
    return count

# Python函数: 减少计数
def decrement():
    global count
    count -= 1
    return count

# 绑定Python函数
webview.bind("getCount", get_count)
webview.bind("increment", increment)
webview.bind("decrement", decrement)

# 获取HTML文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'preact_offline_example.html')

# 检查HTML文件是否存在
if not os.path.exists(html_path):
    print(f"错误: HTML文件不存在: {html_path}")
    sys.exit(1)

# 检查JS库是否已下载
required_libs = ['preact.min.js', 'hooks.min.js', 'htm.min.js']
missing_libs = [lib for lib in required_libs if not os.path.exists(os.path.join(current_dir, lib))]

if missing_libs:
    # 提示用户运行下载脚本
    script_name = 'download_libs.bat' if sys.platform == 'win32' else 'download_libs.sh'
    print(f"错误: 缺少必要的JavaScript库文件: {', '.join(missing_libs)}")
    print(f"请运行 {os.path.join(current_dir, script_name)} 下载所需库文件")
    sys.exit(1)

# 使用file://协议加载HTML
webview.navigate(f"file://{html_path}")
webview.run() 
