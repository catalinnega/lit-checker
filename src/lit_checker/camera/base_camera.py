from typing import Any
from abc import abstractmethod


class BaseCamera:
    def __init__(self, config: Any):
        self.config = config
        self.url = self._get_url(config)
        self.fps = config.fps

    @abstractmethod
    def _get_url(self, config: Any) -> str:
        pass
