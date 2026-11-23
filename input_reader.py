"""Read and validate hexadecimal memory addresses from a trace file."""

import os

from constants import HEX_BASE, HEX_PREFIX, TRACES_FOLDER_NAME

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def parse_hex_address(raw_line, line_number):
    """Parse one line into an integer address, or raise ValueError."""
    line = raw_line.strip().lstrip("\ufeff")
    if not line or line.startswith("#"):
        return None

    text = line.lower()
    if text.startswith(HEX_PREFIX):
        text = text[len(HEX_PREFIX) :]

    if not text:
        raise ValueError(f"Line {line_number}: empty address after '0x'.")

    try:
        return int(text, HEX_BASE)
    except ValueError as exc:
        raise ValueError(
            f"Line {line_number}: invalid hexadecimal address '{line}'."
        ) from exc


def resolve_trace_path(file_path):
    """
    Resolve a trace path against the current folder or the project folder.

    Accepts absolute paths, paths like traces/hand_verified.txt, or just
    a filename such as hand_verified.txt inside the traces folder.
    """
    if not file_path or not str(file_path).strip():
        raise FileNotFoundError("No trace file path was provided.")

    raw_path = str(file_path).strip().strip('"').strip("'")
    candidates = [
        raw_path,
        os.path.abspath(raw_path),
        os.path.join(PROJECT_ROOT, raw_path),
        os.path.join(PROJECT_ROOT, TRACES_FOLDER_NAME, os.path.basename(raw_path)),
    ]

    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

    traces_dir = os.path.join(PROJECT_ROOT, TRACES_FOLDER_NAME)
    raise FileNotFoundError(
        f"Trace file not found: {raw_path}\n"
        f"Look in: {traces_dir}\n"
        f"Example: {os.path.join(traces_dir, 'hand_verified.txt')}"
    )


def read_trace_file(file_path):
    """
    Read a text file with one hexadecimal address per line.

    Blank lines and lines starting with '#' are ignored.
    Returns a list of integer addresses.
    """
    resolved_path = resolve_trace_path(file_path)
    addresses = []
    try:
        with open(resolved_path, "r", encoding="utf-8-sig") as trace_file:
            for line_number, raw_line in enumerate(trace_file, start=1):
                address = parse_hex_address(raw_line, line_number)
                if address is not None:
                    addresses.append(address)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Trace file not found: {resolved_path}") from exc
    except OSError as exc:
        raise OSError(f"Could not read trace file '{resolved_path}': {exc}") from exc

    if not addresses:
        raise ValueError(f"Trace file '{resolved_path}' contains no valid addresses.")

    return addresses
