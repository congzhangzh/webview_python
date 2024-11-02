import os
from webview import Webview, SizeHint, Size

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
html_path = os.path.join(current_dir, 'bind_in_local.html')

# Load the local HTML file
webview.navigate(f"file://{html_path}")

# Run the webview
webview.run()
