"""
Configurable Cache Memory Simulator

Command-line tool that simulates direct-mapped and N-way set-associative
caches using hexadecimal memory address traces.
"""

import argparse
import sys

from cache import CacheSimulator
from constants import (
    DEFAULT_BLOCK_SIZE,
    DEFAULT_CACHE_SIZE,
    DEFAULT_WAYS,
    DIRECT_MAPPED_WAYS,
    EXIT_ERROR,
    EXIT_SUCCESS,
    HIT_RATE_DECIMALS,
)
from input_reader import read_trace_file


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Simulate a direct-mapped or N-way set-associative cache "
            "using a hexadecimal memory address trace."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--trace",
        "-t",
        required=True,
        help="Path to a text file with one hexadecimal address per line.",
    )
    parser.add_argument(
        "--cache-size",
        "-c",
        type=int,
        default=DEFAULT_CACHE_SIZE,
        help="Total cache size in bytes (must be a power of 2).",
    )
    parser.add_argument(
        "--block-size",
        "-b",
        type=int,
        default=DEFAULT_BLOCK_SIZE,
        help="Block (line) size in bytes (must be a power of 2).",
    )
    parser.add_argument(
        "--ways",
        "-w",
        type=int,
        default=DEFAULT_WAYS,
        help=(
            f"Associativity. {DIRECT_MAPPED_WAYS} = direct-mapped; "
            "greater than 1 = N-way set-associative with LRU."
        ),
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print tag, index, and offset for each address access.",
    )
    return parser


def print_results(stats):
    """Print configuration and hit/miss statistics."""
    print()
    print("=" * 50)
    print("  CACHE MEMORY SIMULATOR RESULTS")
    print("=" * 50)
    print(f"  Mapping policy : {stats['mapping_policy']}")
    print(f"  Cache size     : {stats['cache_size']} bytes")
    print(f"  Block size     : {stats['block_size']} bytes")
    print(f"  Ways           : {stats['ways']}")
    print(f"  Number of sets : {stats['num_sets']}")
    print(f"  Offset bits    : {stats['offset_bits']}")
    print(f"  Index bits     : {stats['index_bits']}")
    print("-" * 50)
    print(f"  Total accesses : {stats['total_accesses']}")
    print(f"  Hits           : {stats['hits']}")
    print(f"  Misses         : {stats['misses']}")
    print(f"  Hit rate       : {stats['hit_rate']:.{HIT_RATE_DECIMALS}f}%")
    print("=" * 50)
    print()


def run_verbose(simulator, addresses):
    """Simulate each access and print decoded fields."""
    print()
    print(
        f"{'Address':<12} {'Tag':<10} {'Index':<8} {'Offset':<8} {'Result'}"
    )
    print("-" * 50)
    for address in addresses:
        tag, index, offset = simulator.decoder.decode(address)
        is_hit = simulator.access(address)
        result = "HIT" if is_hit else "MISS"
        print(
            f"0x{address:08X}   "
            f"{tag:<10} {index:<8} {offset:<8} {result}"
        )
    return simulator.get_statistics()


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        addresses = read_trace_file(args.trace)
        simulator = CacheSimulator(args.cache_size, args.block_size, args.ways)

        if args.verbose:
            stats = run_verbose(simulator, addresses)
        else:
            stats = simulator.run(addresses)

        print_results(stats)
        return EXIT_SUCCESS

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
