import unittest
from python_webview import Webview, Size, SizeHint

class TestWebview(unittest.TestCase):
    def test_create_webview(self):
        webview = Webview()
        self.assertIsNotNone(webview)

    def test_set_size(self):
        webview = Webview()
        size = Size(800, 600, SizeHint.NONE)
        webview.size = size
        self.assertEqual(webview.size, size)

    def test_set_title(self):
        webview = Webview()
        title = "Test Title"
        webview.title = title
        self.assertEqual(webview.title, title)

if __name__ == '__main__':
    unittest.main()
