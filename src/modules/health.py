import time
from threading import Thread
from modules.logger import logger
from modules.settings import settings
from typing import Union


class Health():
    """Singleton class.
    Instance of this class represents application health.
    If time since last heartbeat reach heartbeat_timeout (seconds),
    instance will die (not destroy).
    """
    _instance = None

    def __new__(cls, *args: Union[int, float], **kwargs: Union[int, float]) -> "Health":
        if not isinstance(cls._instance, cls):
            cls._instance = super(Health, cls).__new__(cls)
        return cls._instance

    def __init__(self, heartbeat_timeot: Union[int, float] = 60) -> None:
        self.life = Thread(target=self._start_heart)
        self._heartbeat_timeout = heartbeat_timeot
        self.life.start()
        logger.info("Health initialized")

    @property
    def alive(self) -> bool:
        return self.life.is_alive()

    def heartbeat(self) -> None:
        logger.debug("Heartbeat: BUM")
        self._last_hearbeat = time.time()

    def _start_heart(self) -> None:
        self._last_hearbeat = time.time()
        while True:
            if time.time() - self._last_hearbeat > self._heartbeat_timeout:
                break
            time.sleep(0.01)
        logger.error("Heart didn't beat. Dying")


health = Health(settings.heartbeat_timeout)
