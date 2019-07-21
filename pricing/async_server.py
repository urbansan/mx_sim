import asyncio
import websockets
import random
import json
import os
from dotenv import load_dotenv
from .. import connectivity
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor


dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, '..', '.flaskenv')
load_dotenv(dotenv_path=dotenv_path)


async def new_connection(ws, path):
    print('>> log >>', ws, path)
    pricing_id = path.strip('/')
    start = dt.now()
    # while True:
    room_listener = connectivity.get_pricing_room_listener(pricing_id)
    countdown = 0
    countup = float('inf')
    while True:
        message = room_listener.get_message()
        # print(message)
        if message and message['type'] == 'message':

            try:
                countup = int(message['data'])
            except (AttributeError, ValueError):
                countdown += 1

            try:
                await ws.send(message['data'])
            except websockets.exceptions.ConnectionClosedOK:
                pass  #TODO: possible cleanup
        else:

            print(f'countup: {countup}, countdown: {countdown}')
            if countup - countdown < 1:
                break
            await asyncio.sleep(0.3)

    print(f'end y\'all: {dt.now() - start}')


def run_server():
    print('Starting pricing server...')

    host = os.environ['WEBSOCKET_HOST']
    port = os.environ['WEBSOCKET_PORT']
    global new_connection
    server = websockets.serve(new_connection, host, port)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    run_server()
