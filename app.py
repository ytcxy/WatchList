from flask import Flask, render_template
from flask import url_for, escape
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)   # 初始话扩展，传入程序实例app
# ...


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    db.create_all()
    name = 'ytcxy'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1987'},
        {'title': 'Dead Poets Society', 'year': '1988'},
        {'title': 'A Perfect World', 'year': '1992'},
        {'title': 'Leon', 'year': '1993'},
        {'title': 'Mahjong', 'year': '1995'},
        {'title': 'Swallowtail Butterfly', 'year': '1995'},
        {'title': 'King of Comedy', 'year': '1998'},
        {'title': 'Devils on the Doorstep', 'year': '1998'},
        {'title': 'WALL-E', 'year': '2007'},
        {'title': 'The Pork of Music', 'year': '2011'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('done')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


if __name__ == '__main__':
    app.run()
