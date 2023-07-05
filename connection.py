
import websockets.sync.client as ws
import websockets.sync.server as wss

import config


def connect_to_server(update):
    addr, port = config.HOST_ADDR
    with ws.connect(f"ws://{addr}:{port}") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv_messages()
