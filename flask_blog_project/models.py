from datetime import datetime
from flask_blog_project import db, login_manager
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import jwt
from datetime import datetime, timezone, timedelta


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # указание на посты, кот. есть у автора

    def __repr__(self):
        return f"Пользователь('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        payload = {'user_id': self.id, 'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_sec)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token, leeway=10):
        """десериализация ключа"""
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=['HS256'])
        except Exception:
            return None
        return User.query.get(data['user_id'])

    # две следующие функции работают с itsdangerous версии 1.1.0
    # def get_reset_token(self, expires_sec=1800):
    #     # s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     # return s.dumps({'user_id': self.id}).decode('utf-8')
    # @staticmethod
    # def verify_reset_token(token, leeway=10):
    #     """десериализация ключа"""
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except Exception:
    #         return None
    #     return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}', '{self.image_file}')"


