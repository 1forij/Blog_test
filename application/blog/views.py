from flask_login import login_required,current_user
from . import blog_blue
from flask import render_template,redirect,session,flash
from .forms import CreatePost
from application import db
from application.models import Article


@blog_blue.route('/create_post',methods=["POST","GET"])
@login_required
def create_post():

    fm = CreatePost()
    if fm.validate_on_submit():

        in_title = fm.title.data
        in_body = fm.body.data
        in_categories = fm.categories.data

        new_article=Article(title=in_title,body=in_body,author_id=current_user.id,categories=in_categories)

        db.session.add(new_article)
        db.session.commit()
        flash("发布成功")
        return redirect("/")
    return render_template('/blog/write_post.html',form=fm)