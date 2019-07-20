from flask import Blueprint, render_template


frontend_app = Blueprint('frontend', __name__,
                         template_folder='templates')


@frontend_app.route('/')
def home():
    return  render_template('home.html',
                            data={'given_name': 'currently in home'})

@frontend_app.route('/trade_list')
def list_trades():
    trades = {'13413134': {'typology': 'spot', 'price': 400},
              '92314124': {'typology': 'outright', 'price': 3000}}
    return render_template('list_trades.html', trades=trades)