"""Split memory addresses into tag, index, and block offset fields."""

import math

from constants import MIN_BLOCK_SIZE, MIN_CACHE_SIZE, MIN_WAYS


class AddressDecoder:
    """Decode a memory address into tag, index, and offset using bitwise ops."""

    def __init__(self, cache_size, block_size, ways):
        self._validate_config(cache_size, block_size, ways)

        self.cache_size = cache_size
        self.block_size = block_size
        self.ways = ways
        self.num_sets = cache_size // (block_size * ways)

        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_sets)) if self.num_sets > 1 else 0
        self.tag_shift = self.offset_bits + self.index_bits

        self.offset_mask = (1 << self.offset_bits) - 1
        self.index_mask = (1 << self.index_bits) - 1 if self.index_bits > 0 else 0

    @staticmethod
    def _is_power_of_two(value):
        return value > 0 and (value & (value - 1)) == 0

    def _validate_config(self, cache_size, block_size, ways):
        if cache_size < MIN_CACHE_SIZE:
            raise ValueError(f"Cache size must be at least {MIN_CACHE_SIZE} byte(s).")
        if block_size < MIN_BLOCK_SIZE:
            raise ValueError(f"Block size must be at least {MIN_BLOCK_SIZE} byte(s).")
        if ways < MIN_WAYS:
            raise ValueError(f"Number of ways must be at least {MIN_WAYS}.")
        if not self._is_power_of_two(cache_size):
            raise ValueError("Cache size must be a power of 2.")
        if not self._is_power_of_two(block_size):
            raise ValueError("Block size must be a power of 2.")
        if cache_size % (block_size * ways) != 0:
            raise ValueError(
                "Cache size must be divisible by (block size × number of ways)."
            )
        num_sets = cache_size // (block_size * ways)
        if num_sets < 1:
            raise ValueError("Configuration produces zero cache sets.")
        if not self._is_power_of_two(num_sets):
            raise ValueError(
                "Number of sets must be a power of 2 "
                "(check cache size, block size, and ways)."
            )

    def decode(self, address):
        """Return (tag, index, offset) for the given integer address."""
        offset = address & self.offset_mask
        index = (address >> self.offset_bits) & self.index_mask
        tag = address >> self.tag_shift
        return tag, index, offset

    def describe(self):
        """Return a human-readable summary of the bit layout."""
        return {
            "cache_size": self.cache_size,
            "block_size": self.block_size,
            "ways": self.ways,
            "num_sets": self.num_sets,
            "offset_bits": self.offset_bits,
            "index_bits": self.index_bits,
            "tag_shift": self.tag_shift,
        }
