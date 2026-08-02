from setuptools import setup, find_packages

setup(
    name="repointel",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "requests>=2.31.0",
        "rich>=13.7.1"
    ],
    entry_points={
        "console_scripts": [
            "repointel=repointel.main:cli",
        ],
    },
)
