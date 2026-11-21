# Configurable Cache Memory Simulator

A Python tool that simulates **direct-mapped** and **N-way set-associative** caches. It reads hexadecimal memory addresses from a text file, splits each address into tag / index / offset, and reports hits, misses, and hit rate.

Includes both a **command-line interface** and a **graphical user interface (GUI)**.

**Course:** Computer Architecture  
**Members:** Comfort Akorfa Yikpa, Enock Yaw Sie  
**Language:** Python 3 (standard library only)

---

## Features

- Reads hexadecimal addresses from a text file (e.g. `0x1A2B`)
- Decodes tag, index, and block offset with bitwise operations
- Direct-mapped cache (`--ways 1`)
- N-way set-associative cache with **LRU** replacement (`--ways N`)
- Configurable cache size, block size, and number of ways
- Reports total accesses, hits, misses, and hit rate
- **GUI** to browse traces, set options, and view results / access log

---

## Requirements

- Python 3.7 or later
- No third-party packages (uses `argparse`, `math`, `collections`, and `tkinter` only)

---

## Project Structure

```
cache_memory_simulator/
├── main.py                 # CLI + GUI launcher
├── gui_app.py              # Graphical user interface
├── simulation_runner.py    # Shared simulation helper
├── constants.py            # Shared configuration constants
├── address_decoder.py      # Tag / index / offset decoding
├── cache.py                # Cache simulation with LRU
├── input_reader.py         # Trace file loading and validation
├── README.md               # This guide
└── traces/
    ├── sample_addresses.txt
    ├── hand_verified.txt
    └── associativity_demo.txt
```

---

## How to Run

Open a terminal in the project folder.

### Graphical interface (recommended for demos)

```bash
python main.py
```

or:

```bash
python main.py --gui
```

or:

```bash
python gui_app.py
```

In the GUI:

1. Click **Browse** and choose a trace file (start with `traces/sample_addresses.txt`)
2. Set cache size, block size, and ways
3. Click **Run Simulation**
4. Read hit rate / hits / misses and scroll the access log (HIT in green, MISS in red)

### Command-line — direct-mapped (1 way)

```bash
python main.py --trace traces/sample_addresses.txt --cache-size 1024 --block-size 16 --ways 1
```

### Command-line — 4-way set-associative

```bash
python main.py --trace traces/sample_addresses.txt --cache-size 1024 --block-size 16 --ways 4
```

### Verbose mode (show tag, index, offset per access)

```bash
python main.py -t traces/hand_verified.txt -c 64 -b 16 -w 1 --verbose
```

### Short option names

| Option | Short | Meaning |
|--------|-------|---------|
| `--gui` | | Open the graphical interface |
| `--trace` | `-t` | Path to address trace file |
| `--cache-size` | `-c` | Total cache size in bytes |
| `--block-size` | `-b` | Block size in bytes |
| `--ways` | `-w` | Associativity (1 = direct-mapped) |
| `--verbose` | `-v` | Print each access decoded |

---

## Input File Format

One hexadecimal address per line. Lines starting with `#` and blank lines are ignored.

```
0x1A2B
0x00FF
# this is a comment
1A2B
```

Addresses may include or omit the `0x` prefix.

---

## Sample CLI Output

```
==================================================
  CACHE MEMORY SIMULATOR RESULTS
==================================================
  Mapping policy : Direct-Mapped
  Cache size     : 1024 bytes
  Block size     : 16 bytes
  Ways           : 1
  Number of sets : 64
  Offset bits    : 4
  Index bits     : 6
--------------------------------------------------
  Total accesses : 12
  Hits           : 3
  Misses         : 9
  Hit rate       : 25.00%
==================================================
```

Hit rate is calculated as:

```
Hit rate = (Hits / Total accesses) × 100%
```

---

## Comparing Configurations

Use the same trace with different `--ways` values (CLI or GUI) to compare policies:

```bash
python main.py -t traces/associativity_demo.txt -c 64 -b 16 -w 1
python main.py -t traces/associativity_demo.txt -c 64 -b 16 -w 2
python main.py -t traces/associativity_demo.txt -c 64 -b 16 -w 4
```

---

## Configuration Rules

- Cache size and block size must be powers of 2
- Cache size must be divisible by `(block size × ways)`
- Number of sets = `cache size / (block size × ways)` must be a power of 2
- `--ways 1` is direct-mapped; higher values use LRU within each set

---

## Scope

**Included:** CLI + GUI simulator, direct-mapped and N-way set-associative (LRU), hex traces, hit/miss statistics and access log.

**Not included:** Multi-level caches, write policies, timing/power models, hardware design. All accesses are treated as reads.
