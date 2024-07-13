import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, request, jsonify, abort, json
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm, UpdateAccountForm, PostForm, SearchForm
from app.models import Student, Post, Like, UserFriend
from flask_login import login_user, logout_user ,current_user, login_required

from sympy.combinatorics.partitions import IntegerPartition 
from sympy import *





@app.route("/profile")
@login_required
def profile():
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    form = RegisterForm()
    last_name = form.last_name.data
    return render_template("profile.html", last_name=last_name, profile_img=profile_img)



@app.route("/", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("profile"))
        else:
            flash('Login error, please check your username or password', 'error')
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    else:
        form = RegisterForm()
        if request.method == 'POST':
            
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                set_birtdate = f"{form.birthdate_day.data}/{form.birthdate_month.data}/{form.birthdate_year.data}"
                student = Student(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password, birth_date=set_birtdate, gender=form.gender.data, signup_as=form.signup_as.data)
                db.session.add(student)
                db.session.commit()
                flash('Your account successufully created, You can now login.', 'success')
                return redirect(url_for("login"))
        return render_template("signup.html", form=form)
   


@app.route("/about")
@login_required
def about():
    return render_template("about.html")



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_photos', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    form = UpdateAccountForm(country=current_user.country)
    
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.country = form.country.data
        current_user.address = form.address.data
        current_user.phone_number = form.phone_number.data
        # current_user.password = form.password.data    
        db.session.commit()
        return redirect(url_for("profile"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.address.data = current_user.address
        form.phone_number.data = current_user.phone_number
    return render_template("account_settings.html", form=form, profile_img=profile_img)


@app.route("/timeline/<username>", methods=['GET','POST'])
@login_required
def other_timeline(username):
    student = Student.query.filter_by(username=username).first()
    
    follow_recuest = request.form.get('data') 
    form = PostForm()
    posts = Post.query.filter_by(student_id=student.id)
    profile_img = url_for('static', filename=f"profile_images/{student.image_file}")
    # process the data using Python code 
    searched_follower_a = UserFriend.query.filter_by(friend_a=current_user, friend_b=student)
    searched_follower_b = UserFriend.query.filter_by(friend_a=student, friend_b=current_user)
    # if search_follower_a or searched_follower_b:
    #     print("True")
    # else:
    #     print("False")
    lists = [None]
    if (follow_recuest == "followed") :
        
        friend = UserFriend(friend_a=current_user, friend_b=student)
        db.session.add(friend)
        db.session.commit()
        
    elif (follow_recuest == "unfollowed") :
        
        delete_follower_a = UserFriend.query.filter_by(friend_a=current_user, friend_b=student)
        delete_follower_b = UserFriend.query.filter_by(friend_a=student, friend_b=current_user)
        for i in delete_follower_a:
            
            db.session.delete(i)
            db.session.commit()
        for i in delete_follower_b:
            
            db.session.delete(i)
            db.session.commit()
    for follower_a in searched_follower_a:
            if (follower_a.friend_a == current_user) and (follower_a.friend_b == student):
                lists.clear()
                lists.append("True")
    for follower_a in searched_follower_b:
            if (follower_a.friend_a == student) and (follower_a.friend_b == current_user):
                lists.clear()
                lists.append("True")
         
    
   
    
    
    return render_template("other_timeline.html", user=student, profile_img=profile_img, form=form, posts=posts, follower = lists) 

@app.route("/timeline", methods=['GET', 'POST'])
@login_required
def timeline():
    form = PostForm()
    posts = Post.query.all()
    
    students = Student.query.all()
   
    if form.validate_on_submit():
        
        if form.picture.data != None:
            if form.picture.data:
                picture_file = save_post_picture(form.picture.data)
                post_image = picture_file
            
            post = Post(title=form.title.data, content=form.content.data, picture=post_image ,author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("timeline"))
        else:
            post = Post(title=form.title.data, content=form.content.data ,author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("timeline"))
    
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    return render_template("timeline.html", profile_img=profile_img, form=form, posts=posts, students=students)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    students = Student.query.all()
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('timeline'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("post.html",profile_img=profile_img,students=students, post=post, form=form)

@app.route("/post/<int:post_id>", methods=['POST','GET'])
@login_required
def delete_post(post_id):
    
        print(post_id)
        post = Post.query.get_or_404(post_id)
    
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('timeline'))




@app.route("/like-post/<int:post_id>", methods=['GET'])
@login_required
def like(post_id):
    print(type(post_id))
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(student_id=current_user.id, post_id=post_id).first()
    if not post:
        print("hello")
    
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(student_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for("timeline"))
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/chat")
@login_required
def chat():
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    
    searched_follower_a = UserFriend.query.filter_by(friend_a=current_user)
    searched_follower_b = UserFriend.query.filter_by(friend_b=current_user)
    
    
    
    return render_template("chat.html", profile_img=profile_img, friends = searched_follower_a, friends_2 = searched_follower_b)

@app.route("/chat/<friend>")
@login_required
def friend_chat(friend):
    print(friend)
    return render_template("chat_friend.html")





@app.route("/user/<username>", methods=['POST','GET'])
@login_required
def user(username):
    student = Student.query.filter_by(username=username).first()
    profile_img = url_for('static', filename=f"profile_images/{student.image_file}")
   
 

    
    follow_recuest = request.form.get('data') 

    
    searched_follower_a = UserFriend.query.filter_by(friend_a=current_user, friend_b=student)
    searched_follower_b = UserFriend.query.filter_by(friend_a=student, friend_b=current_user)
    
    lists = [None]
    if (follow_recuest == "followed") :
        
        friend = UserFriend(friend_a=current_user, friend_b=student)
        db.session.add(friend)
        db.session.commit()
        
    elif (follow_recuest == "unfollowed") :
        
        delete_follower_a = UserFriend.query.filter_by(friend_a=current_user, friend_b=student)
        delete_follower_b = UserFriend.query.filter_by(friend_a=student, friend_b=current_user)
        for i in delete_follower_a:
            
            db.session.delete(i)
            db.session.commit()
        for i in delete_follower_b:
            
            db.session.delete(i)
            db.session.commit()
    for follower_a in searched_follower_a:
        if (follower_a.friend_a == current_user) and (follower_a.friend_b == student):
            lists.clear()
            lists.append("True")
    for follower_a in searched_follower_b:
        if (follower_a.friend_a == student) and (follower_a.friend_b == current_user):
            lists.clear()
            lists.append("True")
    
    return render_template("other_profile.html", user=student, profile_img=profile_img, follower = lists)


@app.route('/friends')
@login_required 
def friends():
    profile_img = url_for('static', filename=f"profile_images/{current_user.image_file}")
    return render_template("friends.html", profile_img = profile_img)
@app.route('/search',methods=["POST","GET"]) 
@login_required
def search(): 
    
        if request.method == 'POST':
            
            search_word = request.form['query']
            
            if search_word == '':
                
                students = Student.query.all()
            else:    
                students = Student.query.filter(Student.username.contains(search_word)).all()
            
        return jsonify({'htmlresponse': render_template('response.html',  users=students)})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

