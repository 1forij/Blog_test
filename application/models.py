from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from application import db
from datetime import datetime
from application import login_manager
import bleach # 清除多余的html标签
from markdown import markdown


# 数据库类似于一个仓库
class User(UserMixin,db.Model):# 定义的这个User类，类似于一个货架
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)# 该货架的快递清单
    # 以下为货架上的各类快递包裹
    username=db.Column(db.String(30),nullable=False)# 不为空
    _password_hash=db.Column(db.String(256))
    phonenum=db.Column(db.Integer,nullable=False)
    email_ad=db.Column(db.String(30))
    user_img=db.Column(db.String(255),default='../static/imgs/users.jpg')



    @property
    def password(self):#    用户调用密码,能看(哈希值)不能改   使得password == self._password_hash
        return self._password_hash

    @password.setter#   存储密码于db  and  修改密码
    def set_password(self, in_word):
        self._password_hash = generate_password_hash(in_word)


    def check_password(self, in_word):  # 验证密码   返回True/False
        return check_password_hash(self._password_hash, in_word)

@login_manager.user_loader#       读取用户
def user_loader(user_id):
    user = User.query.get(int(user_id))
    return user


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    author = db.Column(db.Text)
    body_html = db.Column(db.Text)# 存放被转换成html格式的文本
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    categories = db.Column(db.String(20))
    num_like = db.Column(db.Integer)
    num_comment = db.Column(db.Integer)
    num_visited = db.Column(db.Integer)
    @staticmethod

    # 当某个方法不需要用到对象中的任何资源, 将这个方法改为一个静态方法, 加一个 @ staticmethod

    # 加上之后, 这个方法就和普通的函数没有什么区别了, 只不过写在了一个类中, 可以使用这个类的对象调用,

    # 也可以使用类直接调用,
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        target.body_html = bleach.linkify(# 作用是将html文本中的url转换成<a>
                            bleach.clean(
                            markdown(value, output_format='html'),
                            tags=allowed_tags,
                            strip=True,
                            attributes=allowed_attrs
                                )
                            )
db.event.listen(Article.body, 'set', Article.on_changed_body)