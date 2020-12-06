# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 20:53:32 2020

@author: czare
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('tag', __name__)

@bp.route('/tag/<tagname>', methods=('GET',))
def show_tag(tagname):
    db = get_db()
    
    posts = db.execute(
        "SELECT p.title, u.username, p.created, p.body, p.author_id, p.id"
        " FROM post_taglist ptl"
        " JOIN post p ON ptl.post_id = p.id"
        " JOIN user u ON p.author_id = u.id"
        " JOIN tag t ON ptl.tag_id = t.id"
        " WHERE t.name = ?", (tagname, )
    ).fetchall()
    
    return render_template('tag/tag.html', posts=posts, tagname=tagname)