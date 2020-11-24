# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 22:00:23 2020

@author: czare
"""
import pytest
from flaskr.db import get_db


def test_get_comment(client, auth):
    auth.login()
    
    response = client.get('/post/1/comment')
    assert b'test comment' in response.data


def test_get_comment_login_required(client):
    response = client.get('/post/1/comment')
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_post_comment(client, auth):
    auth.login()
    
    client.post('/post/1/comment', data = {'body': 'new comment'})
    response = client.get('/post/1')
    assert b'new comment' in response.data
   
    
def test_post_comment_login_required(client):
    response = client.post('/post/1/comment', data = {'body': 'new comment'})
    assert response.headers['Location'] == 'http://localhost/auth/login'
    

def test_post_comment_empty(client, auth):
    auth.login()
    response = client.post('/post/1/comment', data = {'body': ''})
    assert b'You should put some text in the comment!' in response.data
    
    

    