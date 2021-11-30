
from flask_sqlalchemy import SQLAlchemy

from application import main

from application import db

# 数据库类似于一个仓库
class User(db.Model):# 定义的这个User类，类似于一个货架
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)# 该货架的快递清单
    # 以下为货架上的各类快递包裹
    username=db.Column(db.String(30),nullable=False)# 不为空
    password=db.Column(db.String(30),nullable=False)# 不为空
    phonenum=db.Column(db.Integer,nullable=False)

    def __str__(self):
        return self.username


