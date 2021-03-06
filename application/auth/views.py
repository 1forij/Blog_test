# coding=utf-8
import random,json
from flask_login import login_user, logout_user
from flask import redirect, render_template, flash, session, jsonify, request
from . import auth_blue

from .forms import LoginForm,RegisterForm
from application import db
from application.models import User
from flask_mail import Message
from application import my_email
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
            if u_search is not None and u_search.check_password(in_word):# 注意这里：密码判断这里要写实例化后的方法(即u_seaech.某方法),不能写User.某方法
                login_user(u_search,True)#              登录  并记住我
                session["user"]=in_name
                flash("欢迎回来，用户 {}！".format(in_name))#       最好实现成那种自动消失的flash
                return redirect('/')
            else:
                flash("账户不存在,或密码错误,请重新登录")
                return render_template('login.html',form=fm)#   没有这个账号
        else:#                  验证码都不对
            flash("请注意验证码")
            return redirect('/login')
    return render_template('/auth/login.html',form=fm)

# 登出
@auth_blue.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# 注册
@auth_blue.route('/register',methods=['POST','GET'])
def register():
    fm=RegisterForm()
    if fm.validate_on_submit():
        in_name=fm.username.data
        in_word=fm.password.data
        in_phone=fm.phonenum.data
        in_code=fm.proofcode.data # 这里 in_code 是 邮箱验证码
        in_email=fm.email_ad.data
        if in_code==session['email']:
            query_user= User.query.filter(User.username==in_name).first()
            if query_user:
                flash('该用户名已存在!')
                return redirect('/register')
            new_user=User(username=in_name,phonenum=in_phone,email_ad=in_email)# @property的存在，使得password == self._password_hash
            new_user.set_password=in_word
            db.session.add(new_user)
            db.session.commit()
            flash('恭喜你，注册成功,自动前往登录界面')

            return redirect('/login')
    return render_template('/auth/register.html',form=fm)

# 送码
@auth_blue.route('/getcode')
def getcode():
    proofcode = str(random.randint(1111, 9999))
    session['proof']=proofcode
    return jsonify({"code":proofcode})

# 送信    要求:判断邮箱是否合理
@auth_blue.route('/send_email',methods=['POST'])
def send_email():
    # 准备工作
    in_email_ad = request.get_data().decode()#　   将流转为str
    in_email_ad = in_email_ad.replace("%40","@")#       把%40 换成@
    in_email_ad = in_email_ad[12:]#                     掐头去尾

    if "@qq.com" in in_email_ad:
        email_num = str(random.randint(1111, 9999))
        session['email']=email_num
        meg = Message("欢迎!这里是Forij博客",recipients=[in_email_ad])
        meg.body = "您此次的操作的相关验证码为 %s" % email_num
        my_email.send(meg)
        return jsonify({"ok":"1"})
    else:
        flash("邮箱有误,请重新输入")
        return jsonify({"error": "0"})