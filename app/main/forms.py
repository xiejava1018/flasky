#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import Required,Length

class NameForm(FlaskForm):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('提交')


class EditProfileForm(FlaskForm):
    name=StringField('真实姓名',validators=[Length(0,64)])
    location=StringField('地址',validators=[Length(0,64)])
    about_me=TextAreaField('自我介绍')
    submit=SubmitField('提交')