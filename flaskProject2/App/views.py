from random import randrange
from flask import Blueprint, render_template

from App.ext import db
from App.models import Cats

blue = Blueprint('blue', __name__, template_folder="../templates")

def init_blue(app):
    app.register_blueprint(blue)


@blue.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@blue.route('/addcat/')
def add_cat():
    cat = Cats()
    cat.name = "cat %s" % randrange(1000)
    cat.food = "fish"
    db.session.add(cat)
    db.session.commit()
    return "add scuess!"


@blue.route('/addcats/')
def add_cats():
    cats = []

    for i in range(5):
        cat = Cats()
        cat.name = "cat%d" % i
        cat.food = "fish%s" % randrange(1000)
        cats.append(cat)

    db.session.add_all(cats)
    db.session.commit()

    return "add success"


@blue.route('/getcat/')
def get_cat():
    cat = Cats.query.get_or_404('20')

    return cat.name

@blue.route('/getcats/')
def get_cats():
    cats = Cats.query.all()
    for cat in cats:
        print(cat.name)

    return render_template('catlist.html', cats = cats)
    # return "good"