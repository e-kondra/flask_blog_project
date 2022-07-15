from flask import render_template, Blueprint
from flask_blog_project.models import User

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/index")
def home():
    return render_template('index.html')
