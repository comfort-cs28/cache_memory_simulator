"""Shared constants for the cache memory simulator."""

# Default cache configuration (bytes / ways)
DEFAULT_CACHE_SIZE = 1024
DEFAULT_BLOCK_SIZE = 16
DEFAULT_WAYS = 1

# Direct-mapped cache uses a single way per set
DIRECT_MAPPED_WAYS = 1

# Minimum valid values
MIN_CACHE_SIZE = 1
MIN_BLOCK_SIZE = 1
MIN_WAYS = 1

# Address parsing
HEX_PREFIX = "0x"
HEX_BASE = 16

# Statistics display
PERCENT_SCALE = 100.0
HIT_RATE_DECIMALS = 2

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
