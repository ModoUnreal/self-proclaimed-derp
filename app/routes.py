from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user
from werkzeug.urls import url_parse
from app.helpers import redirect_url
from app.models import User, Post, Comment, find_users_post
from app.forms import CommentForm, SubmitForm, SearchForm
from app import app, db


@app.route('/')
@app.route('/index')
def index():
    """View function for the index site, basically the main site."""
    posts = Post.query.all()   
    return render_template('index.html', title='Dopenet: You can do anything', posts=posts )

@app.route('/user/<username>')
def user(username):
    """View function for the user profile page. May become deprecated
       as there isn't much use for it, except for listing specific posts."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = find_users_post(user)
    return render_template('user.html', user=user, posts=posts)

@app.route('/item/<post_id>', methods=['GET', 'POST'])
def item(post_id):
    """Shows a specific item, which is specified by it's unique id.
       Also contains a basic form for submitting comments, which are
       yet to be sorted by popularity."""

    post = Post.query.filter_by(id=post_id).first_or_404()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data, post_id=post.id,
                user_id=current_user.id, username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('item', post_id=post_id))

    comments = Comment.query.filter_by(post_id=post.id)
    user = post.author
    return render_template('item.html', user=user, post=post,
            comments=comments, form=form)


@app.route('/delete_comment/<post_id>/<comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    """View function which deletes comments, specifically a POST method
       for obvious reasons."""
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment != None:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('item', post_id=post_id))



@app.route('/search', methods=['GET', 'POST'])
def search():
    """View function which takes inputted data from a search bar and passes
       it on to the search_result function, to be made into a search_query."""
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        search_str = form.search_str.data
        return redirect(url_for('search_result', search_str=str(search_str)))

    return redirect(url_for('search_result', search_str=form.search_str.data))

@app.route('/search_result/<search_str>', methods=['GET'])
def search_result(search_str):
    """Makes a post_query which contains any posts with
       similar names."""
    post_query = Post.query.filter_by(title=search_str).all()

    return render_template('search_result.html', post_query=post_query)

@app.route('/faq', methods=['GET'])
def faq():
    """Returns the faq html file."""
    return render_template('faq.html')

@app.route('/contact', methods=['GET'])
def contact():
    """Returns the contact html file."""
    return render_template('contact.html')

@app.route('/past_future', methods=['GET'])
def past_future():
    return render_template('past_future.html')
