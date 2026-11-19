"""Configurable cache: direct-mapped (ways=1) or N-way set-associative with LRU."""

from collections import OrderedDict

from address_decoder import AddressDecoder
from constants import DIRECT_MAPPED_WAYS


class CacheSimulator:
    """
    Simulate a cache memory.

    ways=1  -> direct-mapped
    ways>1  -> N-way set-associative with LRU replacement
    """

    def __init__(self, cache_size, block_size, ways):
        self.decoder = AddressDecoder(cache_size, block_size, ways)
        self.ways = ways
        self.num_sets = self.decoder.num_sets

        # Each set holds up to `ways` tags, ordered oldest -> newest for LRU
        self.sets = [OrderedDict() for _ in range(self.num_sets)]

        self.hits = 0
        self.misses = 0

    @property
    def total_accesses(self):
        return self.hits + self.misses

    @property
    def mapping_policy(self):
        if self.ways == DIRECT_MAPPED_WAYS:
            return "Direct-Mapped"
        return f"{self.ways}-Way Set-Associative (LRU)"

    def access(self, address):
        """Process one memory read. Returns True on hit, False on miss."""
        tag, index, _offset = self.decoder.decode(address)
        cache_set = self.sets[index]

        if tag in cache_set:
            # Hit: mark this block as most recently used
            cache_set.move_to_end(tag)
            self.hits += 1
            return True

        # Miss: insert new block; evict LRU if the set is full
        self.misses += 1
        if len(cache_set) >= self.ways:
            cache_set.popitem(last=False)
        cache_set[tag] = True
        return False

    def run(self, addresses):
        """Simulate a full address trace. Returns hit/miss statistics."""
        for address in addresses:
            self.access(address)
        return self.get_statistics()

    def get_statistics(self):
        """Return access counters and hit rate percentage."""
        total = self.total_accesses
        hit_rate = (self.hits / total * 100.0) if total > 0 else 0.0
        return {
            "mapping_policy": self.mapping_policy,
            "cache_size": self.decoder.cache_size,
            "block_size": self.decoder.block_size,
            "ways": self.ways,
            "num_sets": self.num_sets,
            "offset_bits": self.decoder.offset_bits,
            "index_bits": self.decoder.index_bits,
            "total_accesses": total,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }
