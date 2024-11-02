from webview import Webview
import os

# Create webview instance
webview = Webview(debug=True)

# Get the absolute path to the HTML file
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'local.html')

# Load the local HTML file
webview.navigate(f"file://{html_path}")

# Run the webview
webview.run() 
