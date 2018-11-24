#-*-coding:utf-8-*-
import hashlib
import bleach
from datetime import datetime
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin,AnonymousUserMixin
from flask import current_app,request
from markdown import markdown

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False)
    permissions=db.Column(db.Integer)
    users=db.relation('User',backref='role',lazy='dynamic')

    def __int__(self,**kwargs):
        super(Role, self).__int__(**kwargs)
        if self.permissions is None:
            self.permissions=0

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.FOLLOW,Permission.COMMENT,Permission.WRITE),
            'Moderator':(Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE),
            'Administrator':(Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE,Permission.ADMIN)
        }
        default_role='User'
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self,perm):
        if not self.has_permisson(perm):
            self.permissions+=perm

    def remove_permission(self,perm):
        if self.has_permisson(perm):
            self.permissions-=perm

    def reset_permissions(self):
        self.permissions=0

    def has_permisson(self,perm):
        return self.permissions & perm==perm

    def __repr__(self):
        return '<Role %r>' % self.name



class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed=db.Column(db.Boolean,default=False)
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts=db.relationship('Post',backref='author',lazy='dynamic')

    def __int__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(permissions='Administrator').first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_active(self):
        return True

    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except Exception as e:
            print(str(Exception))
            print(str(e))
            print(str(e.message))
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True

    def can(self,perm):
        return self.role is not None and self.role.has_permisson(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash =self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser


class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    body_html=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags=['a','abbr','acronym','b','blockquote','code',
                      'em','i','li','ol','pre','strong','ul',
                      'h1','h2','h3','p']
        target.body_html=bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),
            tags=allowed_tags,strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)

class Follow(db.Model):
    __tablename__='follows'
    follower_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)

