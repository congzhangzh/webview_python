import os
from urllib.parse import quote

from webview import Webview, SizeHint, Size

# # Create HTML with JavaScript that calls Python functions
html = """
<html lang="zh">
<head>
    <title>Python-JavaScript Binding Demo</title>
    <script>
        // 定义所有的 JavaScript 函数
        async function callPython() {
            try {
                const result = await hello();
                document.getElementById('result').innerHTML = result;
            } catch (err) {
                console.error('Error calling Python:', err);
            }
        }

        async function callPythonWithArgs() {
            try {
                const result = await add(40, 2);
                document.getElementById('result').innerHTML = `Result: ${result}`;
            } catch (err) {
                console.error('Error calling Python:', err);
            }
        }

        function updateFromPython(message) {
            document.getElementById('result').innerHTML = `Python says: ${message}`;
        }
    </script>
</head>
<body>
    <h1>Python-JavaScript Binding Demo</h1>
    
    <button onclick="callPython()">Call Python</button>
    <button onclick="callPythonWithArgs()">Call Python with Args</button>
    
    <div id="result"></div>
</body>
</html>
"""

# Create webview instance
webview = Webview(debug=True)

# Define Python functions to be called from JavaScript
def hello():
    # Call JavaScript from Python
    webview.eval("updateFromPython('Hello from Python!')")
    return "Hello from Python!"

def add(a, b):
    result = a + b
    return result

# Bind Python functions
webview.bind("hello", hello)
webview.bind("add", add)

webview.title = "Python-JavaScript Binding Demo"
webview.size = Size(640, 480, SizeHint.FIXED)

# Get the absolute path to the HTML file
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'local_use_bind.html')


# Load the inline HTML
webview.navigate(f"data:text/html,{quote(html)}")

# Run the webview
webview.run()
