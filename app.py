from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = './tmp/'
ALLOWED_EXTENSIONS = ('txt',)

db = SQLAlchemy(app)

import models
