from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session, g
import click, os
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>HELLO , World ! --Myfour </h1>'


# 为一个view函数绑定多个路由
@app.route('/hello', methods=['POST'])  # methods设置该请求的类型只能为POST
@app.route('/hi')
def say_hello():
    return '<b>What\'s up !</b>'


# 向路由中传入参数
# 路由设置默认参数值
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return f'<p>Hello,{ name } !!! </p>'


# flask自动寻找Flask实例的机制是在 1. 当前目录寻找名为app.py或者wsgi.py的模块，并从中寻找app或application的程序实例
# 2.从环境变量FLASK_APP对应的模块寻找app或application 的实例
# 3.如果使用python-dotenv则寻找实例还从.flaskenv或者.env文件中加载环境变量


# 自定义Flask命令
@app.cli.command()
def hello():
    '''\
    Just Say Hello.
    '''
    click.echo('Hello,Human!')


# 使用request对象
@app.route('/rehello')
def re_hello():
    # name = request.args.get('name', 'Flask')
    # 上述被g对象的name属性代替了
    if g.name:
        name = g.name
    else:
        name = '[NULL]'
    if name == '[NULL]':
        name = request.cookies.get('name', 'Human')
    if 'logged_in' in session:
        name += '[Authenticated]'
    else:
        name += '[Not Authenticated]'
    return f'<h1>ReHello,{name}!</h1>'


# 限定url参数的类型
@app.route('/goback/<int:year>')
def go_back(year):
    return f'<h1>back to the {2021-year} !</h1>'


@app.route('/colors/<any(blue,green,red):color>')  # any限定只能输入括号中的内容
def colors(color):
    return f'We Chose {color} !'


# 重定向
@app.route('/gobaidu')
def go_baidu():
    return redirect('http://www.baidu.com')


@app.route('/gohello')
def go_hello():
    return redirect(url_for('re_hello'))  # url_for可以定位到其他视图函数


# 手动返回错误码
@app.route('/404')
def not_found():
    abort(404)


# 设置不同的响应的mimetype
@app.route('/mmtype')
def mmtype():
    response = make_response('<h1>This is text only !</h1>')
    response.mimetype = 'text/plain'
    return response


# 返回json类型
@app.route('/json1')
def json_1():
    data = {'name': 'Myfour', 'gender': 'male'}
    print(data, type(data))
    print(json.dumps(data), type(json.dumps(data)))
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


@app.route('/json2')
def json_2():
    data = {'name': 'sfincs', 'gender': 'unknown'}
    print(type(jsonify(data)))
    return jsonify(data), 500  # 可自定义状态码


# 使用cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('re_hello')))
    response.set_cookie('name', name)
    return response


app.secret_key = os.getenv('SECRET_KEY', 'mmm')


# 使用session模拟登陆
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('re_hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to the Admin Page~'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('re_hello'))


# 使用g对象配合请求钩子使用
@app.before_request
def get_name():
    g.name = request.args.get('name')


# 重定向回前一个页面
@app.route('/foo')
def foo():
    return f"<h1>Foo Page</h1><a href={url_for('dosometing')}>dosometing</a><a href={url_for('dosometing_2',next=request.full_path)}>dosometing2</a>"


# dosometing_2传入一个next参数存储当前路径


@app.route('/bar')
def bar():
    print(request.full_path)
    return f"<h1>Bar Page</h1><a href={url_for('dosometing')}>dosometing</a><a href={url_for('dosometing_2',next=request.full_path)}>dosometing2</a>"


@app.route('/dosometing')
def dosometing():
    return redirect(
        request.referrer or url_for('re_hello')
    )  # request.referrer可以获取前一个跳转来的页面，但是有些浏览器可以关闭这个功能，所以需要设置一层保险的跳转


@app.route('/dosometing2')  # 第二种在请求的url中加一个next参数的方式来实现跳转回前一个页面
def dosometing_2():
    # is_safe_url(request.args.get('next'))
    return redirect(request.args.get('next', url_for('re_hello')))


# 验证重定向的地址是否是当前站点的地址
from urllib.parse import urljoin, urlparse


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    tested_url = urlparse(urljoin(request.host_url, target))
    return tested_url.scheme in (
        'http', 'https') and tested_url.netloc == ref_url.netloc


# AJAX显示全文模拟
from jinja2.utils import generate_lorem_ipsum


@app.route('/more')
def load_more():
    return generate_lorem_ipsum(n=1)


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''\
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://lib.baomitu.com/jquery/latest/jquery.min.js"></script>
<script type="text/javascript">
$(function(){
    $('#load').click(function(){
        $.ajax({
            url:'/more',
            type:'get',
            success:function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>
    ''' % post_body