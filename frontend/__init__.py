from flask import Blueprint, render_template, session
import os
from .. import connectivity
from datetime import datetime as dt, timedelta as td

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

    calc = session.get('current_calculation')
    if calc and calc['expiry'] > dt.now():  # expiry has not been reached
        pricing_id = calc['pricing_id']
        connectivity.continue_pricing(pricing_id, trades)
    else:
        pricing_id = connectivity.price_batch_of_trades(trades)
        session['current_calculation'] = {'expiry': dt.now() + td(minutes=5),
                                          'pricing_id': pricing_id}

    return render_template('list_trades.html',
                           trades=trades,
                           websocket_address=websocket_address,
                           uuid=pricing_id)
#
# @frontend_app.route('/presist')
# def persist():
#     session.