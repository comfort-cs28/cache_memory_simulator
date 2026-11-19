"""Read and validate hexadecimal memory addresses from a trace file."""

from constants import HEX_BASE, HEX_PREFIX


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


def read_trace_file(file_path):
    """
    Read a text file with one hexadecimal address per line.

    Blank lines and lines starting with '#' are ignored.
    Returns a list of integer addresses.
    """
    addresses = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as trace_file:
            for line_number, raw_line in enumerate(trace_file, start=1):
                address = parse_hex_address(raw_line, line_number)
                if address is not None:
                    addresses.append(address)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Trace file not found: {file_path}") from exc
    except OSError as exc:
        raise OSError(f"Could not read trace file '{file_path}': {exc}") from exc

    if not addresses:
        raise ValueError(f"Trace file '{file_path}' contains no valid addresses.")

    return addresses
