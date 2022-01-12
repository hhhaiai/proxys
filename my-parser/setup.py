#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from setuptools import setup
# or
# from distutils.core import setup

setup(
        name='ps',     # 包名字
        version='1.0',   # 包版本
        description='This is a parser',   # 简单描述
        author='sanbo',  # 作者
        author_email='sanbo.xyz@gmail.com',  # 作者邮箱
        # url='https://www.konghy.com',      # 包的主页
        # packages=['demo'],                 # 包
    python_requires='>=3',
    install_requires=[
            'urllib3',
            'requests',
            'six',
            'cython',
            'numpy',
            'bs4',
            'beautifulsoup4',
            'certifi',
            'cffi',
            'openpyxl',
            'pandas',
            'progressbar',
            'pycparser',
            'pyOpenSSL',
            'python-dateutil',
            'selenium',
            'sortedcontainers',
            'soupsieve',
            'wsproto',
            'attrs',
        ],

    # 私有源依赖
    # dependency_links=[
    #     'https://pypi.python.org/simple',
    #     'http://my.company.com/pypi/',
    #     ...
    # ],
)