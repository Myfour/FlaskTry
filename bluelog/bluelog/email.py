from flask import url_for, current_app
from bluelog.extensions import mail
from flask_mail import Message


def send_mail(subject, to, html):
    message = Message(subject, recipients=[to], html=html)
    mail.send(message)


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id,
                       _external=True) + '#comments'
    send_mail(
        'New Comment',
        to=current_app.config['BLUELOG_ADMIN_EMAIL'],
        html=
        '<p>New comment in post <i>%s</i>, click the link below to check:</p>'
        '<p><a href="%s">%s</a></p>'
        '<p><small style="color: #868e96">Do not reply this email.</small></p>'
        % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post',
                       post_id=comment.post_id,
                       _external=True) + '#comments'
    if comment.email:  # 检测评论是否有email的
        send_mail(
            subject='New reply',
            to=comment.email,
            html=
            '<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
            '<p><a href="%s">%s</a></p>'
            '<p><small style="color: #868e96">Do not reply this email.</small></p>'
            % (comment.post.title, post_url, post_url))
