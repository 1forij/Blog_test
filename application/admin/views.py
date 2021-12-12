from . import admin_blue
from .forms import ChangePsd
from flask import session, render_template, redirect, flash
from flask_login import login_required
from application import db
from application.models import User




# 个人主页
@admin_blue.route('/usersapce')
@login_required
def user_space():
    return render_template("myspace.html")



# 要判断邮箱是不是对应用户注册时用的邮箱...不然盗号太容易了。。。**************注意************
# 找回密码/修改密码 (二合一)
@admin_blue.route('/chg_psd', methods=['POST','GET'])
def chg_psd():
    fm=ChangePsd()
    if fm.validate_on_submit():
        in_name = fm.pre_username.data
        in_phone = fm.pre_phonenum.data
        in_email = fm.pre_email_ad.data
        in_code = fm.proofcode.data
        in_word=fm.new_password.data
        if in_code == session['email']:
            query_user = User.query.filter(User.username == in_name,User.phonenum == in_phone,User.email_ad == in_email).first()
            if query_user:
                query_user.set_password = in_word
                db.session.commit()
                flash('恭喜你，修改密码,自动前往登录界面')
                return redirect('/login')
            else:
                flash("存在错误，请重试！")
                return redirect('/chg_psd')
    else:
        return render_template("change_password.html",form=fm)