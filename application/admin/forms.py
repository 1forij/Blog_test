from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField,SubmitField,FileField
from wtforms.validators import DataRequired

class ChangePsd(FlaskForm):
    pre_username = StringField(validators=[DataRequired()])
    pre_phonenum = StringField(validators=[DataRequired()])
    pre_email_ad = StringField(validators=[DataRequired()])
    proofcode = StringField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('点击找回密码')

class Upload_img(FlaskForm):
    user_img = FileField(validators=[FileRequired(), FileAllowed(['jpg'])])
    submit = SubmitField('上传')