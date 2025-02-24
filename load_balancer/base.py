
from dataclasses import dataclass
from typing import Set, Dict
import abc

@dataclass
class EndpointStatus:
    # Number of running requests
    num_running_requests: int = 0


class BaseLoadBalancer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_unavailable_endpoints(self, endpoints_to_status: Dict[str, EndpointStatus]) -> Set[str]:
        """
        Get the endpoints that are temporarily unavailable.

        Args:
            endpoints_to_status (Dict[str, EndpointStatus]): The endpoints and their statuses.

        Returns:
            Set[str]: The endpoints that are temporarily unavailable.
        """
        pass
