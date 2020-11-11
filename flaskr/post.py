# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:52:15 2020

@author: cezxary
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('post', __name__)


@bp.route('/post/<int:id>', methods=['GET'])
def show_post(id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)).fetchone()
        
    return render_template('post/show_post.html', post=post, liked=liked(id))


def liked(id):
    db = get_db()
    is_liked = db.execute(
        'SELECT * FROM likes'
        ' WHERE user_id = ? AND post_id = ?', (g.user['id'], id)
    ).fetchone()
    
    if is_liked:
        return True
    else:
        return False
    

@bp.route('/post/<int:id>/like')
@login_required
def like_post(id):
    db = get_db()
    is_liked = liked(id)
    if is_liked is False:    
        db.execute(
            "INSERT INTO likes (user_id, post_id)"
            " VALUES (?, ?)", (g.user['id'], id)
            )
        db.commit()
    return redirect(url_for("post.show_post", id=id))


@bp.route('/post/<int:id>/unlike')
@login_required
def unlike_post(id):
    db = get_db()
    db.execute(
        "DELETE FROM likes"
        " WHERE user_id = ? AND post_id = ?", (g.user['id'], id)
        )
    db.commit()
    return redirect(url_for("post.show_post", id=id))
    