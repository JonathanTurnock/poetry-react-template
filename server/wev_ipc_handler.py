from __future__ import annotations
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Callable

import dacite
import jsonpickle
import websockets
from PySide2.QtCore import QThread

from server import config, close_window_request_event

LOGGER = logging.getLogger(__name__)

ipc_resolvers: Dict[str, Callable[[Any], any]] = {
    "closeApp": lambda **kwargs: close_window_request_event.on_next(True)
}


@dataclass
class IpcRq:
    action: str
    params: dict

    @staticmethod
    def of(dict_object) -> IpcRq:
        return dacite.from_dict(data_class=IpcRq, data=dict_object)


class IpcResponseStatus(Enum):
    OK = 0
    ERROR = 1


@dataclass
class IpcRs:
    response: IpcResponseStatus
    data: dict = None
    error: str = None

    def __str__(self) -> str:
        resp = {
            "response": str(self.response.name),
        }

        if self.data is not None:
            resp["data"] = jsonpickle.encode(self.data, unpicklable=False)

        if self.error is not None:
            resp["error"] = self.error

        return json.dumps(resp)

    @staticmethod
    def of(dict_object) -> IpcRs:
        return dacite.from_dict(data_class=IpcRs, data=dict_object)


class IpcHandler(QThread):
    def __init__(self, event_loop):
        super(IpcHandler, self).__init__()
        self.event_loop = event_loop
        self._shutdown = False

    def run(self):
        LOGGER.info("Starting IPC Handler Thread")
        self.event_loop.run_until_complete(start_server)
        self.event_loop.run_forever()
        LOGGER.info("WebEngineView Closed, Shutting Down IPC Handler...")

    @staticmethod
    async def handle(websocket, path):
        message = await websocket.recv()
        LOGGER.debug(f"<<<< MSG_RECV: {message}")

        try:
            ipc_rq = IpcRq.of(json.loads(message))
            try:
                ipc_rs = IpcRs(
                    response=IpcResponseStatus.OK,
                    data=ipc_resolvers[ipc_rq.action](**ipc_rq.params),
                )
            except Exception as e:
                ipc_rs = IpcRs(
                    response=IpcResponseStatus.ERROR,
                    error=f"Resolving IpcRq failed due to {e}",
                    data={},
                )
        except Exception as e:
            ipc_rs = IpcRs(
                response=IpcResponseStatus.ERROR,
                error=f"Failed to parse IpcRq due to {e}",
                data={},
            )

        LOGGER.debug(f">>>> MSG_SEND: {ipc_rs}")
        await websocket.send(str(ipc_rs))


start_server = websockets.serve(
    IpcHandler.handle,
    config.get("qt", "ipc_ws_bind_address"),
    config.getint("qt", "ipc_ws_port"),
    origins=None,
)
