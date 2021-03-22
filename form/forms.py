from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class ChinaForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(ChinaForm):
    username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={
                               'placeholder': '你的用户名',
                               'class': 'my_class'
                           })
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')