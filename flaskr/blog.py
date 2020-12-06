# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:26:02 2020

@author: cezxary
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ).fetchall()
    return render_template('blog/index.html', posts=posts)


def extract_tags(tags):
    taglist = tags.split('#')
    taglist = [tag.strip() for tag in taglist if len(tag.strip()) > 0]
    taglist = [tag.replace(' ', '_') for tag in taglist]
    return taglist


def add_tag(post_id, tag):
    db = get_db()
    
    db.execute(
        'INSERT OR IGNORE INTO tag (name) VALUES (?)', (tag,)
    )
    
    tag_id = db.execute(
        'SELECT id'
        ' FROM tag'
        ' WHERE name = ?', (tag,)
    ).fetchone()
    db.execute(
        'INSERT OR IGNORE INTO post_taglist (post_id, tag_id)'
        ' VALUES (?, ?)', (post_id, tag_id['id'])
    )
    db.commit()


def extract_and_add_tags(post_id, tags):
    taglist = extract_tags(tags)

    for tag in taglist:
        add_tag(post_id, tag)
    


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = request.form['tags']
        error = None
        
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES(?, ?, ?)', (title, body, g.user['id'])
            )
            db.commit()
            
            # find last post, so tag and post_taglist tables in DB 
            # could be updated
            last_post = db.execute(
                'SELECT MAX(id) as last_id'
                ' FROM post'
                ' WHERE author_id = ?', (g.user['id'],)
            ).fetchone()
            
            extract_and_add_tags(last_post['last_id'], tags)
            
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    if post is None:
        abort(404, 'Post id {0} doesn\'t exist'.format(id))
        
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
        
    return post


def get_tags(id):
    tags = get_db().execute(
        'SELECT t.name'
        ' FROM post_taglist ptl'
        ' JOIN tag t ON ptl.tag_id = t.id'
        ' JOIN post p ON ptl.post_id = p.id'
        ' WHERE p.id = ?', (id, )
    ).fetchall()
    return [tag['name'] for tag in tags]


def delete_post_tag(post_id, tag_name):
    db = get_db()
    
    tag_id = db.execute(
        'SELECT id FROM tag WHERE name = ?', (tag_name,)
    ).fetchone()['id']
    
    db.execute('DELETE FROM post_taglist'
               ' WHERE post_id = ? AND tag_id = ?', (post_id, tag_id))
    db.commit()


def update_tags(post_id, old_taglist, new_tags):
    new_taglist = extract_tags(new_tags)
    
    tags_out_of_date = [tag_name for tag_name in old_taglist 
                        if tag_name not in new_taglist]
    for tag_name in tags_out_of_date:
        delete_post_tag(post_id, tag_name)
    
    for tag_name in new_taglist:
        add_tag(post_id, tag_name)


@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id):
    post = get_post(id)
    taglist = get_tags(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_tags = request.form['tags']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?', 
                (title, body, id)
            )
            db.commit()
            
            update_tags(id, taglist, new_tags)
            
            return redirect(url_for('blog.index'))
        
    return render_template('blog/update.html', post=post, taglist=taglist)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
