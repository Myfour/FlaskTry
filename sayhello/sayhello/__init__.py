from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

app = Flask('sayhello')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)
# 之所以定义在结尾是为了避免循环依赖
from sayhello import views, errors, commands, models, forms
