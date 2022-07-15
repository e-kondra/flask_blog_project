from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog_project import db, bcrypt
from flask_blog_project.models import User, Post
from flask_blog_project.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,
                                            ResetPasswordForm)
from flask_blog_project.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt. \
            generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.allpost'))

        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account was changed!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=
                                    form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
        image_file = url_for('static', filename='profile_pics/' +
                                            current_user.image_file)  # получение объекта фото
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, posts=posts,
                           user=user)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """сброс пароля"""
    if current_user.is_authenticated:
        return redirect(url_for('posts.allposts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)  # отправка письмо с инструкциями
        flash(' Instructions for password reset has been sent to your email address', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Сброс пароля', form=form)


@users.route("/reset_password_<token>", methods=['GET', 'POST'])
def reset_token(token):
    """ контроллер для изменения пароля"""
    if current_user.is_authenticated:
        return redirect(url_for('posts.allposts'))
    user = User.verify_reset_token(token)  # десериализация ключа
    if user is None:
        flash('This is invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Получаем пароль из формы и выполняем его хеширование,
        user.password = hashed_password  # Вносим изменения в бд
        db.session.commit()
        flash('The password was renewed! Noe you can login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='reset password', form=form)
