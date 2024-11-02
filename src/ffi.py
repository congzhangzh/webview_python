import ctypes
import sys
import os
import platform
import urllib.request
from pathlib import Path
from ctypes import c_int, c_char_p, c_void_p, CFUNCTYPE
import ctypes.util

def _encode_c_string(s: str) -> bytes:
    return s.encode("utf-8")

def _get_webview_version():
    """Get webview version from environment variable or use default"""
    return os.getenv("WEBVIEW_VERSION", "0.8.1")

def _get_lib_name():
    """Get platform-specific library name."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # ref: https://github.com/webview/webview_deno/releases/tag/0.8.1/
    if system == "windows":
        if machine == "amd64" or machine == "x86_64":
            return "webview.dll"
        elif machine == "arm64":
            raise Exception("arm64 is not supported on Windows")
    elif system == "darwin":
        if machine == "arm64":
            return "libwebview.aarch64.dylib"
        else:
            return "libwebview.x86_64.dylib"
    else:  # linux
        return "libwebview.so"

def _get_download_url():
    """Get the appropriate download URL based on the platform."""
    version = _get_webview_version()
    lib_name = _get_lib_name()
    return f"https://github.com/webview/webview_deno/releases/download/{version}/{lib_name}"

def _be_sure_library():
    """Ensure library exists and return path."""
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):  # onefile 模式
            base_dir = Path(sys._MEIPASS)
        else:  # onedir 模式
            base_dir = Path(sys.executable).parent / '_internal'
    else:
        base_dir = Path(__file__).parent
    
    lib_dir = base_dir / "lib"
    lib_name = _get_lib_name()
    lib_path = lib_dir / lib_name

    if lib_path.exists():
        return lib_path

    """Download the webview library."""
    download_url = _get_download_url()
    system = platform.system().lower()
        
    lib_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading webview library from {download_url}")
    
    try:
        # Create a request with a user agent to avoid GitHub raw content restrictions
        req = urllib.request.Request(
            download_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(lib_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        raise RuntimeError(f"Failed to download webview library: {e}")
    
    # Make the library executable on Unix-like systems
    if system != "windows":
        lib_path.chmod(lib_path.stat().st_mode | 0o755)
    
    return lib_path

class _WebviewLibrary:
    def __init__(self):
        lib_name=_get_lib_name()
        try:
            library_path = ctypes.util.find_library(lib_name)
            if not library_path:
                library_path = _be_sure_library()
            self.lib = ctypes.cdll.LoadLibrary(library_path)
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
