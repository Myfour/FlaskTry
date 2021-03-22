from . import app, db
from .models import Message
from .forms import HelloForm
from flask import render_template, redirect, url_for, flash


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)
