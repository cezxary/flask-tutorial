# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:52:44 2020

@author: cezxary
"""
from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'