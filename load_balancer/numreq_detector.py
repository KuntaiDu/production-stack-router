
from typing import Set, Dict
from .base import EndpointStatus, BaseLoadBalancer

class NumReqLoadBalancer(BaseLoadBalancer):

    def __init__(self, num_running_requests_threshold: int = 100):
        self.num_running_requests_threshold = num_running_requests_threshold

    def get_unavailable_endpoints(self, endpoints_to_status: Dict[str, EndpointStatus]) -> Set[str]:

        unavailable_endpoints = set()
        
        for endpoint in endpoints_to_status:
            if endpoints_to_status[endpoint].num_running_requests > self.num_running_requests_threshold:
                unavailable_endpoints.add(endpoint)

        return unavailable_endpoints
