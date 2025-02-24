import xxhash

from .base import BasePrefixMatcher
from collections import defaultdict
from typing import Set, Generator, Tuple
import logging
import random

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.endpoints = set()

class HashTrie:
    def __init__(self, chunk_size: int = 128):
        """
        Initialize the HashTrie.

        Args:
            chunk_size (int): the string chunk size (in terms of # characters)
        """
        self.root = TrieNode()
        self.chunk_size = chunk_size

    def _chunk_and_hash(self, request: str) -> Generator[int, None, None]:
        """
        Chunk and hash the request.

        Args:
            request (str): The request to chunk and hash.

        Returns:
            Generator[int, None, None]: A generator that yields hashes of 32-character chunks.
        """
        
        for i in range(0, len(request), self.chunk_size):
            yield xxhash.xxh64(request[i:i+self.chunk_size]).intdigest()

    def insert(self, request: str, endpoint: str) -> None:
        """
        Insert the request and endpoint into the trie.

        Args:
            request (str): The request to insert.
            endpoint (str): The endpoint to insert.
        """
        node = self.root
        node.endpoints.add(endpoint)
        for chunk_hash in self._chunk_and_hash(request):
            if chunk_hash not in node.children:
                node.children[chunk_hash] = TrieNode()
            node = node.children[chunk_hash]
            node.endpoints.add(endpoint)
        node.is_end = True

    def longest_prefix_match(self, request: str, unavailable_endpoints: Set[str] = set()) -> Tuple[int, Set[str]]:
        """
        Find the longest matching prefix using hashed chunks.

        Args:
            request (str): The request to find the longest matching prefix.
            unavailable_endpoints (Set[str]): The endpoints that are unavailable.
        """
        node = self.root
        match_length = 0
        chunk_hashes = self._chunk_and_hash(request)
        all_endpoints = self.root.endpoints
        selected_endpoints = self.root.endpoints - unavailable_endpoints

        for i, chunk_hash in enumerate(chunk_hashes):
            if chunk_hash in node.children:
                
                node = node.children[chunk_hash]
                
                # This line will remove the endpoints that are deleted by
                # `remove_endpoints` function call of the router.
                node.endpoints = node.endpoints.intersection(all_endpoints)
                
                # Check if the current node still contains available endpoints.
                if not (node.endpoints - unavailable_endpoints):
                    break
                match_length += self.chunk_size
                selected_endpoints = node.endpoints - unavailable_endpoints
            else:
                break

        return match_length, selected_endpoints


class HashTrieMatcher(BasePrefixMatcher):
    def __init__(self, chunk_size: int = 32):
        """
        Initialize the HashTrieMatcher.

        Args:
            chunk_size (int): the string chunk size (in terms of # characters)
            that is used to calculate the string hash of each chunk.
        """
        self.trie = HashTrie(chunk_size=chunk_size)
        self.chunk_size = chunk_size
        self.logger = logging.getLogger("LCPMatcher")

    def match(self, text: str, unavailable_endpoints: Set[str]) -> str:
        """
        Match the request to the longest matching prefix.

        Args:
            text (str): The request to match.
            unavailable_endpoints (Set[str]): The endpoints that are unavailable.
        """
        assert unavailable_endpoints.issubset(self.trie.root.endpoints)
        
        match_length, selected_endpoints = self.trie.longest_prefix_match(text, unavailable_endpoints)
        
        choice = random.choice(list(selected_endpoints))

        self.logger.debug("Match length: %d, matched endpoints: %s, choice: %s", match_length, selected_endpoints, choice)

        return choice

    def update(self, text: str, endpoint: str) -> None:
        """
        Update the trie with the new request and endpoint.

        Args:
            text (str): The request to update.
            endpoint (str): The endpoint to update.
        """
        self.trie.insert(text, endpoint)

    def add_endpoints(self, endpoints: Set[str]) -> None:
        """
        Add the endpoints to the trie.

        Args:
            endpoints (Set[str]): The endpoints to add.
        """
        self.trie.root.endpoints.update(endpoints)

    def remove_endpoints(self, endpoints: Set[str]) -> None:
        """
        Remove the endpoints from the trie.

        Args:
            endpoints (Set[str]): The endpoints to remove.
        """
        self.trie.root.endpoints.difference_update(endpoints)
