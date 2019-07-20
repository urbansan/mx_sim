import asyncio
import websockets
import random
import json

trades =['13413134', '92314124']

print('pushing_trades')

async def new_conn(ws, path):
    print('>> log >>', ws, path)
    while True:
        await asyncio.sleep(1)
        trade = random.choice(trades)
        price_update = {'trade_no': trade, 'price': random.randint(100, 1000)}
        to_json = json.dumps(price_update)
        await ws.send(to_json)





server = websockets.serve(new_conn, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
