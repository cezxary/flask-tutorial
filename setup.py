# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:03:52 2020

@author: cezxary
"""
from setuptools import setup, find_packages

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)