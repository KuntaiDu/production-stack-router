"""
    Abstract class for prefix matchers.
"""

import abc
from typing import Set

class BasePrefixMatcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def match(self, text: str, unavailable_endpoints: Set[str] = set()) -> str:
        """
        Match the request to the endpoint (best-effort match).

        Args:
            text (str): The request to match.
            unavailable_endpoints (Set[str]): The endpoints that are temporarily unavailable.

        Returns:
            str: The endpoint that best matches the request.
        """
        pass

    @abc.abstractmethod
    def update(self, text: str, endpoint: str) -> None:
        """
        Notify the matcher that the text is actually routed to the endpoint.

        Args:
            text (str): The request.
            endpoint (str): The endpoint that is actually routed to.
        """

    @abc.abstractmethod
    def add_endpoints(self, endpoints: Set[str]) -> None:
        """
        Add new endpoints to the matcher.

        Args:
            endpoints (Set[str]): The endpoints to add.
        """
        pass

    @abc.abstractmethod
    def remove_endpoints(self, endpoints: Set[str]) -> None:
        """
        Remove endpoints from the matcher.

        Args:
            endpoints (Set[str]): The endpoints to remove.
        """
        pass
