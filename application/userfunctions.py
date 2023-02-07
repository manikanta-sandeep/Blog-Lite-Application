from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode



class userfunctions:
    def send_mail_to(self,email,subject,msg):
        e=emailTo()
        e.send_email(subject,email,msg)
        return 1


    def send_verification(self,email):
        e=emailTo()
        password=e.generate_password()
        msg=f'''
Hi ,

Thank you for registering your account on Project BLUE. Hope you will find it easier to use. Here is the verification code, please verify your account with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project BLUE.
        '''
        userfunctions().new_user(email,password)
        return userfunctions().send_mail_to(email,"Verification code for account creation",msg)
        
    def forgot_send_verification(self,email):
        a=userfunctions().check_username(email)
        if a==-1:
            return -1
        else:
            e=emailTo()
            password=e.generate_password()
            msg=f'''
Hi ,

You are recently requested for resetting your password for your account on Project BLUE. Here is the verification code, please reset your account password with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project BLUE.
        '''
            userfunctions().new_user(email,password)
            return userfunctions().send_mail_to(email,"Verification code for Reset Password",msg)
        


    def user_status(self,user_email):
        a=db.session.execute("select password from user where email=:mail",{"mail":user_email})
        no_of_users=a.fetchall()
        if len(no_of_users)==1:
            return 1
        return 0

    def new_user(self,user_email,password):
        join_time=time_calc().time()
        already_present=db.session.execute("select count(*) from user where email=:mail",{"mail":user_email})
        if int(already_present.fetchall()[0][0])==0:
            db.session.execute("insert into user(email,password,joined_time) values (:email,:pwd,:time)",{"email":user_email,"pwd":password, "time":join_time})
        else:
            db.session.execute("update user set password=:password where email=:mail",{"mail":user_email,"password":password})
        db.session.commit()
        return

    def check_user(self,user_email,password):
        a = db.session.execute("select password from user where email=:mail",{"mail": user_email})
        fetched_password = list(a.fetchall())
        print(fetched_password)
        #print(fetched_password,password,fetched_password==password)
        if len(fetched_password) != 0:
            f2=list(fetched_password[0])
            if f2[0]== password:
                return 1
            else:
                return 0
        else:
            return 0

    def join_user(self,email,username,name,dob,password,profile_picture,gender):
        join_time=time_calc().time()
        gender=int(gender)
        #profile_picture=b64encode(profile_picture).decode("utf-8")
        db.session.execute("update user set username=:un, name=:n, dob=:dob, password=:pwd, profile_picture=:pp, gender=:g, joined_time=:jt where email=:mail",{ "mail":email ,"un":username,"n":name,"pwd":password, "dob":dob, "pp":profile_picture, "g":gender , "jt":join_time})
        db.session.commit()
        return

    def fp_update_password(self,email,password):
        db.session.execute("update user set password=:pwd where email=:mail",{"mail":email,"pwd":password})
        db.session.commit()
        return

    def user_name(self,email):
        a=db.session.execute("select user_id,username from user where email=:mail",{"mail":email})
        u_id_name=list(a.fetchall())
        print(len(u_id_name),"Length")
        return u_id_name

    def account_details(self,email):
        a=db.session.execute("select email,username, name, dob, profile_picture, gender, joined_time,user_id  from user where email=:mail",{"mail":email})
        details=list(a.fetchall()[0])
        if details[4]=='' or details[4]=='None' or details[4]==None or details[4]=="b''" or str(details[4])=="b''":
            details[4]=-1
        else:
            details[4]=b64encode(details[4]).decode("utf-8")
        details[6]=time_calc().convert(details[6])
        return details
    
    def follow_details(self,k,code):
        if k==0:
            user_id=userfunctions().get_uid_from_email(code)
        else:
            user_id=code
        following=db.session.execute("select count(*) from follows where follower_id=:id",{"id":user_id})
        followers=db.session.execute("select count(*) from follows where user_id=:id",{"id":user_id})
        posts=db.session.execute("select count(*) from blogs where user_id=:id",{"id":user_id})
        followers,following,posts=followers.fetchall()[0][0],following.fetchall()[0][0],posts.fetchall()[0][0]
        return [followers,following,posts]



    def delete_account(self,email):
        db.session.execute("delete from user where email=:mail",{"mail":email})
        db.session.commit()
        return

    def update_profile(self,email,un,n,dob,g,pp):
        a=db.session.execute("select email,username,name,dob,gender,profile_picture from user where email=:mail",{"mail":email})
        old_data=a.fetchall()[0]
        if un!='':
            un1=un
        else:
            un1=old_data[1]
        if n!='':
            n1=n
        else:
            n1=old_data[2]
        if dob!='':
            dob1=dob
        else:
            dob1=old_data[3]
        if g!='':
            g1=g
        else:
            g1=old_data[4]
        print(pp)
        if pp=="" or str(pp)=="b''":
            #print('success')
            pp1=old_data[5]
        else:
            pp1=pp
        #print(old_data[1:])
        #print(un,n,dob,g,pp)
        #print(un1,n1,dob1,g1,pp1)
        db.session.execute("update user set username=:un, name=:n, dob=:dob, gender=:g, profile_picture=:pp where email=:mail",{"mail":email,"un":un1,"n":n1,"dob":dob1,"g":g1,"pp":pp1})
        db.session.commit()
        return un1
    def get_all_users(self,user_id):
        #a=db.session.execute("select email,username,profile_picture,gender, user_id from user where email!=:mail",{ "mail":email })
        #a=db.session.execute("select u.email,u.username,u.profile_picture,u.gender,u.user_id,case when f.follower_id=:uid THEN 1 else 0 end as k from user u, follows f where u.user_id=f.user_id and f.user_id!=:uid;",{"uid":user_id})
        a=db.session.execute("select email ,username ,profile_picture, gender, user_id, max(k) from (select u.email,u.username,u.profile_picture,u.gender,u.user_id,case when f.follower_id=:uid and u.user_id=f.user_id THEN 1 else 0 end as k from user u, follows f where f.user_id!=:uid and u.username!='None') where user_id!=:uid group by user_id;",{"uid":user_id})
        a=a.fetchall()
        l=[]
        for i in a:
            temp=list(i)
            if temp[2]=='' or temp[2]=='None' or temp[2]==None or temp[2]=="b''" or str(temp[2])=="b''":
                temp[2]=-1
            else:
                temp[2]=b64encode(temp[2]).decode("utf-8")
            l+=[temp]
        return l

    def search_users(self,pattern,user_id):
        query='select email ,username ,profile_picture, gender, user_id, max(k),name from (select u.email,u.username,u.profile_picture,u.gender,u.user_id,u.name, case when f.follower_id='+str(user_id)+' and u.user_id=f.user_id THEN 1 else 0 end as k from user u, follows f where f.user_id!='+str(user_id)+' and ((u.username like '+"'%"+pattern+"%'"+') or (u.name like '+"'%"+pattern+"%'"+'))) where user_id!='+str(user_id)+' group by user_id'
        a=db.session.execute(query)
        a=a.fetchall()
        l=[]
        for i in a:
            temp=list(i)
            if temp[2]=='' or temp[2]=='None' or temp[2]==None or temp[2]=="b''" or str(temp[2])=="b''":
                temp[2]=-1
            else:
                temp[2]=b64encode(temp[2]).decode("utf-8")
            l+=[temp]
        return l

    

    def check_username(self,email):
        a=db.session.execute("select username,email, name, dob, gender,user_id, password from user where email=:mail",{"mail": email})
        a=list(a.fetchall())
        #print(a)
        if len(a)==0:
            return -1
        return list(a[0]) 

    def modify_account(self,email,username,name,dob,gender,pp):
        old=db.session.execute("select dob,profile_picture,user_id from user where email=:mail",{"mail":email})
        old=old.fetchall()[0]
        if dob=='-1':
            dob=old[0]
        if pp=="" or str(pp)=="b''":
            pp=old[1]
        db.session.execute("update user set username=:un, name=:n, dob=:dob, gender=:g, profile_picture=:pp where user_id=:id",{"id":old[2],"un":username,"n":name, "dob":dob,"g":gender, "pp":pp})
        db.session.commit()
        return old[2]
    
    def user_details(self, id):
        user_email=db.session.execute("select email from user where user_id=:id",{"id":int(id)})
        user_email=user_email.fetchall()[0][0]
        return userfunctions().account_details(user_email)
        
    def home_function(self,email):
        user_details=db.session.execute("select user_id,username,profile_picture,gender from user where email=:mail",{"mail":email})
        user_details=list(user_details.fetchall()[0])
        if user_details[2]=='' or user_details[2]=='None' or user_details[2]==None or user_details[2]=="b''" or str(user_details[2])=="b''":
            user_details[2]=-1       
        else:
            user_details[2]=b64encode(user_details[2]).decode("utf-8")
        return user_details

    def get_uid_from_email(self,email):
        user_id=db.session.execute("select user_id from user where email=:mail",{"mail":email})
        user_id=int(user_id.fetchall()[0][0])
        return user_id

    def post_user_details(self,email):
        data=db.session.execute("select user_id, username, profile_picture, gender,name from user where email=:mail",{"mail":email})
        data=list(data.fetchall()[0])
        if data[2]=='' or data[2]=='None' or data[2]==None or data[2]=="b''" or str(data[2])=="b''":
            data[2]=-1       
        else:
            data[2]=b64encode(data[2]).decode("utf-8")
        return data

    def retrieve(self,s):
        p=s.split("_")
        ul=p[0]+'/'+p[1]+'/'+p[2]
        #print(ul)
        l=ul,int(p[2])
        return l

    def admin_all_users(self):
        a=db.session.execute("select user_id,email, username,name, dob,gender, password, profile_picture, joined_time from user")
        a=a.fetchall()
        l=[]
        for i in a:
            temp=list(i)
            temp[8]=time_calc().convert(temp[8])

            if temp[7]=='' or temp[7]=='None' or temp[7]==None or temp[7]=="b''" or str(temp[7])=="b''":
                temp[7]=-1
            else:
                temp[7]=b64encode(temp[7]).decode("utf-8")
            l+=[temp]
        return l
    def admin_delete(self,did):
        db.session.execute("delete from blogs where user_id=:did",{"did":did})
        db.session.execute("delete from user where user_id=:did",{"did":did})
        db.session.execute("delete from follows where user_id=:did",{"did":did})
        db.session.execute("delete from comments where user_id=:did",{"did":did})
        db.session.execute("delete from likes where user_id=:did",{"did":did}) 
        db.session.commit()
        return

    def un_with_id(self,uid):
        a=db.session.execute("select username from user where user_id=:id",{"id":uid})
        a=list(a.fetchall())
        if len(a)!=0:
            ou=list(a[0])
            oun=ou[0]
            return oun
        return "User"