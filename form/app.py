from flask import Flask, render_template, request
from forms import LoginForm
app = Flask(__name__)
app.secret_key = 'secret secret'
app.config['WTF_I18N_ENABLED'] = False

# from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired, Length

# class LoginForm(Form):
#     username = StringField('username', validators=[DataRequired()])
#     password = PasswordField('password',
#                              validators=[DataRequired(),
#                                          Length(8, 128)])
#     remember = BooleanField('Remember me')
#     submit = SubmitField('Log in')


@app.route('/', methods=['GET', 'POST'])
def test():
    form = LoginForm()
    # if request.method == 'POST' and form.validate():
    #     return 'All Right'
    if form.validate_on_submit():
        username = form.username.data
        print(f'welcome home,{username}')
        return '同上if语句一样的功能 ALL RIGHT'
    return render_template('bootstrap.html', form=form)
