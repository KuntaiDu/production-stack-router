
from prefix_matcher.simhash_matcher import SimhashMatcher
from unavailable_endpoints_detector.numreq_detector import NumReqUnavailableEndpointsDetector
from unavailable_endpoints_detector.base import EndpointStatus


class Router:

    def __init__(self, endpoints: Set[str]):
        self.matcher = SimhashMatcher()
        self.unavailable_endpoints_detector = NumReqUnavailableEndpointsDetector()

        self.endpoint_to_status = {endpoint: EndpointStatus(num_running_requests=0) for endpoint in endpoints}

    def route(self, text: str) -> str:

        # This should be done periodically in a separate coroutine. But for the sake of testing let's just do it here.
        unavailable_endpoints = self.unavailable_endpoints_detector.detect(self.endpoints_to_status)

        endpoint = self.matcher.match(text, unavailable_endpoints)

        self.endpoint_to_status[endpoint].num_running_requests += 1

        return endpoint


if __name__ == "__main__":

    prefix = 
