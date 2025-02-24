import xxhash

from .base import BasePrefixMatcher
from collections import defaultdict
from typing import Set, Generator
import logging
import random

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class HashTrie:
    def __init__(self, chunk_size: int = 32):
        self.root = TrieNode()
        self.chunk_size = chunk_size

    def _chunk_and_hash(self, word: str) -> Generator[int, None, None]:
        """Generator that yields hashes of 32-character chunks."""
        for i in range(0, len(word), self.chunk_size):
            yield xxhash.xxh64(word[i:i+self.chunk_size]).intdigest()

    def insert(self, word: str) -> None:
        node = self.root
        for chunk_hash in self._chunk_and_hash(word):
            if chunk_hash not in node.children:
                node.children[chunk_hash] = TrieNode()
            node = node.children[chunk_hash]
        node.is_end = True

    def longest_prefix_match(self, word: str) -> int:
        """Finds the longest matching prefix using hashed chunks."""
        node = self.root
        match_length = 0
        chunk_hashes = self._chunk_and_hash(word)

        for i, chunk_hash in enumerate(chunk_hashes):
            if chunk_hash in node.children:
                match_length += self.chunk_size
                node = node.children[chunk_hash]
            else:
                break

        return match_length


class LCPMatcher(BasePrefixMatcher):
    def __init__(self, chunk_size: int = 32):
        self.endpoint_to_trie = {}
        self.chunk_size = chunk_size
        self.logger = logging.getLogger("LCPMatcher")

    def match(self, text: str, unavailable_endpoints: Set[str]) -> str:

        best_endpoints = []
        max_match_length = -1

        assert unavailable_endpoints.issubset(self.endpoint_to_trie.keys())

        # This for loop should be done in parallel.
        for endpoint in self.endpoint_to_trie:
            if endpoint in unavailable_endpoints:
                continue

            match_length = self.endpoint_to_trie[endpoint].longest_prefix_match(text)

            if match_length > max_match_length:
                max_match_length = match_length
                best_endpoints = [endpoint]
            elif match_length == max_match_length:
                best_endpoints.append(endpoint)

        choice = random.choice(best_endpoints)

        self.logger.debug("Match length: %d, best endpoints: %s, choice: %s", max_match_length, best_endpoints, choice)

        return choice

    def update(self, text: str, endpoint: str) -> None:
        self.endpoint_to_trie[endpoint].insert(text)

    def add_endpoints(self, endpoints: Set[str]) -> None:
        for endpoint in endpoints:
            self.endpoint_to_trie[endpoint] = HashTrie(chunk_size=self.chunk_size)

    def remove_endpoints(self, endpoints: Set[str]) -> None:
        for endpoint in endpoints:
            del self.endpoint_to_trie[endpoint]
