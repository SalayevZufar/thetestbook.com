from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from datetime import datetime

from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

class Student(db.Model, UserMixin):

    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("First name", db.String(20), nullable=False)
    last_name = db.Column("Last name", db.String(20), nullable=False)
    birth_date = db.Column("Birth date", db.String(15), nullable=False)
    username = db.Column("Username", db.String(100), unique=True, nullable=False)
    email = db.Column("Email", db.String(50), unique=True, nullable=False)
    gender = db.Column("Gender", db.String(10), nullable=False)
    signup_as = db.Column("Sign up as", db.String(10), nullable=False)
    image_file = db.Column("Profile pic", db.String(20), nullable=False,default='default.jpg')
    password = db.Column("password", db.String(120), nullable=False)
    bio = db.Column("Bio",db.String(100),default=None)
    country = db.Column("Country",db.String(100),default=None)
    address = db.Column("Address",db.String(100),default=None)
    phone_number = db.Column("Phone number",db.String(20),default="(+123)456789")
    created_date = db.Column(DateTime(timezone=True), server_default=func.now())
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Like', backref='author',  passive_deletes=True)
    a_friends = db.relationship('UserFriend',
                                primaryjoin=lambda: Student.id == UserFriend.friend_a_id,
                                back_populates='friend_a')
    my_friends = association_proxy('a_friends', 'friend_a',
                                      creator=lambda u: UserFriend(friend_b=u))

    b_friends = db.relationship('UserFriend',
                                primaryjoin=lambda: Student.id == UserFriend.friend_b_id,
                                back_populates='friend_b')
    im_their_friend = association_proxy('b_friends', 'friend_b',
                                           creator=lambda u: UserFriend(friend_a=u))
    def __repr__(self):
        return f"User('{self.first_name}','{self.password}','{self.username}')"
    def as_dict(self):
        return {'name': self.username}
    
class UserFriend(db.Model):
    
    friend_a_id = db.Column(db.ForeignKey('student.id'), primary_key=True)
    friend_a = db.relationship('Student',
                               primaryjoin=friend_a_id == Student.id,
                               back_populates='a_friends')

    friend_b_id = db.Column(db.ForeignKey('student.id'), primary_key=True)
    friend_b = db.relationship('Student',
                               primaryjoin=friend_b_id == Student.id,
                               back_populates='b_friends')

    # other columns here

    def __init__(self, friend_a=None, friend_b=None, **kwargs):
        super().__init__(**kwargs)
        if friend_a:
            self.friend_a = friend_a
        if friend_b:
            self.friend_b = friend_b

class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("Title", db.String(100), nullable=False)
    picture = db.Column("Post picture", db.String(20))
    date_posted = db.Column("Posted date",DateTime(timezone=True),nullable=False, default=datetime.utcnow)
    content = db.Column("Content", db.Text(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"


    


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)


# class Like(db.Model):
#     id = db.Column("id", db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
#     date_liked = db.Column("Liked date",DateTime(timezone=True),nullable=False, default=datetime.utcnow)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)