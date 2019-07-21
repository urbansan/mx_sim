import asyncio
import websockets
import random
import json
import os
from dotenv import load_dotenv
from .. import connectivity


dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, '..', '.flaskenv')
load_dotenv(dotenv_path=dotenv_path)


async def new_connection(ws, path):
    print('>> log >>', ws, path)
    pricing_id = path.strip('/')


    # while True:
    room_listener = connectivity.get_pricing_room_listener(pricing_id)
    for message in room_listener.listen():
        if message['type'] == 'message':
            print(message)
            if message['data'] == 'FINISHED':
                # await ws.close()
                break
                # raise websockets.exceptions.ConnectionClosedOK(1001, 'pricing finished')

            try:
                await ws.send(message['data'])
            except websockets.exceptions.ConnectionClosedOK:
                pass  #TODO: possible cleanup
    print('end y\'all')


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
