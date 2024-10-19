import ctypes
from ctypes import c_int, c_char_p, c_void_p, CFUNCTYPE

def encode_c_string(value: str) -> bytes:
    return value.encode('utf-8') + b'\0'

class Library:
    def __init__(self):
        self.lib = ctypes.cdll.LoadLibrary("libwebview.so")  # Adjust for different platforms

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

lib = Library()
