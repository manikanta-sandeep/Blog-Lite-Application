from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode
from .userfunctions import *

class followfunctions:
    def follow(self,follow_id,follower_id):
        follow_time=time_calc().time()
        db.session.execute("insert into follows(user_id,follower_id,follow_time) values (:uid, :fid, :ft)",{"fid":follower_id,"uid":follow_id,"ft":follow_time})
        db.session.commit()
        return 

    def get_all_whom_following(self,user_id):
        details=db.session.execute("select u.username,u.user_id,u.profile_picture,u.gender,u.email from user u, follows f where u.user_id=f.user_id and f.follower_id=:user_id",{"user_id":user_id})
        username=db.session.execute("select username from user where user_id=:uid",{"uid":user_id})
        username=username.fetchall()
        if len(username)!=0:
            un=list(username[0])[0]
        l=[]
        for i in details:
            temp=list(i)
            if temp[2]=='' or temp[2]=='None' or temp[2]==None or temp[2]=="b''" or str(temp[2])=="b''":
                temp[2]=-1
            else:
                temp[2]=b64encode(temp[2]).decode("utf-8")
            l+=[temp]
        return l,un

    def get_all_followers(self,user_id):
        details=db.session.execute("select u.username,u.user_id,u.profile_picture,u.gender,u.email,case when f.follower_id in (select user_id from follows where follower_id=:uid) then 1 else 0 end as revfollow from user u, follows f where u.user_id=f.follower_id and f.user_id=:uid",{"uid":user_id})
        l=[]
        username=db.session.execute("select username from user where user_id=:uid",{"uid":user_id})
        username=username.fetchall()
        if len(username)!=0:
            un=list(username[0])[0]
        for i in details:
            temp=list(i)
            if temp[2]=='' or temp[2]=='None' or temp[2]==None or temp[2]=="b''" or str(temp[2])=="b''":
                temp[2]=-1
            else:
                temp[2]=b64encode(temp[2]).decode("utf-8")
            l+=[temp]
        return l,un

    def unfollow(self,uid,fid):
        db.session.execute("delete from follows where user_id=:uid and follower_id=:fid",{"uid":uid,"fid":fid})
        db.session.commit()
        return 


    def isfollower(self,uid,fid):
        d1=db.session.execute("select * from follows where user_id=:uid and follower_id=:fid",{"uid":uid,"fid":fid})
        d2=db.session.execute("select * from follows where user_id=:uid and follower_id=:fid",{"uid":fid,"fid":uid})
        (d1,d2)=(list(d1.fetchall()),list(d2.fetchall()))
        #print(d1,d2)
        if len(d2)==0:
            if len(d1)==0:
                return [-1,-1]
            else:
                return [1,list(d1[0])]
        else:
            return [2,list(d2[0])]
        return 