import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """Model for the user table.
    
    Represents a user on the website.
    
    Parameters
    ----------
    id : int
        Unique id which is different for all users.
    username : str
        String for username which the user can pick and also change.
    email : str
        String that holds the user's email, for notifications.
    password_hash : str
        Contains the hashed password, for security purposes.
    posts : method
        Contains an sql query for all of the user's posts.
    
    Relationships
    -------------
    User-Post = One to many relationship"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), index=True, unique=True)
    email = db.Column(db.String(300), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return self.username  

    def set_password(self, password):
        """Sets the user's password hash, so that it is safer."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the password hash is equal to the plain text password."""
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """Model for the posts table.
       
    Represents the posts made by a user on the website.
    
    Parameters
    ----------
    id : int
        Unique number that is different for all posts.
        
    text : str
        The main part of the post, so the text.
    timestamp: int
        The time at which the post was made.
    user_id : int
        The unique id of the user that originally made the post.
    title : str
        The title of the post.
    comments : method
        Sql query for all of the comments made in the post.

    score : int
        Upvotes - Downvotes of a post.
    upvotes : int
        The number of times a user has voted the post up.
    downvotes : int
        The number of times a user has voted the post down.
    importance : int
        The number of times a user has given a post importance.
    hotness : int
        Number which posts will be sorted by.

    age : int
        How old a post is, compared to the epoch time.
    topics : method
        Sql query which returns a list of all the topics a post has.

    created_on : int
       Same deal as the timestamp...

    Relationships
    --------------
    Posts-Comments = One to Many
    Posts-Topics = Many to Many
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1000))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    age = db.Column(db.Integer)

    created_on = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Post {}>'.format(self.text)

class Comment(db.Model):
    """Model for the comments table
    
    Represents the comments made in a specific post.
    
    Parameters
    ----------
    id : int
        Unique id used to find specific comments.
    user_id : int
        Unique id of the user that originally made the post.
    username : str
        The name of the user that made the comment
    text : str
        The comment itself, so the text in the comment.
    timestamp : int
        The time at which the comment was made.

    Relationships
    ------------
    Posts-Comments = One to Many
        """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    username = db.Column(db.String(500))
    text = db.Column(db.String(20000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.text)

@login.user_loader
def load_user(id):
    """Gets a user from it's id, definitely deprecated once I get to it."""
    return User.query.get(int(id))

def find_users_post(user):
    """Fetches the user of a post, will be deprecated some day..."""
    posts = Post.query.all()
    user_posts = []
    for post in posts:
        if post.author.id == user.id:
            user_posts.append(post)

    return user_posts
