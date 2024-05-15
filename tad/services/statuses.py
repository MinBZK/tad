import logging

from tad.core.singleton import Singleton
from tad.repositories.statuses import StatusesRepository

logger = logging.getLogger(__name__)


class StatusesService(metaclass=Singleton):
    __statuses_repository = StatusesRepository()

    def __init__(self):
        logger.info("Statuses service initialized")
        # TODO find out why logging is not visible

    def get_status(self, status_id):
        return self.__statuses_repository.find_by_id(status_id)

    def get_statuses(self) -> []:
        return self.__statuses_repository.find_all()
