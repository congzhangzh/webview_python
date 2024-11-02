# Python Webview

Python bindings for the webview library, allowing you to create desktop applications with web technologies.

## Installation
bash
pip install webview

## Usage

### Local HTML
```python
from webview import Webview
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
```
### Remote URL
```python
from python_webview import Webview
webview = Webview()
webview.navigate("https://www.python.org")
webview.run()
```

### Bindings

TBD

# TODO
- [ ] Add bind example
- [ ] Polish README.md
- [ ] Publish to PyPI
- [ ] Use github actions to build and publish to PyPI when new tag is pushed
- [ ] Add preact example
- [ ] Add three.js example
- [ ] Add three.js fiber example
- [ ] Add screen saver 4 window example
- [ ] Add MRI principle demo example by three.js fiber
- [ ] Add screen saver 4 windows with MRI principle demo example by three.js fiber

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
