from flask import Blueprint, render_template


frontend_app = Blueprint('frontend', __name__,
                         template_folder='templates')


@frontend_app.route('/')
def home():
    return  render_template('home.html',
                            data={'given_name': 'currently in home'})

