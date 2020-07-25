from __future__ import annotations

import asyncio
import logging

import websockets

from server import config, close_window_request_event, shutdown_event

LOGGER = logging.getLogger(__name__)


async def _listen(websocket, path):
    message = await websocket.recv()
    LOGGER.debug(f"<<<< MSG_RECV: {message}")
    try:
        ipc_resolvers[message]()
    except Exception as e:
        LOGGER.error(f"Failed to process IPC Instruction ${message}", e)


async def get_server():
    return await websockets.server.serve(
        _listen,
        config.get("qt", "ipc_ws_bind_address"),
        config.getint("qt", "ipc_ws_port"),
        origins=None,
    )


def start_listener():
    LOGGER.info("Starting IPC Listener Thread")
    _el.run_until_complete(server)
    _el.run_forever()


_el = asyncio.get_event_loop()

ipc_resolvers = {
    "CLOSE": lambda: close_window_request_event.on_next(True)
}

server = get_server()
shutdown_event.subscribe(lambda e: server.close())
