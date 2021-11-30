from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField(validators=[DataRequired()])
    password=PasswordField(validators=[DataRequired()])
    proofcode=StringField(validators=[DataRequired()])
    submit=SubmitField('登录')
class RegisterForm(FlaskForm):
    username=StringField(validators=[DataRequired()])
    password=PasswordField(validators=[DataRequired()])
    phonenum=StringField(validators=[DataRequired()])
    proofcode=StringField(validators=[DataRequired()])
    submit=SubmitField('注册')