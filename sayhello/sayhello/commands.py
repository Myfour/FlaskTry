from sayhello import app, db
from .models import Message
import click


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Database Initialized.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages,default is 20')
def forge(count):
    """
    Generate fake messages.
    """
    from faker import Faker
    db.drop_all()
    db.create_all()
    fake = Faker('zh_CN')
    click.echo('working....')
    for i in range(count):
        message = Message(name=fake.name(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year())
        db.session.add(message)
    db.session.commit()
    click.echo(f'Created { count } fake messages.')