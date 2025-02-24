
from dataclasses import dataclass
from typing import Set, Dict
import abc

@dataclass
class EndpointStatus:
    # Number of running requests
    num_running_requests: int = 0


class BaseUnavailableEndpointsDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def detect(self, endpoints_to_status: Dict[str, EndpointStatus]) -> Set[str]:
        pass
