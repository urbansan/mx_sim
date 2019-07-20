import asyncio
import websockets
import random
import json
import os
from dotenv import load_dotenv
from ..connectivity import get_trades_by_pricing_id


dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, '..', '.flaskenv')
load_dotenv(dotenv_path=dotenv_path)


async def new_conn(ws, path):
    print('>> log >>', ws, path)
    pricing_id = path.strip('/')
    trades = get_trades_by_pricing_id(pricing_id)

    while True:
        await asyncio.sleep(1)
        trade = random.choice(trades).decode("utf-8")
        print(trade)
        price_update = {'trade_no': trade, 'price': random.randint(100, 1000)}
        to_json = json.dumps(price_update)
        try:
            hadouken = await ws.send(to_json)
            print(hadouken)
        except websockets.exceptions.ConnectionClosedOK:
            pass  #TODO: possible cleanup

def hadouken():
    print('Starting pricing server...')

    host = os.environ['WEBSOCKET_HOST']
    port = os.environ['WEBSOCKET_PORT']
    global new_conn
    server = websockets.serve(new_conn, host, port)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    hadouken()
