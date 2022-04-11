from flask import Flask

from App.ext import init_ext
from App.settings import envs
from App.views import init_blue


def creat_app(env):
    app = Flask(__name__)

    app.config.from_object(envs.get(env))

    init_blue(app)

    init_ext(app)

    return app

