from application import db,admin_it
from application.models import User,Article,Role
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose
from flask_login import login_required,current_user
from flask import abort,current_app

# 加DIY或第三方管理
# class MyView(BaseView):
#     @login_required
#     @expose('/')
#     def index(self):
#         if current_user.email_ad == current_app.config['FLASKY_ADMIN']:
#             return self.render('/admin/index.html')
#         else:
#             return abort(403)
#
# admin_it.add_view(MyView(name="DIY_VIEWS"))


# 定义一个类并继承ModelView，并重写一些代码，把想要显示出来的列名写在column_list中
class Article_View(ModelView):
    column_labels = {
        'id': u'序号',
        'title': u'新闻标题',
        'body':u'文章内容',
        'create_time':u'创建时间',
        'categories':u'类别',
    }
    column_list = ('id','title','body','create_time','categories')
    def __init__(self, session, **kwargs):
        super(Article_View, self).__init__(Article, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated and current_user.email_ad == current_app.config['FLASKY_ADMIN']:
            print(current_app.config['FLASKY_ADMIN'])
            return True
        return False
admin_it.add_view(Article_View(db.session,name = u'管理文章'))



class User_View(ModelView):
    column_labels = {
        'id': u'序号',
        'username': u'用户名',
        'phonenum': u'手机号',
        'email_ad': u'邮箱',
    }
    column_list = ('id','username', 'phonenum', 'email_ad')
    def __init__(self, session, **kwargs):
        super(User_View, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated and current_user.email_ad == current_app.config['FLASKY_ADMIN']:
            return True
        return False
admin_it.add_view(User_View(db.session,name = u'管理用户'))