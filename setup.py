from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            name='webview._platform_binary',
            sources=[],
        )
    ],
) 