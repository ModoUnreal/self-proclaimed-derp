from app import db, app
from app.models import User, Post, Comment
from flask import url_for
from waitress import serve
import os


@app.shell_context_processor
def make_shell_context():
    """Makes the shell context, allowing for specific variables, and classes
       to be known by the interactive Python session on startup."""
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment}

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
