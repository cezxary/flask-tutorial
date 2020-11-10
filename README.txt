Wanting to make the app uWSGI-friendly, 
uWSGI needs the directory to the file with Flask app.

Possibilities to run uWSGI app:

1. When app is contained within a module:
[bash]
uwsgi --http :5000 --module app_name:app

the module containing the app is 'app_name', and 'app' indicates the global variable in the __init__.py of that module.
[__init__.py]
from flask import flask

app = Flask(__name__)


2. When app is contained within an app factory within a module:
[bash]
uwsgi --http :5000 --module app_name:app_returned
OR
[bash]
uwsgi --http :5000 --mount /flaskr=flaskr:app_returned

[__init__.py]
from flask import Flask

def create_app():
    app = Flask(__name__)

    # other contents of the file, app configuretion etc.
    return app

app_returned = create_app()


3. When app is contained within singular file:
[bash]
uwsgi --http :5000 --wsgi-file wsgi_file.py --callable 

[__init__.py]
from flask import Flask
app = Flask(__name__)
@app.route('/hello')
def hello():
    return 'Hello, World!'


Aswell, it's good to read this piece: https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/