from ..requests import get_quotes
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Post,Comment,Subscriber
from .. import db,photos
from flask_login import login_required,current_user
from .forms import UpdateProfile,NewPost,CommentForm
from ..email import mail_message

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
    subscribers = Subscriber.query.all()
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post=form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,post=post)
        flash('You Posted a new Blog')
        return redirect(url_for('main.index'))
    return render_template('newPost.html', title='New Post', form=form)


@main.route("/blog/<int:id>")
def blog(id):
    post = Post.query.get(id)
    comments = Comment.query.filter_by(post_id=id).all()
    return render_template('blog.html',post=post,comments=comments)


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


@main.route("/blog/<int:id>/delete", methods=['GET'])
@login_required
def delete_blog(id):
    post = Post.query.get(id)
    if post.user != current_user:
        abort(403)
    post.delete_post()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))


@main.route('/blog/comments/<int:id>', methods=['Post', 'GET'])
@login_required
def new_comment(id):
    form = CommentForm()
    post = Post.query.get(id)
    comments = Comment.query.get(id)
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment( comment = comment, user_id = current_user.id, post_id = id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.blog', id=post.id))
    return render_template('new_comment.html', comment_form=form, title='New Comment',comments=comments , post = post)


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to QwertyBlog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))