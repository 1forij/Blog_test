from flask_login import login_required

from . import main_blue

from flask import render_template

from application.models import Article

@main_blue.route('/')
@login_required# 如果你将这个装饰器放在视图上，它会保证你的当前用户是登录状态，并且在调用实际视图之前进行认证。
def index():#    如果当前用户不是系统认证的登录状态，它将调用LoginManager.unauthorized回调。
    a=Article.query.filter(Article.author=="123").all()

    return render_template('index.html',body_html=a[1].body_html,title=a[1].title)


@main_blue.route('/test')
def test_case():
    return render_template('test.html')