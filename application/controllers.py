from flask import render_template, redirect, request, session, flash
from flask import current_app as app
from .database import db 
from .userfunctions import *
from .blogfunctions import *
from .followfunctions import *
from .commentfunctions import *
from .likefunctions import *


@app.route("/", methods=["GET","POST"])
def index_page():
    
    if request.method=="GET":
        return render_template("index_page.html")
    else:
        return render_template("index_page.html")


@app.route("/login",methods=["GET","POST"])
def login_page():
    session.clear()
    db.session.commit()
    if request.method=="POST" or request.method=="GET":
        return render_template("login_page.html",option=1,invalid=0)



@app.route("/create_account/send_verification",methods=["GET","POST"])
def create_account():
    if request.method=="GET":
        return render_template("login_page.html",option=5, invalid=0)

@app.route("/create_account/verify_code", methods=["GET","POST"])
def verify_code():
    if request.method=="POST":
        session["email"]=request.form["email"]
        uf=userfunctions()
        if uf.user_status(session["email"])==1:
            return render_template("login_page.html", option=8, key=1)
        else:
            uf.send_verification(session["email"])
            return render_template("login_page.html",option=6,inavlid=0)


@app.route("/create_account/check_code", methods=["GET","POST"])
def check_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continuing to creating account
            return render_template("login_page.html",option=7, mail=session["email"], invalid=0 )
        else:
            #redirecting to enter verification code correctly
            return render_template("login_page.html",option=6, invalid=1)

@app.route("/account_created", methods=["GET","POST"])
def account_created():
    #(username,name,dob,pp,p,cp,g)
    l=[request.form["username"],request.form["name"], request.form["dob"], request.files["profile_picture"].read(), request.form["password"], request.form["confirm_password"], request.form["flexRadioDefault"]]  
    uf=userfunctions()
    
    if l[4]==l[5]:
        uf.join_user(session["email"],l[0],l[1],l[2],l[4],l[3],l[6])
        return render_template("index_page.html",option=8)
    else:
        return render_template("index_page.html",option=7,invalid=1)
            
@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    if request.method=="GET":
        return render_template("login_page.html",option=2)

@app.route("/forgot_password/verify_code", methods=["GET","POST"])
def fp_send_verification():
    if request.method=="POST":
        mail=request.form["email"]
        session["email"]=mail
        uf=userfunctions()
        code=uf.forgot_send_verification(mail)
        if code==-1:
            return render_template("login_page.html",option=2,invalid=1)
        else:
            return render_template("login_page.html",option=3,invalid=0)
        

@app.route("/forgot_password/check_code", methods=["GET","POST"])
def fp_verify_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continue to resetting password
            return render_template("login_page.html",option=9, invalid=0)
            
        else:
            #verification code not matched 
            return render_template("login_page.html",option=3, inavlid=1)
            
@app.route("/forgot_password/check_password",methods=["GET","POST"])
def check_rp_password():
    if request.method=="POST":
        p=request.form["password"]
        cp=request.form["confirm_password"]
        if p==cp:
            uf=userfunctions()
            uf.fp_update_password(session["email"],p)
            session.clear()
            return render_template("login_page.html",option=4,invalid=0)
            #update password
        else:
            return render_template("login_page.html",option=9, invalid=1)

@app.route("/home",methods=["GET","POST"])
def home():
    #print("coming into home", request.method)
    if request.method=="GET":
        #print("POST Coming")
        d=blogfunctions().user_feeds(session["user_id"])
        user_data=userfunctions().post_user_details(session["email"])
        top_feed=blogfunctions().top_feeds(session["user_id"])
        return render_template("blog_feeds.html", un=session["username"], option=1, d=d, ud=user_data, h=1, tf=top_feed)
    if request.method=="POST":
        #print("GET Coming")
        try:
            #print("try coming")
            if session["on"]==1:
                #print("on coming")
                d=blogfunctions().user_feeds(session["user_id"])
                top_feed=blogfunctions().top_feeds(session["user_id"])
                user_data=userfunctions().post_user_details(session["email"])
                return render_template("blog_feeds.html", un=session["username"], option=1, d=d, ud=user_data,h=1, tf=top_feed)
        except:
            print("on not coming")
            return redirect("/login")


@app.route("/check", methods=["GET","POST"])
def check_login():
    print(request.method)
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        a=userfunctions().check_username(email)
        if a==-1:
            print("value of a",a)
            return render_template("login_page.html",option=1, invalid=1, nr=1)
        else:
            a=list(a)
            print("value of a",a)
            if a[6]==password:
                session["email"]=email
                session["on"]=1
                if a[0]==None:
                    return render_template("login_page.html",option=7, key=1, data=a)
                else:
                    session["user_id"]=a[5]
                    session["username"]=a[0]
                    return redirect("/home")
            else:
                return render_template("login_page.html",option=1, invalid=1) 




@app.route("/account_modified", methods=["GET","POST"])
def account_modified():
    if session["on"]!=1:
        return redirect("/login")
    if request.method=="POST":
        email=session["email"]
        username=request.form["username"]
        name=request.form["name"]
        dob=request.form["dob"]
        gender=request.form["flexRadioDefault"]
        pp=request.files["profile_picture"].read()
        session["user_id"]=userfunctions().modify_account(session["email"],username,name,dob,gender,pp)
        session["username"]=username
        session["on"]=1
        return redirect("/home")



@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/login") 


@app.route("/account", methods=["GET","POST"])
def account():
    db.session.commit()
    details=userfunctions().account_details(session["email"])
    follow_details=userfunctions().follow_details(0,session["email"])
    latest_posts=blogfunctions().latest_posts(session["user_id"])
    return render_template("blog_account.html", data=details, un=session["username"], option=1, fd=follow_details, lp=latest_posts)


@app.route("/delete_user", methods=["GET","POST"])
def delete_user():
    userfunctions().delete_account(session["email"])
    session.clear()
    return redirect("/login")

@app.route("/update_account", methods=["GET","POST"])
def update_account():
    details=userfunctions().account_details(session["email"])
    return render_template("blog_account.html",data=details, un=session["username"], option=2)

@app.route("/account_update", methods=["GET","POST"])
def account_update():
    un=request.form["username"]
    n=request.form["name"]
    dob=request.form["dob"]
    g=int(request.form["flexRadioDefault"])
    pp=request.files["profile_picture"].read()
    session["username"]=userfunctions().update_profile(session["email"],un,n,dob,g,pp)
    return redirect("/account")

@app.route("/search_a_user", methods=["GET","POST"])
def search_a_user():
    pattern=request.form["pattern"]
    details=userfunctions().search_users(pattern,session["user_id"])
    return render_template("blog_feeds.html", un=session["username"],option=2, d=details, key=1, f=1, pattern=pattern)


@app.route("/all_users", methods=["GET","POST"])
def all_users():
    details=userfunctions().get_all_users(session["user_id"])
    return render_template("blog_feeds.html",un=session["username"],option=2, d=details, key=1)

@app.route("/admin", methods=["GET","POST"])
def admin():
    details=userfunctions().admin_all_users()
    return render_template("admin.html", un=session["username"], d=details)

@app.route("/admin-delete/<did>", methods=["GET","POST"])
def admin_delete(did):
    userfunctions().admin_delete(int(did))
    return redirect("/admin")

@app.route("/search_post", methods=["GET","POST"])
def search_post():
    pattern=request.form["post_pattern"]
    details=blogfunctions().search_a_post(pattern,session["user_id"])
    user_data=userfunctions().post_user_details(session["email"])

    return render_template("blog_feeds.html",option=1, d=details,un=session["username"], ud=user_data,p=pattern, q=1)

@app.route("/user/<id>", methods=["GET","POST"])
def users(id):
    if int(id)==int(session["user_id"]):
        return redirect("/account")
    get_details=userfunctions().user_details(id)
    follow_details=userfunctions().follow_details(1,id)
    follows=followfunctions().isfollower(id,session["user_id"])
    latest_posts=blogfunctions().latest_posts(id)
    return render_template("blog_account.html",option=1,lp=latest_posts,data=get_details, un=session["username"],fd=follow_details,ou=1, follows=follows)

@app.route("/create_a_post", methods=["GET","POST"])
def create_a_post():
    db.session.commit()
    title=request.form["title"]
    content=request.form["content"]
    bp=request.files["bp"]
    a=bp.filename
    exten=['jpg','jpeg','png']
    ls=a.split('.')
    print(ls[-1])
    if (ls[-1] in exten)==False:
        return 'Not a valid file'
    bp=bp.read()
    user_id=request.form["id"]
    d=blogfunctions().create_blog(title,content,bp,user_id)
    return redirect("/my_posts")


@app.route("/follow", methods=["GET","POST"])
def follow():
    follow_id=request.form["follow"]
    follower_id=session["user_id"]
    followfunctions().follow(follow_id,follower_id)
    return redirect("/all_users")

@app.route("/unfollow", methods=["GET","POST"])
def unfollow():
    other_id=request.form["unfollow"]
    followfunctions().unfollow(other_id,session["user_id"])
    return redirect("/all_users")

@app.route("/followers/follow", methods=["GET","POST"])
def followersfollow():
    follow_id=request.form["follow"]
    follower_id=session["user_id"]
    followfunctions().follow(follow_id,follower_id)
    return redirect("/followers")

@app.route("/followers/unfollow", methods=["GET","POST"])
def followersunfollow():
    other_id=request.form["unfollow"]
    followfunctions().unfollow(other_id,session["user_id"])
    return redirect("/followers")


@app.route("/following/unfollow", methods=["GET","POST"])
def followingunfollow():
    other_id=request.form["unfollow"]
    followfunctions().unfollow(other_id,session["user_id"])
    return redirect("/following")

@app.route("/following",methods=["GET","POST"])
def following():
    data,usn=followfunctions().get_all_whom_following(session["user_id"])
    return render_template("blog_feeds.html", option=2, key=2, d=data, un=session["username"],p=1)

@app.route("/followers",methods=["GET","POST"])
def followers():
    data,usn=followfunctions().get_all_followers(session["user_id"])
    #print(data)
    return render_template("blog_feeds.html", option=2, key=2, d=data, un=session["username"],p=2)

@app.route("/my_posts", methods=["GET","POST"])
def my_posts():
    d=blogfunctions().my_blogs_2(session["user_id"],session["user_id"])
    user_data=userfunctions().post_user_details(session["email"])
    return render_template("blog_feeds.html",d=d,un=session["username"],option=1,ud=user_data )
    #return render_template("blog_feeds.html", un=session["username"], option=1, d=d, ud=user_data)

@app.route("/user/following/<int:uid>",methods=["GET","POST"])
def otheruser_following(uid):
    data,usn=followfunctions().get_all_whom_following(uid)
    return render_template("blog_feeds.html", option=2, key=2, d=data, un=session["username"],p=1,ou=1,usn=usn)

@app.route("/user/followers/<int:uid>",methods=["GET","POST"])
def otheruser_followers(uid):
    data,usn=followfunctions().get_all_followers(uid)
    return render_template("blog_feeds.html", option=2, key=2, d=data, un=session["username"],p=2, ou=1,usn=usn)

@app.route("/user/posts/<int:uid>", methods=["GET","POST"])
def otheruser_my_posts(uid):
    d=blogfunctions().my_blogs_2(uid, session["user_id"])
    oun=userfunctions().un_with_id(int(uid))
    pdl="user_posts_"+str(uid)
    user_data=userfunctions().post_user_details(session["email"])
    return render_template("blog_feeds.html",d=d,un=session["username"],option=1,ud=user_data,l=1, pdl=pdl ,ou=1,oun=oun)
    #return render_template("blog_feeds.html", un=session["username"], option=1, d=d, ud=user_data)

@app.route("/delete/<bid>", methods=["GET","POST"])
def delete_post(bid):
    blogfunctions().delete_blog(int(bid))
    return redirect("/my_posts")
    

@app.route("/comment", methods=["GET","POST"])
def comment():
    comment=request.form["comment"]
    blog_id=request.form["blog_id"]
    commentfunctions().addcomment_email(session["email"],blog_id,comment)
    return redirect("/postdetails/"+blog_id)

@app.route("/postdetails/<b_id>", methods=["GET","POST"])
def post_details(b_id):
    #print('blog_id',"is this id", type(b_id))
    comment_d,blog_d,cc=commentfunctions().allcomments(b_id, session["user_id"])
    #print(comment_d)
    #Comments will return 
    #username, pp, g, uid, cid, comment, time 
    like_d,lc=likefunctions().get_all_likes_of(b_id)
    #username,profile_picture,gender,user_id,like_id,liked_time
    user_data=userfunctions().post_user_details(session["email"])
    pdl="postdetails"
    return render_template("blog_feeds.html",un=session["username"],d=blog_d, ud=user_data,option=1,comment_d=comment_d, like_d=like_d , lc=lc , cc=cc , pd=1 ,l=1, pdl=pdl)

@app.route("/edit_post", methods=["GET","POST"])
def edit_post():
    b_id=request.form["blog_id"]
    t=request.form["title"]
    c=request.form["content"]
    bi=request.files["bp"].read()
    blogfunctions().edit_blog(b_id,t,c,bi)
    return redirect("/postdetails/"+str(b_id))

@app.route("/like/<string:url>/<int:bid>", methods=["GET","POST"])
def like(url,bid):
    #print("Coming to like view")
    if url=="postdetails":
        url=url+"/"+str(bid)
    #print(url[:10])
    if url[:10]=="user_posts":
        k=userfunctions().retrieve(url)
        url=k[0]
    likefunctions().addlike(session["user_id"], int(bid))
    return redirect("/"+str(url)+"#post-"+str(bid))


@app.route("/unlike/<string:url>/<int:bid>", methods=["GET","POST"])
def unlike(url,bid):
    #print("Coming to like view")
    if url=="postdetails":
        url=url+"/"+str(bid)
    if url[:10]=="user_posts":
        k=userfunctions().retrieve(url)
        url=k[0]
    likefunctions().unlike(session["user_id"], int(bid))
    return redirect("/"+str(url)+"#post-"+str(bid))


