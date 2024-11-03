# Webview Python

[![Test - Windows](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml/badge.svg?branch=main&event=push&label=Windows)](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml)
[![Test - Linux](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml/badge.svg?branch=main&event=push&label=Linux)](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml)
[![Test - macOS](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml/badge.svg?branch=main&event=push&label=macOS)](https://github.com/congzhangzh/webview_python/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/webview_python.svg)](https://badge.fury.io/py/webview_python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/webview_python.svg)](https://pypi.org/project/webview_python/)

Python bindings for the webview library, allowing you to create desktop applications with web technologies.

## Installation

```bash
pip install webview_python
```

## Usage

### Display Inline HTML:

```python
from webview.webview import Webview
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
```

### Load Local HTML File:

```python
from webview.webview import Webview
import os

webview = Webview()
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'local.html')
webview.navigate(f"file://{html_path}")
webview.run()
```

### Load Remote URL:

```python
from webview.webview import Webview
webview = Webview()
webview.navigate("https://www.python.org")
webview.run()
```

### Python-JavaScript Bindings:

```python
from webview.webview import Webview, Size, SizeHint
from urllib.parse import quote

webview = Webview(debug=True)

# Python functions that can be called from JavaScript
def hello():
    webview.eval("updateFromPython('Hello from Python!')")
    return "Hello from Python!"

def add(a, b):
    return a + b

# Bind Python functions
webview.bind("hello", hello)
webview.bind("add", add)

# Configure window
webview.title = "Python-JavaScript Binding Demo"
webview.size = Size(640, 480, SizeHint.FIXED)

# Load HTML with JavaScript
html = """
<html>
<head>
    <title>Python-JavaScript Binding Demo</title>
    <script>
        async function callPython() {
            const result = await hello();
            document.getElementById('result').innerHTML = result;
        }

        async function callPythonWithArgs() {
            const result = await add(40, 2);
            document.getElementById('result').innerHTML = `Result: ${result}`;
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

webview.navigate(f"data:text/html,{quote(html)}")
webview.run()
```

## Features

- Create desktop applications using HTML, CSS, and JavaScript
- Load local HTML files or remote URLs
- Bidirectional Python-JavaScript communication
- Window size and title customization
- Debug mode for development
- Cross-platform support (Windows, macOS, Linux)

## Development

### Setup Development Environment

```bash
# Install Python build tools
pip install --upgrade pip build twine

# Install GitHub CLI (choose one based on your OS):
# macOS
brew install gh

# Windows
winget install GitHub.cli
# or
choco install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh
```

### Running Tests

```bash
python -m unittest discover tests
```

### Project Structure

```
webview_python/
├── src/
│   ├── webview.py      # Main webview implementation
│   └── ffi.py          # Foreign Function Interface
├── examples/           # Example applications
├── tests/             # Unit tests
└── README.md          # Documentation
```

### Release Process

For maintainers who want to release a new version:
1. **Test**
```bash
# Install dependencies if not installed 
pip install -r requirements.txt

# Run tests
pytest

# Build wheels
python -m build -n -w
```

2. **Update Version**
   ```bash
   # Ensure you have the latest code
   git pull origin main
   
   # Update version in pyproject.toml
   # Edit version = "x.y.z" to new version number
   ```

3. **Create Release**
   ```bash
   # Commit changes
   old_version=0.99.0
   new_version=0.99.1
   git add pyproject.toml
   git commit -m "Bump version to ${new_version}"
   git push origin main

   # Create and push tag
   git tag v${new_version}
   git push origin v${new_version}

   # Create GitHub release
    gh release create v${new_version} --title "${new_version}" \
        --notes "Full Changelog: https://github.com/congzhangzh/webview_python/compare/v${old_version}...v${new_version}"
   ```

4. **Monitor Release**
   - Check GitHub Actions progress in the Actions tab
   - Verify package on PyPI after workflow completion

### First-time Release Setup

1. **PyPI Setup**
   - Create account: https://pypi.org/account/register/
   - Generate API token: https://pypi.org/manage/account/token/

2. **GitHub Setup**
   - Repository Settings → Secrets and variables → Actions
   - Add new secret: `PYPI_API_TOKEN` with PyPI token value

## Roadmap

- [ ] Publish to PyPI
- [ ] Setup GitHub Actions for CI/CD
- [ ] Add preact example
- [ ] Add three.js example
- [ ] Add three.js fiber example
- [ ] Add screen saver 4 window example
- [ ] Add MRI principle demo example by three.js fiber
- [ ] Add screen saver 4 windows with MRI principle demo example by three.js fiber

## References

- [Webview](https://github.com/webview/webview)
- [webview_deno](https://github.com/eliassjogreen/webview_deno)

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
