from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from application import db
from datetime import datetime
from application import login_manager
import bleach # 清除多余的html标签
from markdown import markdown
from flask import current_app


# 数据库类似于一个仓库
class User(UserMixin,db.Model):

    __tablename__ = 'user'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)

    username=db.Column(db.String(30),nullable=False)# 不为空

    _password_hash=db.Column(db.String(256))

    phonenum=db.Column(db.Integer,nullable=False)

    email_ad=db.Column(db.String(30))

    user_img=db.Column(db.String(255),default='../static/imgs/users.jpg')
    
    articles = db.relationship("Article",backref="user")# backref="user"  提供反向引用的接口    可以通过文章反向找到作者  article.user
                                                       # lazy 决定了什么时候从数据库中加载数据
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))


    @property
    def password(self):#    用户调用密码,能看(哈希值)不能改   使得password == self._password_hash
        return self._password_hash

    @password.setter#   存储密码于db  and  修改密码
    def set_password(self, in_word):
        self._password_hash = generate_password_hash(in_word)

    def check_password(self, in_word):  # 验证密码   返回True/False
        return check_password_hash(self._password_hash, in_word)

    @property
    def is_authenticated(self):
        return True

    def __init__(self, **kwargs):   # 根据邮箱设置角色权限
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

@login_manager.user_loader#       读取用户
def user_loader(user_id):
    user = User.query.get(int(user_id))
    return user


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128))

    body = db.Column(db.Text)

    body_html = db.Column(db.Text)# 存放被转换成html格式的文本

    # 外键 同步到数据库的外键关系   存在于表中，且是与User类互相映射的桥梁
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    create_time = db.Column(db.String(50), default=datetime.now().strftime('%Y-%m-%d %H:%M'))

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


class Permissions(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)

    FOLLOW = 0X01

    FOLLOWED = 0X02

    WRITE_ARTICLE = 0X04

    COMMENT = 0X08

    ADMIN = 0X80


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), unique=True)

    default = db.Column(db.Boolean, default=False, index=True)

    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role')# backref参数则对关系提供反向引用的声明。                                                        # 子查询方式(subquery)

    @staticmethod
    def init_role():
        roles = {          #  身份权限映射
            'user': [Permissions.WRITE_ARTICLE,Permissions.COMMENT,Permissions.FOLLOW,Permissions.FOLLOWED],
            'admin': (0xff,False)
        }
        try:
            for r in roles:
                role = Role.query.filter_by(name=r).first()#　角色名为用户的第一个
                if role is None:    # 如果查询结果为空
                    role = Role(name=r)         # 加入类型
                role.permissions=role[r][0]    #   　重置其permissions === 0
                role.default = role[r][1]
                db.session.add(role)
            db.session.commit()
        except: # 若发生异常，撤销刚刚的操作
            db.session.rollback()
        db.session.close()


    def has_permission(self, permission):
        return self.permissions & permission == permission
