#!/usr/bin/env python3
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="typedmodel",
    version="0.2.6",
    description="provide strict type checking for dataclass and pydantic model",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/qiujiangkun/typedmodel",
    author="Jiangkun QIU",
    author_email="qjk2001@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["typedmodel"],
    include_package_data=True,
    install_requires=["beartype"],
    entry_points={},
)
