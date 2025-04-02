from webview.webview import Webview, Size, SizeHint
from urllib.parse import quote
import json

# 创建Webview实例
webview = Webview(debug=True)
webview.title = "Preact与Python交互示例"
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

# HTML内容
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preact与Python交互示例</title>
    <style>
        body { 
            font-family: system-ui, sans-serif; 
            max-width: 500px; 
            margin: 0 auto; 
            padding: 2rem; 
            text-align: center;
        }
        button {
            margin: 0 0.5rem;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
        }
        .counter {
            font-size: 2rem;
            margin: 2rem 0;
        }
        .loading {
            opacity: 0.5;
        }
        .error {
            color: red;
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <div id="app"></div>

    <script type="module">
        import { h, render } from 'https://esm.sh/preact';
        import { useState, useEffect } from 'https://esm.sh/preact/hooks';
        import htm from 'https://esm.sh/htm';

        // 初始化htm与Preact
        const html = htm.bind(h);

        function Counter() {
            const [count, setCount] = useState(null);
            const [loading, setLoading] = useState(true);
            const [updating, setUpdating] = useState(false);
            const [error, setError] = useState(null);
            
            // 从Python获取计数
            const fetchCount = async () => {
                try {
                    setLoading(true);
                    setError(null);
                    const result = await getCount();
                    setCount(result);
                } catch (err) {
                    setError('获取计数失败: ' + err.message);
                    console.error('获取计数错误:', err);
                } finally {
                    setLoading(false);
                }
            };
            
            // 初始加载
            useEffect(() => {
                fetchCount();
            }, []);
            
            // 增加计数 - 处理异步
            const handleIncrement = async () => {
                try {
                    setUpdating(true);
                    setError(null);
                    const newCount = await increment();
                    setCount(newCount);
                } catch (err) {
                    setError('增加计数失败: ' + err.message);
                    console.error('增加计数错误:', err);
                } finally {
                    setUpdating(false);
                }
            };
            
            // 减少计数 - 处理异步
            const handleDecrement = async () => {
                try {
                    setUpdating(true);
                    setError(null);
                    const newCount = await decrement();
                    setCount(newCount);
                } catch (err) {
                    setError('减少计数失败: ' + err.message);
                    console.error('减少计数错误:', err);
                } finally {
                    setUpdating(false);
                }
            };
            
            // 显示加载状态
            if (loading) {
                return html`<div>加载中...</div>`;
            }
            
            return html`
                <div class=${updating ? 'loading' : ''}>
                    <h1>Preact计数器示例</h1>
                    <p>通过Python后端管理状态（异步通信）</p>
                    
                    <div class="counter">${count !== null ? count : '...'}</div>
                    
                    ${error && html`<div class="error">${error}</div>`}
                    
                    <div>
                        <button 
                            onClick=${handleDecrement} 
                            disabled=${updating}
                        >
                            减少
                        </button>
                        <button 
                            onClick=${handleIncrement} 
                            disabled=${updating}
                        >
                            增加
                        </button>
                    </div>
                </div>
            `;
        }
        
        // 渲染应用
        render(html`<${Counter} />`, document.getElementById('app'));
    </script>
</body>
</html>
"""

webview.navigate(f"data:text/html,{quote(html)}")
webview.run()
