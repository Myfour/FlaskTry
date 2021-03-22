from flask import Flask, render_template, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import click, os
app = Flask(__name__)

# 配置邮箱相关
# app.config.update(MAIL_SERVER='smtp.126.com',
#                   MAIL_USE_SSL=True,
#                   MAIL_PORT=465,
#                   MAIL_USERNAME='oz_myx@126.com',
#                   MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
#                   MAIL_DEFAULT_SENDER=('Myfour', 'oz_myx@126.com'),
#                   SECRET_KEY='SECRET')

# mailgun邮箱配置
app.config.update(
    MAIL_SERVER='smtp.mailgun.org',
    MAIL_USE_TLS=True,
    MAIL_PORT=587,
    MAIL_USERNAME=
    ' postmaster@sandboxe246aec5fba84ff0880cbcaae9fdb6d2.mailgun.org',
    MAIL_PASSWORD='904882536db88d9317b5078367a33372-e49cc42c-09f94b63',
    MAIL_DEFAULT_SENDER=('Myfour', 'xxxxxx@xxx.com'),
    SECRET_KEY='SECRET')

mail = Mail(app)  # 这步实例化Mail对象必须在邮箱配置完之后


class SubForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired()])
    submit = SubmitField('Subscribe')


@app.route('/', methods=['GET', 'POST'])
def subscribe():
    form = SubForm()
    if form.validate_on_submit():
        email = form.email.data
        send_mail('Hello World!', email)
        flash('订阅成功')
        return redirect(url_for('subscribe'))
    return render_template('index.html', form=form)


def send_mail(subject, to):
    message = Message(
        subject=subject,
        recipients=[to],
        body='Across the Great Wall we can reach every corner in the world.')
    mail.send(message)


@app.cli.command()
def send():
    ''' send email'''
    message = Message(
        subject='Hello, World!',
        recipients=['913906842@qq.com'],
        body='Across the Great Wall we can reach every corner in the world.')
    mail.send(message)
    click.echo('send over')