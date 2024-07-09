from setuptools import setup, find_packages

setup(
    name="scanner-backend",
    version="1.0.0",
    description="Scanner Backend",
    url="https://github.com/politicalwatch/scanner-backend",
    author="pr3ssh",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-restx",
    ],
)
