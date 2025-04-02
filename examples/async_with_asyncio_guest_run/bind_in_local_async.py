import os
import asyncio
from webview import Webview, SizeHint, Size

# Create webview instance
webview = Webview(debug=True)

# 异步函数示例 - 简单延迟响应
async def delayed_response(seconds=1):
    await asyncio.sleep(seconds)
    return f"异步响应完成，耗时 {seconds} 秒"

# 异步函数示例 - 模拟进度报告
async def process_with_progress(steps=5, step_time=1):
    results = []
    for i in range(1, steps + 1):
        await asyncio.sleep(step_time)
        # 通过JavaScript回调报告进度
        progress = (i / steps) * 100
        webview.eval(f"updateProgress({progress}, '处理中: 步骤 {i}/{steps}')")
        results.append(f"步骤 {i} 完成")
    
    return {
        "status": "完成",
        "steps": steps,
        "results": results
    }

# 异步函数示例 - 模拟API请求
async def fetch_data(delay=2, success=True):
    await asyncio.sleep(delay)
    
    if not success:
        raise Exception("模拟的API请求失败")
        
    return {
        "id": 123,
        "name": "示例数据",
        "timestamp": "2023-06-15T12:34:56Z",
        "items": [
            {"id": 1, "value": "项目 1"},
            {"id": 2, "value": "项目 2"},
            {"id": 3, "value": "项目 3"}
        ]
    }

# Bind Python functions
webview.bind("delayedResponse", delayed_response)
webview.bind("processWithProgress", process_with_progress)
webview.bind("fetchData", fetch_data)

webview.title = "Python-JavaScript 异步绑定演示"
webview.size = Size(800, 600, SizeHint.FIXED)

# Get the absolute path to the HTML file
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'bind_in_local_async.html')

# Load the local HTML file
webview.navigate(f"file://{html_path}")

# Run the webview

