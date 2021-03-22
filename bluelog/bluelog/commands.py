import click
from bluelog.fakes import fake_admin, fake_categories, fake_post, fake_comments
from bluelog.extensions import db
from bluelog.email import send_new_reply_email, send_new_comment_email
from bluelog.models import Post, Admin, Category


def register_commands(app):
    @app.cli.command()
    @click.option('--category',
                  default=10,
                  help='Quantity of categories default is 10.')
    @click.option('--post', default=50, help='Quantity of posts default is 50')
    @click.option('--comment',
                  default=500,
                  help='Quantity of comments default is 500')
    def forge(category, post, comment):
        """Generate the fake categories,posts,comments."""
        db.drop_all()
        db.create_all()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo(f'Generating {category} categories...')
        fake_categories(category)
        click.echo(f'Generating {post} posts...')
        fake_post(post)
        click.echo(f'Generating {comment} comment...')
        fake_comments(comment)
        click.echo('Done.')

    @app.cli.command()
    def send():
        '''test send'''
        post = Post.query.get(1)
        send_new_comment_email(post)

    @app.cli.command()
    @click.option('--username',
                  prompt=True,
                  help='The username userd to login.')
    @click.option('--password',
                  prompt=True,
                  hide_input=True,
                  confirmation_prompt=True,
                  help='The password used to login.')
    def init(username, password):
        '''Building Bluelog just for you'''
        click.echo('Initialize the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('The administrator already exists,updating ...')
            admin.username = username
            admin.password = password
        else:
            click.echo('Create the temporary administrator account ...')
            admin = Admin(username=username,
                          blog_title='Bluelog',
                          blog_sub_title='No,I\'m the real thing .',
                          name='Admin',
                          about='Anything about you.')
            admin.password = password
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)
        db.session.commit()
        click.echo('Done.')
