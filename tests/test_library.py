import unittest
from ffi import _webview_lib

class TestLibrary(unittest.TestCase):
    def test_library_load(self):
        """Test that the library can be loaded successfully"""
        try:
            lib = _webview_lib
            self.assertIsNotNone(lib)
        except Exception as e:
            self.fail(f"Failed to load library: {e}")

if __name__ == '__main__':
    unittest.main() 