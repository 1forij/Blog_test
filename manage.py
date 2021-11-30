# 启动项
from application import create_app
from application import db
from flask_script import Manager

app = create_app("development")
manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
