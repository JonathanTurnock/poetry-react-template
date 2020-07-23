from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    OK = 0
    DOWN = 1


@dataclass
class Health:
    status: Status
    detail: dict

    @classmethod
    def up(cls) -> Health:
        """
        :return: Health status of OK
        """
        return Health(Status.OK, {})

    @classmethod
    def down(cls, detail: dict = None) -> Health:
        """
        :param detail: Detailed cause of the status being down in dictionary format
        :return: Health Status od DOWN with given Detail
        """
        return Health(Status.DOWN, detail if detail is not None else {})


def get_app_health() -> Health:
    try:
        return Health.up()
    except Exception as e:
        return Health.down({"error": str(e)})
