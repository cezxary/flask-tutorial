# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:37:54 2020

@author: cezxary
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
