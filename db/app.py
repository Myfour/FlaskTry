from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
import os
import click
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# 迁移第一步执行flask db init创建迁移文件夹，flask db migrate根据模型创建迁移文件，flask db upgrade/downgrade 实现模型的升级、降级
# --------------------------------------------------------------- Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 只要使用了flask_wtf就会用到csrf，也就需要设置SECRET_KEY配置
app.config['SECRET_KEY'] = 'SECRET'
# --------------------------------------------------------------- Model


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Note %r>' % self.body


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20))
    # 一侧添加关系属性
    articles = db.relationship(
        'Article')  # db.relationship()关系函数，其第一个参数为对应的模型类的名称

    def __repr__(self):
        return f'<Author {self.name}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    # 多侧添加外键,外键一定在多的一边
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('author.id'))  # author.id是实际的 表名.字段名，表名默认为模型名的小写，可以自定义表名

    def __repr__(self):
        return f'<Article {self.title}>'


# 配置双向关系------------------------------
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    books = db.relationship('Book', back_populates='writer')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')


# 使用backref简化双向关系的设置-----------------


class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship('Song', backref='singer')


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'))


# 一对一关系建立--------------------------------
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    capital = db.relationship(
        'Capital', uselist=False)  # 一对一关系的要点就是在非标量关系属性这边设置uselist=False来实现


class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country')


# 多对多关系建立--------------------------------
association_table = db.Table(
    'association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    grade = db.Column(db.String(30))
    teachers = db.relationship('Teacher',
                               secondary=association_table,
                               back_populates='students')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student',
                               secondary=association_table,
                               back_populates='teachers')


# 级联操作--------------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    body = db.Column(db.Text)
    comments = db.relationship('Comment',
                               back_populates='post',
                               cascade='all,delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


# --------------------------------------------------------------- Form
class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')


# 为delete操作单独设置一个只有删除按钮的表单
class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')


# --------------------------------------------------------------- View
# Create
@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved.')
        # flash的内容在模板中使用get_flashed_messages()即可获取
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


# Update
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated .')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)


# Delete 删除操作不能做单独的一个a标签来GET请求Delete操作，有CSRF攻击的风险，需要做一个表单来删除
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted.')
    else:
        abort(400)
    return redirect(url_for('index'))


@app.route('/')
def index():
    form = DeleteNoteForm()  # 为了在主页中渲染一个删除按钮
    notes = Note.query.all()
    return render_template('index.html', notes=notes, form=form)


# --------------------------------------------------------------- Others
# 注册一个flask命令
@app.cli.command()
def initdb():
    '''
    Initialize database.
    '''
    db.create_all()
    click.echo('Initialized database.')


# 为flask shell注册上下文,便于在flask shell中处理一些对象
@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
                Note=Note,
                Author=Author,
                Article=Article,
                Writer=Writer,
                Book=Book,
                Country=Country,
                Capital=Capital,
                Student=Student,
                Teacher=Teacher,
                Post=Post,
                Comment=Comment)
