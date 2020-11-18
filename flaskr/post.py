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


# TODO: known issue - sending multiple post requests results in registering one
# comment multiple times - would be best to check if incoming comment has
# the same body as the last one.
@bp.route('/post/<int:id>', methods=('GET',))
def show_post(id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchone()
    
    comments = db.execute(
        'SELECT p.id, c.body, c.created, author_id, username'
        ' FROM comment c '
        ' JOIN post p ON c.post_id = p.id'
        ' JOIN user u ON c.user_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchall()
    
    return render_template('post/show_post.html', post=post, liked=liked(id), comments=comments)


def liked(id):
    db = get_db()

    try:
        is_liked = db.execute(
            'SELECT * FROM likes'
            ' WHERE user_id = ? AND post_id = ?', (g.user['id'], id)
        ).fetchone()
    except TypeError: 
        # if user is not logged in, g.user['id
        is_liked = None
    
    if is_liked:
        return True
    else:
        return False
    

@bp.route('/post/<int:id>/like', methods=('GET',))
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


@bp.route('/post/<int:id>/unlike', methods=('GET',))
@login_required
def unlike_post(id):
    db = get_db()
    db.execute(
        "DELETE FROM likes"
        " WHERE user_id = ? AND post_id = ?", (g.user['id'], id)
    )
    db.commit()
    return redirect(url_for("post.show_post", id=id))