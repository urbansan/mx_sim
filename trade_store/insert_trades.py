import redis
from ..common.enums import Databases
from ..common.trade import Trade

print(Databases.TRADES.value)
redis_conn = redis.Redis(db=Databases.TRADES.value)

trade_list = [
    Trade('spot', 10320, 10210),
    Trade('outright', 100, 1020),
    Trade('spot', 1010, 10540),
    Trade('irs', 3230, 10650),
    Trade('cf', 1120, 10760),
    Trade('xccy', 123, 14500),
    Trade('cf piecewise', 999, 100),
]

for trade in trade_list:
    redis_conn.hset('uci:live', str(trade.number), trade.serialize())