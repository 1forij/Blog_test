from . import admin_blue_1
from .forms import ChangePsd,Upload_img
from flask import render_template, redirect, flash, request, jsonify ,session
from flask_login import login_required,current_user
from application import db
from application.models import User
import base64,os

# 个人主页
@admin_blue_1.route('/userspace/<id>')
@login_required
def user_space(id):
    return render_template("/admin/myspace.html")



# 要判断邮箱是不是对应用户注册时用的邮箱...不然盗号太容易了。。。**************注意************
# 找回密码/修改密码 (二合一)
@admin_blue_1.route('/chg_psd', methods=['POST','GET'])
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
        return render_template("/admin/change_password.html",form=fm)

@admin_blue_1.route('/getinfo')
def send_info():
    get_data = request.args.to_dict()
    request_type = get_data.get("request_type")
    request_user = get_data.get("request_user")

    if request_type =="following":
        pass
    elif request_type =="fans":
        pass
    elif request_type =="article":
        user = User.query.get(current_user.id)
        temp={}
        i=0
        for a in user.articles:
            temp[i]=a.title
            i=i+1
        return jsonify(temp)
    elif request_type =="info":
        query_user = User.query.filter_by(username=request_user).first()

        temp={}

        temp["send_username"]=query_user.username

        temp["send_sex"]="男"

        temp["send_phonenum"]=query_user.phonenum

        temp["send_emial"]=query_user.email_ad

        temp["send_labels"]="<睡觉>   <摸鱼>    <上号>"

        return jsonify(temp)
    else:
        pass

@admin_blue_1.route('/upload',methods=['POST','GET'])# 获取用户名-----气死
def upload():#          文件格式没做筛选
    form = Upload_img()
    if request.method=="POST":

        # 获取用户名
        in_name = session["user"]#   实在实现不了post接收总是None，索性直接 全局session 保存一下得了

        # 获取类型为 <class 'werkzeug.datastructures.FileStorage'> 的文件
        user_img_Storage = request.files["user_img"]

        # 将上一步的文件 转化 为 bytes stream
        user_img_stream = user_img_Storage.stream.read()

        # 转化为 base64 编码字符
        image_base64 = str(base64.b64encode(user_img_stream), encoding='utf-8')  # image_base64即是对图像进行base64编码后的内容
        # 存入 数据库
        query_user = User.query.filter_by(username=in_name).first()

        query_user.user_img=image_base64

        return redirect('/userspace')
    return render_template('/admin/upload.html', form=form)
