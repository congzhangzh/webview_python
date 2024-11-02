from webview import Webview
from urllib.parse import quote

html = """
<html>
<body>
  <h1>Hello from Python Webview!</h1>
</body>
</html>
"""

webview = Webview()
webview.navigate(f"data:text/html,{quote(html)}")
webview.run()
