from flask import Blueprint, request, render_template, make_response, Response, abort, session

blue = Blueprint('blue', __name__)


def init_blue(app):
    app.register_blueprint(blue)


@blue.route("/")
def index():
    return "Index"


@blue.route("/sendrequest/", methods=["GET", "POST"])
def send_request():
    print(request.args)
    print(type(request.args))
    print(request.form)
    print(type(request.form))
    print(request.headers)
    print(type(request.headers))
    return "send success"


@blue.route("/getresponse/", methods=["GET", "POST"])
def get_response():
    # result = render_template('hello.html')
    # print(result)
    # print(type(result))
    # return result

    # response = make_response("<h2>你是个鸟人</h2>")
    # print(response)
    # print(type(response))

    abort(401)
    response = Response("自己DIY")
    return response


@blue.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        print(username)
        response = Response("登录成功:{}".format(username))
        # response.set_cookie("username", username)
        session['username'] = username
        return response


@blue.route('/mine/')
def mine():
    # username = request.cookies.get('username')
    username = session.get('username')
    return '欢迎回来：%s' % username