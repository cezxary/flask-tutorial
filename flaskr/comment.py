# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:09:45 2020

@author: cezxary
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('comment', __name__, template_folder='templates/post/')


@bp.route('/post/<int:id>/comment', methods=('GET','POST'))
@login_required
def comment(id):
    if request.method == 'POST':
        comment_body = request.form['body']
        error = None
        db = get_db()
        
        if not (len(comment_body) > 0):
            error = 'You should put some text in the comment!'
        
        if error is None:
            db.execute(
                'INSERT INTO comment (body, post_id, user_id)'
                ' VALUES (?, ?, ?)', (comment_body, id, g.user['id'])
            )
            db.commit()
            
            return redirect(url_for('post.show_post', id=id))
        
        flash(error)
    
    db = get_db()
    
    post = db.execute(
        'SELECT * FROM post'
        ' WHERE id = ?', (id,)
    ).fetchone()
    
    comments = db.execute(
        'SELECT p.id, c.body, c.created, u.username FROM post p'
        ' JOIN comment c ON p.id = c.post_id'
        ' JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchall()
    
    return render_template('post/comment.html', post=post, comments=comments)