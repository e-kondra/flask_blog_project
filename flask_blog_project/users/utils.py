import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message  # класс-конструктор для создания объекта сообщения
from flask_blog_project import mail


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    """отправка сообщения со ссылкой о сбросе пароля"""
    token = user.get_reset_token()  # Запрашиваем токен, который по сути является той самой электронной подписью,
                                    # которая гарантирует безопасность доставки письма.
    message = Message('Запрос на сброс пароля', sender='ramlir5201@yandex.ru', recipients=[user.email])
    message.body = f'''Чтобы сбросить пароль перейдите по следующей ссылкой 
                    {url_for('users.reset_token', token=token, _external=True)}. 
                    Если же Вы не делали этот запрос - просто проигнорируйте это письмо'''
    mail.send(message)
