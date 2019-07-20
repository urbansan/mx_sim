import redis
from .common.enums import Databases
from .common.base import deserialize

def get_trades_for(entity, status) -> list:
    r = redis.Redis(db=Databases.TRADES.value)
    key = f'{entity}:{status}'
    data = [deserialize(value) for value in r.hgetall(key).values()]
    return data


def price_batch_of_trades(trades):
    from uuid import uuid4

    r = redis.Redis(db=Databases.PRICING.value)
    pricing_id = str(uuid4())

    trade_numbers = [trade.number for trade in trades]
    r.lpush(pricing_id, *trade_numbers)
    return pricing_id

def get_trades_by_pricing_id(pricing_id):
    r = redis.Redis(db=Databases.PRICING.value)
    trades = r.lrange(pricing_id, 0, -1)
    return trades