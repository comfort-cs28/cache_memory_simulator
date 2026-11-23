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

# Access results
RESULT_HIT = "HIT"
RESULT_MISS = "MISS"

# Statistics display
PERCENT_SCALE = 100.0
HIT_RATE_DECIMALS = 2

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

# GUI theme (navy + gold academic look)
GUI_COLOR_NAVY = "#0B1F3A"
GUI_COLOR_NAVY_MID = "#143D66"
GUI_COLOR_GOLD = "#C4A35A"
GUI_COLOR_CREAM = "#F7F4EF"
GUI_COLOR_WHITE = "#FFFFFF"
GUI_COLOR_MUTED = "#4A5568"
GUI_COLOR_HIT = "#1B7F4E"
GUI_COLOR_MISS = "#B33A3A"
GUI_COLOR_BORDER = "#D8D2C8"

GUI_WINDOW_TITLE = "Cache Memory Simulator"
GUI_WINDOW_WIDTH = 1100
GUI_WINDOW_HEIGHT = 720
GUI_MIN_WIDTH = 900
GUI_MIN_HEIGHT = 600

GUI_FONT_TITLE = ("Georgia", 20, "bold")
GUI_FONT_HEADING = ("Georgia", 12, "bold")
GUI_FONT_BODY = ("Calibri", 11)
GUI_FONT_BODY_BOLD = ("Calibri", 11, "bold")
GUI_FONT_MONO = ("Consolas", 10)
GUI_FONT_STAT_VALUE = ("Calibri", 18, "bold")
GUI_FONT_STAT_LABEL = ("Calibri", 10)

GUI_CURSOR_POINTER = "hand2"

# Common ways choices shown in the GUI dropdown
GUI_WAYS_OPTIONS = (1, 2, 4, 8, 16)

# Sample traces folder / default demo file
TRACES_FOLDER_NAME = "traces"
DEFAULT_TRACE_FILE_NAME = "hand_verified.txt"
