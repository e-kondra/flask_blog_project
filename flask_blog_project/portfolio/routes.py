from flask import render_template, Blueprint

portfolio = Blueprint('portfolio', __name__)


@portfolio.route("/portfolio")
def portfolio_main():
    return render_template('portfolio.html')