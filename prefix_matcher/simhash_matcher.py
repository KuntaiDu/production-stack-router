import xxhash
from simhash import Simhash
from uhashring import HashRing
import abc
import enum
import random
from functools import partial
from dataclasses import dataclass
from typing import Set, Callable
from collections import defaultdict, Counter

from .base import BasePrefixMatcher

class HashType(str, enum.Enum):
    XXHASH = "xxhash"
    SIMHASH = "simhash"

    def get_hash_func(self, max_length: int | None = None) -> Callable[[str], int]:
        def trim_and_hash(hash_func: Callable[[str], int], text: str) -> int:
            if max_length is not None:
                text = text[:max_length]
            return hash_func(text)

        base_funcs = {
            HashType.XXHASH: xxhash.xxh64_intdigest,
            HashType.SIMHASH: lambda text: Simhash(text).value
        }

        return partial(trim_and_hash, base_funcs[self])

        
class SimhashMatcher(BasePrefixMatcher):
    def __init__(
        self,
        hash_type: HashType = HashType.SIMHASH,  # The hash function to use for hashing the request
        max_length: int = 512,  # The maximum length of the request to hash
    ):
        self.hash_ring = HashRing()
        self.hash_func = hash_type.get_hash_func(max_length=max_length)
        self.endpoints = set()


    def match(
        self,
        text: str,
        unavailable_endpoints: Set[str],
    ) -> str:

        assert unavailable_endpoints.issubset(self.endpoints)

        hash_value = self.hash_func(text)

        # Iterate through nodes starting from the hash position
        for endpoint in self.hash_ring.iterate_nodes(str(hash_value), distinct=True):

            if endpoint not in unavailable_endpoints:
                return endpoint

        raise ValueError(f"No endpoint found for text: {text}")

    def routed(self, text: str, endpoint: str) -> None:
        # In simhash matcher the endpoint state is irrelevant to which request
        # is routed to which endpoint.
        pass

    def add_endpoints(self, endpoints: Set[str]) -> None:

        assert endpoints.isdisjoint(self.endpoints)

        # Add new nodes that are not already in the hash ring
        for endpoint in endpoints:
            self.hash_ring.add_node(endpoint)

        self.endpoints.update(endpoints)

    def remove_endpoints(self, endpoints: Set[str]) -> None:

        assert endpoints.issubset(self.endpoints)

        # Remove nodes that are no longer in the list
        for node in endpoints:
            self.hash_ring.remove_node(node)

        self.endpoints.difference_update(endpoints)
