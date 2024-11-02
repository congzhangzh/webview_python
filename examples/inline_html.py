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
