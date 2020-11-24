# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:24:39 2020

@author: cezxary
"""
import pytest
from flaskr.db import get_db


def test_show_post(auth, client):
    auth.login()
    response = client.get('/post/1')
    assert b"<h1>test title</h1>" in response.data
    
    
def test_show_post_logged_out(client):
    response = client.get('/post/1')
    assert b"<h1>test title</h1>" in response.data
    
    
@pytest.mark.parametrize('path', (
    '/post/1/like',
    '/post/1/unlike'))
def test_login_required(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'
    

def test_like_post(auth, client, app):
    auth.login()
    
    response = client.get('/post/1/like')
    assert response.headers['Location'] == 'http://localhost/post/1'
    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM likes'
            ' WHERE user_id = 1 AND post_id = 1'
        ).fetchone() is not None            


def test_like_new_post(auth, client, app):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO post (id, title, body, author_id)'
                   ' VALUES (2, "new post", "test", 2)')
        
    auth.login()
    response = client.get('post/2/like')
    assert response.headers['Location'] == 'http://localhost/post/2'


def test_unlike_post(auth, client, app):
    auth.login()
    
    response = client.get('/post/1/unlike')
    assert response.headers['Location'] == 'http://localhost/post/1'
    
    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM likes'
            ' WHERE user_id = 1 AND post_id = 1'
        ).fetchone() is None


def test_unliked(auth, client, app):
    with app.app_context():
        db = get_db()
        db.execute('DELETE FROM likes'
            ' WHERE user_id = 1 AND post_id = 1'
        )
        db.commit()
    
    auth.login()
    
    response = client.get('/post/1')
    assert b'Like</a>' in response.data    

