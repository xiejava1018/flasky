#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('密码',validators=[Required()])
    remember_me=BooleanField('记住我')
    submit=SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(),Length(1,64), Email()])
    username=StringField('用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须是字母数字点或下划线组成')])
    password=PasswordField('密码',validators=[Required(),Length(4,18,message='密码必须大于4位'),EqualTo('password2',message='确认密码不一致')])
    password2=PasswordField('确认密码',validators=[Required()])
    submit=SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email已经被注册。')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册。')