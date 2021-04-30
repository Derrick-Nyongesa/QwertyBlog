from ..requests import get_quotes
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Post
from .. import db,photos
from flask_login import login_required,current_user
from .forms import UpdateProfile,NewPost

@main.route('/')
def index():
    quotes = get_quotes()
    posts = Post.query.all()
    return render_template('index.html', quotes=quotes, posts=posts, current_user=current_user)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post=form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('newPost.html', title='New Post', form=form)


@main.route("/blog/<int:id>")
def blog(id):
    post = Post.query.get(id)
    return render_template('blog.html',post=post)


@main.route("/blog/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_blog(id):
    post = Post.query.get(id)
    if post.user != current_user:
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.post = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.post
    return render_template('newPost.html', title='Update Post', form=form)