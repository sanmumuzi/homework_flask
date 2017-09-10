from flask import render_template

from . import main
from ..models import User, Role, Post
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/homework_list/<group_name>')
def home_list(group_name):
    posts = Post.query.filter_by(group=group_name).order_by(Post.timestamp.desc()).all()
    return render_template('home_list.html', group_name=group_name, posts=posts)
