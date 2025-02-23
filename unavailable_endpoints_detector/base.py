
from dataclasses import dataclass
from typing import Set

@dataclass
class EngineStats:
    # Number of running requests
    num_running_requests: int = 0


class BaseUnavailableEndpointsDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def detect(self, endpoints_to_status: Dict[str, EndpointStatus]) -> Set[str]:
        pass
