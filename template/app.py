from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}
movies = [
    {
        'name': 'My Neighbor Totoro',
        'year': '1988'
    },
    {
        'name': 'Three Colours trilogy',
        'year': '1993'
    },
    {
        'name': 'Forrest Gump',
        'year': '1994'
    },
    {
        'name': 'Perfect Blue',
        'year': '1997'
    },
    {
        'name': 'The Matrix',
        'year': '1999'
    },
    {
        'name': 'Memento',
        'year': '2000'
    },
    {
        'name': 'The Bucket list',
        'year': '2007'
    },
    {
        'name': 'Black Swan',
        'year': '2010'
    },
    {
        'name': 'Gone Girl',
        'year': '2014'
    },
    {
        'name': 'CoCo',
        'year': '2017'
    },
]


@app.route('/index')
def watch_list():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


# 自定义模板上下文
# 这个装饰器装饰的函数当flask渲染任何一个template时都会自己执行，把该字典注入到模板上下文中去
@app.context_processor
def inject_foo():
    foo = 'I am foo'
    return dict(foo=foo)


# 自定义全局函数
@app.template_global()
def bar():
    return 'I am Bar'


# 标记文本安全
from flask import Markup


@app.route('/hello')
def hello():
    # text = Markup('<h1>Hello,Flask!</h1>')
    text = '<h1>Hello,Flask!</h1>'
    return render_template(
        'index.html',
        text=text)  # 这里传入模板的东西不会被自动转义为html，要想自动转义为HTML需要使其变为Markup类的对象


# 默认jinja2中的传入的内容是不会被转义为HTML的，若想转义为HTML就需要用Markup类或者
# safe过滤器等东西


# 自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# 可以通过操作app.jinja_env对象的globals/filters/tests等属性添加自定义的全局对象、过滤器、测试器


@app.route('/newindex')
def new_index():
    return render_template('new_index.html')


# SECRET_KEY都是通过app来设置的，无法直接从环境变量中读取使用，需要手动读取使用
import os
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/flash')
def just_flash():
    flash('I am flash,who is looking for me?')
    flash('诶，是吗？')
    return redirect(url_for('new_index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
