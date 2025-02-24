"""
    Abstract class for prefix matchers.
    It implements four methods:
    1. match(text: str, unavailable_endpoints: Set[str]) -> str
        -- It returns one endpoint in endpoints that best matches the text.
    2. update(text: str, endpoint: str) -> None
        -- It updates the matcher state by telling it that the given text is
           routed to the given endpoint.
    3. add_endpoints(endpoints: Set[str]) -> None
        -- It adds new endpoints to the matcher.
    4. remove_endpoints(endpoints: Set[str]) -> None
        -- It removes endpoints from the matcher.
"""

import abc
from typing import Set

class BasePrefixMatcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def match(self, text: str, unavailable_endpoints: Set[str] = set()) -> str:
        pass

    @abc.abstractmethod
    def update(self, text: str, endpoint: str) -> None:
        pass

    @abc.abstractmethod
    def add_endpoints(self, endpoints: Set[str]) -> None:
        pass

    @abc.abstractmethod
    def remove_endpoints(self, endpoints: Set[str]) -> None:
        pass
