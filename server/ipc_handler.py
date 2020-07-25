from __future__ import annotations

import asyncio
import logging

import websockets
from rx.subject import Subject

from server import config

LOGGER = logging.getLogger(__name__)

ipc_shutdown_event = Subject()


async def _listen(websocket, path):
    async for message in websocket:
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
    _el.run_until_complete(ipc_server)
    _el.run_forever()


_el = asyncio.get_event_loop()

ipc_resolvers = {"closeApplication": lambda: ipc_shutdown_event.on_next(True)}

ipc_server = get_server()
