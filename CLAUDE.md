# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `webview_python`, a Python library providing bindings for the webview library to create desktop applications with web technologies. The project follows the deno_webview design principles and supports cross-platform development (Windows, macOS, Linux).

## Development Commands

### Testing
```bash
# Run all tests
python -m unittest discover tests
# or
pytest

# Run tests with coverage
pytest --cov
```

### Building
```bash
# Install build dependencies
pip install -r requirements.txt

# Build wheel packages
python -m build -n -w

# Build source distribution
python -m build -n -s
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Project Architecture

### Core Structure
- `src/webview/webview.py` - Main Webview class and API implementation
- `src/webview/_webview_ffi.py` - Foreign Function Interface for native webview library
- `src/webview/__init__.py` - Package initialization

### Key Components

**Webview Class**: Main interface providing:
- Window creation and management
- JavaScript-Python bidirectional binding
- Async function support for long-running operations
- Window sizing, title, and navigation control

**FFI Layer**: Handles native library loading and C API bindings, with automatic platform detection and library downloading from GitHub releases or custom locations.

**Async Support**: Built-in support for async Python functions callable from JavaScript, enabling non-blocking operations and progress reporting.

### Environment Variables
- `WEBVIEW_VERSION`: Specify webview library version (default: "0.9.0")
- `WEBVIEW_DOWNLOAD_BASE`: Custom download location for webview libraries

### Examples Structure
- `examples/` - Comprehensive examples including basic usage, async operations, and framework integrations
- `examples/async_with_asyncio_guest_run/` - Advanced async examples with asyncio integration

## Testing Architecture

Tests are located in `tests/` directory:
- `test_webview.py` - Core webview functionality tests
- `test_library.py` - Library loading and FFI tests

## Release Process

Version management through `pyproject.toml`. GitHub Actions handles automated testing and PyPI publishing on tag creation. Manual release steps documented in README.md.