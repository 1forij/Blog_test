import random
from werkzeug.datastructures import RequestCacheControl
from flask import redirect,render_template,flash, session
from . import auth_blue

from .forms import LoginForm,RegisterForm
from application import db
from application.models import User

'''
1.密码不能明文丢数据库---hash
2.使用flask_login
'''
# 登录
@auth_blue.route('/login',methods=['POST','GET'])
def login():
    fm=LoginForm()
    if fm.validate_on_submit():
        in_name=fm.username.data
        in_word=fm.password.data
        in_code=fm.proofcode.data

        if in_code==session['proof']:
            u_search=User.query.filter(User.username==in_name).first()
            if u_search is not None and in_word == u_search.password:
                print(u_search.password)
                # 设置cookie
                response=redirect('/')
                response.set_cookie('yourName',in_name,max_age=10000)
                response.set_cookie('yourPassword',in_word,max_age=10000)
                return response
            else:
                flash("用户不存在!")
                proofcode=str(random.randint(1111,9999))
                session['proof']=proofcode
                return render_template('login.html',form=fm,rn=proofcode)

    proofcode=str(random.randint(1111,9999))
    session['proof']=proofcode
    return render_template('login.html',form=fm,rn=proofcode)

# 登出
@auth_blue.route('/logout')
def logout():
    logout_res = redirect('/')
    logout_res.delete_cookie('yourName')
    logout_res.delete_cookie('yourPassword')
    return logout_res

# 注册
@auth_blue.route('/register',methods=['POST','GET'])
def register():
    fm=RegisterForm()
    if fm.validate_on_submit():
        in_name=fm.username.data
        in_word=fm.password.data
        in_phone=fm.phonenum.data
        in_code=fm.proofcode.data
        if in_code==session['proof']:
            new_user=User(username=in_name,password=in_word,phonenum=in_phone)
            db.session.add(new_user)
            db.session.commit()
            flash('恭喜你，注册成功')
            response=redirect('/')
            response.set_cookie('yourName',in_name,max_age=10000)
            response.set_cookie('yourPassword',in_word,max_age=10000)
            return response
    proofcode=str(random.randint(1111,9999))
    session['proof']=proofcode
    return render_template('register.html',form=fm,rn=proofcode)

# 送码
@auth_blue.route('/getcode')
def getcode():
    proofcode = str(random.randint(1111, 9999))
    session['proof']=proofcode
    print(proofcode)
    # return '<label id="code">{}<label>'.format(proofcode)
    return proofcode