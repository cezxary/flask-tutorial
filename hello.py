# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:47:07 2020

@author: cezxary
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'