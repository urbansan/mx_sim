import redis
from .common.enums import Databases
from .common.base import deserialize
from .mq import async_tasks

redis_default_options = {
    'decode_responses': True
}


def get_trades_for(entity, status) -> list:
    r = redis.Redis(db=Databases.TRADES.value)
    key = f'{entity}:{status}'
    data = [deserialize(value) for value in r.hgetall(key).values()]
    return data


def price_batch_of_trades(trades):
    from uuid import uuid4

    r = redis.Redis(db=Databases.PRICING.value, **redis_default_options)
    pricing_id = str(uuid4())

    trade_numbers = [trade.number for trade in trades]
    r.lpush(pricing_id, *trade_numbers)

    async_tasks.price_by_pricing_id.delay(pricing_id)

    return pricing_id

def get_trades_by_pricing_id(pricing_id):
    r = redis.Redis(db=Databases.PRICING.value, **redis_default_options)
    trades = r.lrange(pricing_id, 0, -1)
    return trades

def get_pricing_room_listener(pricing_id):
    r = redis.Redis(db=Databases.PRICING.value, **redis_default_options)
    subscriber = r.pubsub()
    subscriber.subscribe([pricing_id])
    return subscriber

def get_pricing_room_publish_function(pricing_id):
    r = redis.Redis(db=Databases.PRICING.value, **redis_default_options)
    p = r.pubsub()
    from functools import partial
    publish = partial(r.publish, channel=pricing_id)
    return publish
