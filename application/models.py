from .database import db 
from sqlalchemy import ForeignKey,PrimaryKeyConstraint


class user(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer, primary_key=True, auto_increment=True)
    email=db.Column(db.String, not_null=True, unique=True)
    username=db.Column(db.String)
    name=db.Column(db.String)
    dob=db.Column(db.String)
    gender=db.Column(db.Integer)
    password=db.Column(db.String, not_null=True)
    profile_picture=db.Column(db.LargeBinary,default=None)
    joined_time=db.Column(db.String)

class blogs(db.Model):
    __tablename__="blogs"
    blog_id=db.Column(db.Integer,not_null=True)
    user_id=db.Column(db.Integer, ForeignKey("user.user_id",ondelete="CASCADE", onupdate="CASCADE"))
    title=db.Column(db.String)
    content=db.Column(db.String)
    post_time=db.Column(db.String)
    blog_image=db.Column(db.LargeBinary, default=None)
    edited=db.Column(db.Integer, default=0)

class follows(db.Model):
    __tablename__="follows"
    user_id=db.Column(db.Integer, ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    follower_id=db.Column(db.Integer, ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    follow_time=db.Column(db.String)
    PrimaryKeyConstraint(user_id,follower_id)

class comments(db.Model):
    __tablename__="comments"
    comment_id=db.Column(db.Integer,primary_key=True)
    blog_id=db.Column(db.Integer,ForeignKey("blogs.blog_id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id=db.Column(db.Integer,ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    comment=db.Column(db.String)
    comment_posted=db.Column(db.String)

class likes(db.Model):
    __tablename__="likes"
    like_id=db.Model(db.Integer,primary_key=True)
    blog_id=db.Model(db.Integer,ForeignKey("blogs.blog_id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id=db.Model(db.Integer, ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    liked_time=db.Model(db.String)

    