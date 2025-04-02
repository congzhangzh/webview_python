import ctypes
import sys
import os
import platform
import urllib.request
from pathlib import Path
from ctypes import c_int, c_char_p, c_void_p, CFUNCTYPE
import ctypes.util
import shutil

def _encode_c_string(s: str) -> bytes:
    return s.encode("utf-8")

def _get_webview_version():
    """Get webview version from environment variable or use default"""
    return os.getenv("WEBVIEW_VERSION", "0.9.0")

def _get_download_base():
    """Get download base URL or path from environment variable or use default.
    
    This allows users to specify a custom location (URL or file path) to download
    libraries from, which is particularly useful for internal deployments or 
    offline environments.
    
    Returns:
        str: The base URL or path for downloading libraries
    """
    return os.getenv(
        "WEBVIEW_DOWNLOAD_BASE", 
        "https://github.com/webview/webview_deno/releases/download"
    )

def _get_lib_names():
    """Get platform-specific library names."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if machine == "amd64" or machine == "x86_64":
            return ["webview.dll", "WebView2Loader.dll"]
        elif machine == "arm64":
            raise Exception("arm64 is not supported on Windows")
    elif system == "darwin":
        if machine == "arm64":
            return ["libwebview.aarch64.dylib"]
        else:
            return ["libwebview.x86_64.dylib"]
    else:  # linux
        if machine == "aarch64" or machine == "arm64":
            return ["libwebview.aarch64.so"]
        else:
            return ["libwebview.x86_64.so"]

def _get_download_urls():
    """Get the appropriate download URLs based on the platform."""
    version = _get_webview_version()
    base_url = _get_download_base()
    
    # Handle both URL and file path formats
    if base_url.startswith(("http://", "https://", "file://")):
        # For URLs, use / separator
        return [f"{base_url}/{version}/{lib_name}" 
                for lib_name in _get_lib_names()]
    else:
        # For file paths, use OS-specific path handling
        base_path = Path(base_url)
        return [str(base_path / version / lib_name)
                for lib_name in _get_lib_names()]

def _be_sure_libraries():
    """Ensure libraries exist and return paths."""
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(sys.executable).parent / '_internal'
    else:
        base_dir = Path(__file__).parent
    
    lib_dir = base_dir / "lib"
    lib_names = _get_lib_names()
    lib_paths = [lib_dir / lib_name for lib_name in lib_names]
    
    # Check if any library is missing
    missing_libs = [path for path in lib_paths if not path.exists()]
    if not missing_libs:
        return lib_paths

    # Download or copy missing libraries
    download_urls = _get_download_urls()
    system = platform.system().lower()
    
    lib_dir.mkdir(parents=True, exist_ok=True)
    
    for url, lib_path in zip(download_urls, lib_paths):
        if lib_path.exists():
            continue
            
        print(f"Getting library from {url}")
        try:
            # Handle different URL types
            if url.startswith(("http://", "https://")):
                # Web URL - download
                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response, open(lib_path, 'wb') as out_file:
                    out_file.write(response.read())
            elif url.startswith("file://"):
                # File URL - copy from local filesystem
                source_path = url[7:]  # Strip 'file://' prefix
                shutil.copy2(source_path, lib_path)
            else:
                # Assume it's a filesystem path
                source_path = url
                if os.path.exists(source_path):
                    shutil.copy2(source_path, lib_path)
                else:
                    raise FileNotFoundError(f"Could not find library at {source_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to get library from {url}: {e}")
    
    return lib_paths

class _WebviewLibrary:
    def __init__(self):
        lib_names=_get_lib_names()
        try:
            library_path = ctypes.util.find_library(lib_names[0])
            if not library_path:
                library_paths = _be_sure_libraries()
            self.lib = ctypes.cdll.LoadLibrary(str(library_paths[0]))
        except Exception as e:
            print(f"Failed to load webview library: {e}")
            raise
        # Define FFI functions
        self.webview_create = self.lib.webview_create
        self.webview_create.argtypes = [c_int, c_void_p]
        self.webview_create.restype = c_void_p

        self.webview_destroy = self.lib.webview_destroy
        self.webview_destroy.argtypes = [c_void_p]

        self.webview_run = self.lib.webview_run
        self.webview_run.argtypes = [c_void_p]

        self.webview_terminate = self.lib.webview_terminate
        self.webview_terminate.argtypes = [c_void_p]

        self.webview_set_title = self.lib.webview_set_title
        self.webview_set_title.argtypes = [c_void_p, c_char_p]

        self.webview_set_size = self.lib.webview_set_size
        self.webview_set_size.argtypes = [c_void_p, c_int, c_int, c_int]

        self.webview_navigate = self.lib.webview_navigate
        self.webview_navigate.argtypes = [c_void_p, c_char_p]

        self.webview_init = self.lib.webview_init
        self.webview_init.argtypes = [c_void_p, c_char_p]

        self.webview_eval = self.lib.webview_eval
        self.webview_eval.argtypes = [c_void_p, c_char_p]

        self.webview_bind = self.lib.webview_bind
        self.webview_bind.argtypes = [c_void_p, c_char_p, c_void_p, c_void_p]

        self.webview_unbind = self.lib.webview_unbind
        self.webview_unbind.argtypes = [c_void_p, c_char_p]

        self.webview_return = self.lib.webview_return
        self.webview_return.argtypes = [c_void_p, c_char_p, c_int, c_char_p]

        self.CFUNCTYPE = CFUNCTYPE

_webview_lib = _WebviewLibrary()
