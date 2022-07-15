from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog_project import db
from flask_blog_project.models import Post, User
from flask_blog_project.posts.forms import PostForm
from flask_blog_project.posts.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/blog")
def allpost():
    page = request.args.get('page', 1, type=int)
    c_p = current_user
    if current_user.is_authenticated:
        posts_list = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=6)
    else:
        userid = User.query.filter_by(username='e-kondra').first().id
        posts_list = Post.query.filter(Post.user_id == userid).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('blog.html', posts=posts_list)


@posts.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == 'POST':
        if form.picture.data:
            picture_name = save_picture(form.picture.data)

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user, image_file=picture_name)
        db.session.add(post)
        db.session.commit()
        flash('The Post was successfully created!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html',
                           title='New Post', image_file=form.picture.data, form=form, legend='New Post')


@posts.route("/post_<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/update_post_<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        db.session.commit()
        flash('The Post was successfully updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        if post.image_file:
            image_file = url_for('static', filename='posts_pics/' +
                                                post.image_file)  # получение объекта фото
        else:
            image_file = ''
    return render_template('create_post.html', title='Post Updating', image_file=image_file,
                           form=form, legend='Post Updating')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The Post was deleted!', 'success')
    return redirect(url_for('posts.allpost'))

