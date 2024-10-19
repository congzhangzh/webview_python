# Python Webview

Python bindings for the webview library, allowing you to create desktop applications with web technologies.

## Installation
bash
pip install python-webview

## Usage

### Local HTML
```python
from python_webview import Webview
html = """
<html>
<body>
<h1>Hello from Python Webview!</h1>
</body>
</html>
"""
webview = Webview()
webview.navigate(f"data:text/html,{html}")
webview.run()
webview = Webview()
webview.navigate(f"data:text/html,{html}")
webview.run()
```
### Remote URL
```python
from python_webview import Webview
webview = Webview()
webview.navigate("https://www.python.org")
webview.run()
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
