from celery import Celery
from .. import connectivity
import json
import random
import time
celery_async = Celery('async_tasks', backend='redis://localhost', broker='redis://localhost')


@celery_async.task
def send_single_price(trade, pricing_id):
    publish = connectivity.get_pricing_room_publish_function(pricing_id)
    price_update = {'trade_no': trade, 'price': random.randint(100, 1000)}
    # time.sleep(random.random() * 1.5)
    publish(message=json.dumps(price_update))
    # return price_update


@celery_async.task
def price_by_pricing_id(pricing_id):
    print(f'pricing id: {pricing_id}')
    trades = connectivity.get_trades_by_pricing_id(pricing_id)
    publish = connectivity.get_pricing_room_publish_function(pricing_id)
    random.shuffle(trades)
    time.sleep(2)
    tasks = []
    price_count = 5000
    for _ in range(price_count):
        for trade in trades:
            result = send_single_price.delay(trade, pricing_id)
            tasks.append(result)


    publish(message=str(len(trades) * price_count))



