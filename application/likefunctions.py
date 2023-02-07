from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode



class likefunctions:
    def addlike(self,user_id,blog_id):
        like_time=time_calc().time()
        db.session.execute("insert into likes(user_id,blog_id,liked_time) values(:uid, :bid, :lt) ",{"uid":user_id,"bid":blog_id,"lt":like_time})
        db.session.commit()
        return 

    def unlike(self,user_id,blog_id):
        db.session.execute("delete from likes where user_id=:uid and blog_id=:bid",{"uid":user_id, "bid":blog_id})
        db.session.commit()
        return
    
    def get_all_likes_of(self, blog_id):
        details=db.session.execute("select u.username,u.profile_picture,u.gender,u.user_id, l.like_id, l.liked_time from user u, likes l where u.user_id=l.user_id and l.blog_id=:bid order by like_id DESC ",{"bid":blog_id})
        l=[]
        for i in details:
            temp=list(i)
            temp[5]=time_calc().convert(temp[5])
            if temp[1]=='' or temp[1]=='None' or temp[1]==None or temp[1]=="b''":
                temp[1]=-1
            else:
                temp[1]=b64encode(temp[1]).decode("utf-8")
            l+=[temp]
        count=db.session.execute("select count(*) from user u, likes l where u.user_id=l.user_id and l.blog_id=:bid order by like_id DESC ",{"bid":blog_id})
        count=list(count.fetchall()[0])
        if len(count)==0:
            count=0
        else:
            count=count[0]
        return l,count

