#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import Required,Length,Email,Regexp,ValidationError,DataRequired
from flask_pagedown.fields import PageDownField
from app.models import Role,User

class NameForm(FlaskForm):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('提交')


class EditProfileForm(FlaskForm):
    name=StringField('真实姓名',validators=[Length(0,64)])
    location=StringField('地址',validators=[Length(0,64)])
    about_me=TextAreaField('简介')
    submit=SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters,number,dots or underscores')])
    role=SelectField(
        '角色',
        coerce=int
    )
    name=StringField('真实姓名',validators=[Length(0,64)])
    location=StringField('地址',validators=[Length(0,64)])
    about_me=TextAreaField('简介')
    confirmed = BooleanField('是否已确认')
    submit=SubmitField('提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if field.data!=self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')


class PostForm(FlaskForm):
    body=PageDownField("What's on your mind?",validators=[Required()])
    submit=SubmitField('提交')


class CommentForm(FlaskForm):
    body=StringField("",validators=[Required()])
    submit=SubmitField('提交')