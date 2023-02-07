from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode
from .userfunctions import *

class blogfunctions:

    def top_feeds(self):
        db.session.execute("")
        pass

    def next_blog_id(self):
        bid=db.session.execute("select max(blog_id) from blogs")
        bid=list(bid.fetchall())
        #print(bid)
        if len(bid)!=0:
            bid=list(bid[0])
            if len(bid)!=0 and bid[0]!=None:
                bid=bid[0]
                return bid+1
        return 0

    def create_blog(self,title,content,bp,user_id):
        post_time=time_calc().time()
        b_id=blogfunctions().next_blog_id()
        #print(b_id)
        db.session.execute("insert into blogs(user_id, title, content, post_time, blog_image, blog_id, edited) values (:id, :t, :c, :pt, :bi, :b_id, :e)", {"id":int(user_id),"t":title,"c":content,"bi":bp,"pt":post_time, "b_id":b_id, "e":0})
        db.session.commit()
        details=db.session.execute("select * from blogs where post_time=:pt",{"pt":post_time})
        details=list(details.fetchall()[0])
        #print(details)
        if details[5]=='' or details[5]=='None' or details[5]==None or details[5]=="b''" or str(details[5])=="b''":
            details[5]=-1
        else:
            details[5]=b64encode(details[5]).decode("utf-8")
       
        user_details=db.session.execute("select user_id,username,profile_picture,gender from user where user_id=:id",{"id":user_id})
        user_details=list(user_details.fetchall()[0])
        if user_details[2]=='' or user_details[2]=='None' or user_details[2]==None or user_details[2]=="b''" or str(user_details[2])=="b''":
            user_details[2]=-1
       
        else:
            user_details[2]=b64encode(user_details[2]).decode("utf-8")
        return user_details,details
    
    def blogs_from_email(self,email):
        user_id=userfunctions().get_uid_from_email(email)
        details=db.session.execute("select * from blogs where user_id=:id",{"id":user_id})
        details=list(details.fetchall()[0])
        if details[5]=='' or details[5]=='None' or details[5]==None or details[5]=="b''" or str(details[5])=="b''":
            details[5]=-1
       
        else:
            details[5]=b64encode(details[5]).decode("utf-8")
        return details

    def blog_with_id(self,blog_id, user_id):
        #print("this is blog_with_id",'blog_id',type(blog_id))
        details=db.session.execute("select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id=:uid) then 1 else 0 end as like, b.edited from blogs b, user u where b.user_id=u.user_id and b.blog_id=:id order by blog_id",{"id":blog_id, "uid":user_id})
        l=[]
        '''
        0 b.blog_id, 
        1 b.title, 
        2 b.content, 
        3 b.post_time, 
        4 b.blog_image, 
        5 u.username,
        6 u.profile_picture, 
        7 u.gender, 
        8 u.user_id
        9 like
        10 b.edited
        '''
        for i in details:
            temp=list(i)
            #print(temp[4])
            temp[3]=time_calc().convert(temp[3])

            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''"  or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            if temp[6]=='' or temp[6]=='None' or temp[6]==None or temp[6]=="b''" or str(temp[6])=="b''":
                temp[6]=-1
            else:
                temp[6]=b64encode(temp[6]).decode("utf-8")
            l+=[temp]
        #print(l)
        return l

    def my_blogs(self,email):
        user_id=userfunctions().get_uid_from_email(email)
        details=db.session.execute("select blog_id, title, content, post_time, blog_image from blogs where user_id=:id order by blog_id DESC",{"id":user_id})
        l=[]
        for i in details:
            temp=list(i)
            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''"  or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            l+=[temp]
        return l

    def my_blogs_2(self,user_id,my_id):
        details=db.session.execute("select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id=:my_id) then 1 else 0 end as like, b.edited from blogs b, user u where b.user_id=u.user_id and u.user_id=:id order by b.blog_id DESC",{"id":user_id,"my_id":my_id})
        l=[]
        '''
        0 b.blog_id, 
        1 b.title, 
        2 b.content, 
        3 b.post_time, 
        4 b.blog_image, 
        5 u.username,
        6 u.profile_picture, 
        7 u.gender, 
        8 u.user_id
        9 like
        10 b.edited
        '''
        for i in details:
            temp=list(i)
            #print(temp[4])
            temp[3]=time_calc().convert(temp[3])
            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''"  or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            if temp[6]=='' or temp[6]=='None' or temp[6]==None or temp[6]=="b''"  or str(temp[6])=="b''":
                temp[6]=-1
            else:
                temp[6]=b64encode(temp[6]).decode("utf-8")
            l+=[temp]
        return l

    def user_feeds(self,user_id):
        details=db.session.execute("select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id=:id) then 1 else 0 end as like,b.edited from blogs b, user u where b.user_id=u.user_id and (u.user_id in (select user_id from follows where follower_id=:id) or u.user_id=:id) order by b.blog_id DESC",{"id":user_id})
        l=[]
        '''
        0 b.blog_id, 
        1 b.title, 
        2 b.content, 
        3 b.post_time, 
        4 b.blog_image, 
        5 u.username,
        6 u.profile_picture, 
        7 u.gender, 
        8 u.user_id
        9 like
        10 edited
        '''
        for i in details:
            temp=list(i)
            temp[3]=time_calc().convert(temp[3])

            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''" or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            if temp[6]=='' or temp[6]=='None' or temp[6]==None or temp[6]=="b''"  or str(temp[6])=="b''":
                temp[6]=-1
            else:
                temp[6]=b64encode(temp[6]).decode("utf-8")
            l+=[temp]
        return l

    def top_feeds(self,user_id):
        #a="select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id=:id) then 1 else 0 end as like, k.c from blogs b, user u, (select blog_id,user_id, count(blog_id) as c from (select blog_id,user_id from likes UNION all select blog_id,user_id from comments) GROUP by blog_id ORDER by c DESC) k where b.blog_id=k.blog_id and u.user_id=k.user_id; "
        details=db.session.execute("select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id=:id) then 1 else 0 end as like, b.edited, k.c from blogs b, user u, (select blog_id,user_id, count(blog_id) as c from (select blog_id,user_id from likes UNION all select blog_id,user_id from comments) GROUP by blog_id ORDER by c DESC) k where b.blog_id=k.blog_id and u.user_id=b.user_id",{"id":user_id})
        l=[]
        '''
        0 b.blog_id, 
        1 b.title, 
        2 b.content, 
        3 b.post_time, 
        4 b.blog_image, 
        5 u.username,
        6 u.profile_picture, 
        7 u.gender, 
        8 u.user_id
        9 like
        10 edited
        11 count
        '''
        for i in details:
            temp=list(i)
            temp[3]=time_calc().convert(temp[3])
            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''" or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            if temp[6]=='' or temp[6]=='None' or temp[6]==None or temp[6]=="b''"  or str(temp[6])=="b''":
                temp[6]=-1
            else:
                temp[6]=b64encode(temp[6]).decode("utf-8")
            l+=[temp]
        return l

    def search_a_post(self,pattern,user_id):
        query='select b.blog_id,b.title, b.content, b.post_time, b.blog_image, u.username, u.profile_picture, u.gender, u.user_id, case when b.blog_id in (select blog_id from likes where user_id='+str(user_id)+') then 1 else 0 end as like,b.edited from blogs b, user u where b.user_id=u.user_id and b.title like'+"'%"+pattern+"%'"+' order by b.blog_id DESC'
        details=db.session.execute(query)
        l=[]
        '''
        0 b.blog_id, 
        1 b.title, 
        2 b.content, 
        3 b.post_time, 
        4 b.blog_image, 
        5 u.username,
        6 u.profile_picture, 
        7 u.gender, 
        8 u.user_id
        9 like
        10 edited
        '''
        for i in details:
            temp=list(i)
            temp[3]=time_calc().convert(temp[3])

            if temp[4]=='' or temp[4]=='None' or temp[4]==None or temp[4]=="b''" or str(temp[4])=="b''":
                temp[4]=-1
            else:
                temp[4]=b64encode(temp[4]).decode("utf-8")
            if temp[6]=='' or temp[6]=='None' or temp[6]==None or temp[6]=="b''"  or str(temp[6])=="b''":
                temp[6]=-1
            else:
                temp[6]=b64encode(temp[6]).decode("utf-8")
            l+=[temp]
        return l

    def edit_blog(self,b_id,t,c,bi):
        old_d=db.session.execute("select blog_id, title, content, blog_image, user_id from blogs where blog_id=:b_id",{"b_id":b_id})
        old_d=list(old_d.fetchall()[0])
        if t=="":
            t1=old_d[1]
        else:
            t1=t
        if c=="":
            c1=old_d[2]
        else:
            c1=c
        if bi=='' or bi=='None' or bi==None or bi=="b''" or str(bi)=="b''":
            bi1=old_d[3]
        else:
            bi1=bi
        pt=time_calc().time()
        db.session.execute("update blogs set title=:t1, content=:c1, blog_image=:bi1, post_time=:pt, edited=1 where blog_id=:b_id",{"b_id":b_id,"t1":t1,"c1":c1,"bi1":bi1, "pt":pt})
        db.session.commit()
        return

    def latest_posts(self,uid):
        details=db.session.execute("select blog_id,title, content, blog_image,post_time,edited from blogs where user_id=:id order by blog_id DESC limit 3",{"id":uid})
        details=list(details.fetchall())
        #print(details)
        l=[]
        for i in details:
            temp=list(i)
            temp[4]=time_calc().convert(temp[4])
            if temp[3]=='' or temp[3]=='None' or temp[3]==None or temp[3]=="b''" or str(temp[3])=="b''":
                temp[3]=-1
            else:
                temp[3]=b64encode(temp[3]).decode("utf-8")
            l+=[temp]
        #print(l[0][3]=='')
        return l
    
    def delete_blog(self,bid):
        db.session.execute("delete from blogs where blog_id=:bid",{"bid":bid})
        db.session.execute("delete from likes where blog_id=:bid",{"bid":bid})
        db.session.execute("delete from comments where blog_id=:bid",{"bid":bid})
        db.session.commit()
        return 