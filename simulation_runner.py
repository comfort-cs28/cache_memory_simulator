"""Shared simulation helpers used by the CLI and GUI."""

from cache import CacheSimulator
from constants import RESULT_HIT, RESULT_MISS


def run_simulation(cache_size, block_size, ways, addresses):
    """
    Run a full trace and return (statistics_dict, access_log_list).

    Each access_log entry has: address, tag, index, offset, result, is_hit.
    """
    simulator = CacheSimulator(cache_size, block_size, ways)
    access_log = []

    for address in addresses:
        tag, index, offset = simulator.decoder.decode(address)
        is_hit = simulator.access(address)
        access_log.append(
            {
                "address": address,
                "tag": tag,
                "index": index,
                "offset": offset,
                "is_hit": is_hit,
                "result": RESULT_HIT if is_hit else RESULT_MISS,
            }
        )

    return simulator.get_statistics(), access_log
