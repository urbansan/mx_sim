from flask import Blueprint, render_template
import os
from .. import connectivity


host = os.environ['WEBSOCKET_HOST']
port = os.environ['WEBSOCKET_PORT']
websocket_address =  f'{host}:{port}'


frontend_app = Blueprint('frontend', __name__,
                         template_folder='templates')


@frontend_app.route('/')
def home():
    return  render_template('home.html',
                            data={'given_name': 'currently in home'})

@frontend_app.route('/trade_list')
def list_trades():
    trades = connectivity.get_trades_for('uci', 'live')
    pricing_id = connectivity.price_batch_of_trades(trades)
    return render_template('list_trades.html',
                           trades=trades,
                           websocket_address=websocket_address,
                           uuid=pricing_id)