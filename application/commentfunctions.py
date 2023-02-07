from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode
from .userfunctions import *
from .blogfunctions import *

class commentfunctions:
    def addcomment(self,user_id,blog_id,comment):
        comment_posted=time_calc().time()
        db.session.execute("insert into comments(user_id,blog_id,comment,comment_posted) values (:user_id,:blog_id,:comment,:comment_posted)",{"user_id":user_id,"blog_id":blog_id,"comment":comment,"comment_posted":comment_posted})
        db.session.commit()
        return 

    def addcomment_email(self,email,blog_id,comment):
        user_id=userfunctions().get_uid_from_email(email)
        return commentfunctions().addcomment(user_id,blog_id,comment)

    def allcomments(self,blog_id,user_id):
        blog_details=blogfunctions().blog_with_id(blog_id,user_id)
        details=db.session.execute("select u.username,u.profile_picture,u.gender,u.user_id, c.comment_id, c.comment, c.comment_posted from user u, comments c where u.user_id=c.user_id and c.blog_id=:id order by comment_id DESC",{"id":blog_id})
        l=[]
        for i in details:
            temp=list(i)
            temp[6]=time_calc().convert(temp[6])
            if temp[1]=='' or temp[1]=='None' or temp[1]==None or temp[1]=="b''":
                temp[1]=-1
            else:
                temp[1]=b64encode(temp[1]).decode("utf-8")
            l+=[temp]
        count=db.session.execute("select count(*) from user u, comments c where u.user_id=c.user_id and c.blog_id=:id order by comment_id DESC",{"id":blog_id})
        count=list(count.fetchall()[0])
        if len(count)==0:
            count=0
        else:
            count=count[0]
        return l,blog_details,count
