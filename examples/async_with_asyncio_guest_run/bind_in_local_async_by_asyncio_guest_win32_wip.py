#
# Copyright 2020 Richard J. Sheridan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from asyncio_guest_run import asyncio_guest_run, schedule_on_asyncio

import traceback
from queue import Queue

import win32api
import win32con
import win32gui

import asyncio
from webview import Webview, SizeHint, Size

import os

ASYNCIO_MSG = win32con.WM_APP + 3

# 使用线程安全的 Queue 代替 deque
trio_functions = Queue()

def do_trio():
    """Process all pending trio tasks in the queue"""
    while not trio_functions.empty():
        try:
            # 获取并执行一个任务
            func = trio_functions.get()
            func()
        except Exception as e:
            print(rf"{__file__}:{do_trio.__name__} e: {e}")
            print(traceback.format_exc())
            raise e

class WebviewHost:
    def __init__(self, webview):
        self.webview = webview
        self.mainthreadid = win32api.GetCurrentThreadId()
        # create event queue with null op
        win32gui.PeekMessage(
            win32con.NULL, win32con.WM_USER, win32con.WM_USER, win32con.PM_NOREMOVE
        )
        self.create_message_window()

    def create_message_window(self):
        # 注册窗口类
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.trio_wndproc_func
        wc.lpszClassName = "TrioMessageWindow"
        win32gui.RegisterClass(wc)
        
        # 创建隐藏窗口
        self.msg_hwnd = win32gui.CreateWindowEx(
            0, "TrioMessageWindow", "Trio Message Window",
            0, 0, 0, 0, 0, 0, 0, None, None
        )

    def trio_wndproc_func(self, hwnd, msg, wparam, lparam):
        if msg == ASYNCIO_MSG:
            # 处理所有排队的 trio 任务
            do_trio()
            return 0
        # elif msg == DESTROY_WINDOW_MSG:
        #     # 在正确的线程中销毁窗口
        #     win32gui.DestroyWindow(hwnd)
        #     return 0
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def run_sync_soon_threadsafe(self, func):
        """先添加函数到队列，后发送消息"""
        trio_functions.put(func)
        win32api.PostMessage(self.msg_hwnd, ASYNCIO_MSG, 0, 0)

    def run_sync_soon_not_threadsafe(self, func):
        """与 threadsafe 相同，保持一致性"""
        trio_functions.put(func)
        win32api.PostMessage(self.msg_hwnd, ASYNCIO_MSG, 0, 0)

    def done_callback(self, result):
        """non-blocking request to end the main loop"""
        print(f"Main Task Result: {result}")
        if isinstance(result, Exception):
            exc=result
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            exitcode = 1
        elif isinstance(result, BaseException):
            # TODO: special case for asyncio.CancelledError and other BaseException?
            exitcode = 1
        else:
            exitcode = 0
        self.display.dialog.PostMessage(win32con.WM_CLOSE, 0, 0)
        self.display.dialog.close()
        # 通过消息请求主线程销毁窗口
        # win32api.PostMessage(self.msg_hwnd, DESTROY_WINDOW_MSG, 0, 0)
        win32gui.PostQuitMessage(exitcode)

    def mainloop(self):
        self.webview.run()

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

async def counter():
    count = 0   
    while True:
        await asyncio.sleep(5)
        count += 1
        print(f"counter: {count}")

if __name__ == "__main__":       # Create webview instance
    webview = Webview(debug=True)

    # Bind Python functions
    webview.bind("delayedResponse", delayed_response)
    webview.bind("processWithProgress", process_with_progress)
    webview.bind("fetchData", fetch_data)

    webview.title = "Python-JavaScript 异步绑定演示"
    webview.size = Size(800, 600, SizeHint.NONE)

    # Get the absolute path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'bind_in_local_async.html')

    # Load the local HTML file
    webview.navigate(f"file://{html_path}")

    # --begin-- guest run
    host = WebviewHost(webview)
    asyncio_guest_run(
        counter,
        run_sync_soon_threadsafe=host.run_sync_soon_threadsafe,
        run_sync_soon_not_threadsafe=host.run_sync_soon_not_threadsafe,
        done_callback=host.done_callback,
    )
    host.mainloop()
    # --end-- guest run
