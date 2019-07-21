from celery import Celery
from .. import connectivity

celery_async = Celery('async_tasks', backend='redis://localhost', broker='redis://localhost')

@celery_async.task
def add(x, y):
    print('workek started')
    return x + y

@celery_async.task
def price_by_pricing_id(pricing_id):
    print(f'pricing id: {pricing_id}')
    import random
    import time
    import json
    trades = connectivity.get_trades_by_pricing_id(pricing_id)
    random.shuffle(trades)
    publish = connectivity.get_pricing_room_publish_function(pricing_id)
    for trade in trades:
        time.sleep(0.2)
        print(trade)
        price_update = {'trade_no': trade, 'price': random.randint(100, 1000)}
        publish(message=json.dumps(price_update))

    publish(message='FINISHED')

