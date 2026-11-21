"""
Graphical interface for the Configurable Cache Memory Simulator.

Uses tkinter from the Python standard library.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from constants import (
    DEFAULT_BLOCK_SIZE,
    DEFAULT_CACHE_SIZE,
    DEFAULT_WAYS,
    DIRECT_MAPPED_WAYS,
    GUI_COLOR_BORDER,
    GUI_COLOR_CREAM,
    GUI_COLOR_GOLD,
    GUI_COLOR_HIT,
    GUI_COLOR_MISS,
    GUI_COLOR_MUTED,
    GUI_COLOR_NAVY,
    GUI_COLOR_NAVY_MID,
    GUI_COLOR_WHITE,
    GUI_CURSOR_POINTER,
    GUI_FONT_BODY,
    GUI_FONT_BODY_BOLD,
    GUI_FONT_HEADING,
    GUI_FONT_MONO,
    GUI_FONT_STAT_LABEL,
    GUI_FONT_STAT_VALUE,
    GUI_FONT_TITLE,
    GUI_MIN_HEIGHT,
    GUI_MIN_WIDTH,
    GUI_WAYS_OPTIONS,
    GUI_WINDOW_HEIGHT,
    GUI_WINDOW_TITLE,
    GUI_WINDOW_WIDTH,
    HIT_RATE_DECIMALS,
    RESULT_HIT,
    RESULT_MISS,
)
from input_reader import read_trace_file
from simulation_runner import run_simulation


class CacheSimulatorGUI:
    """Main window for configuring and running cache simulations."""

    def __init__(self, root):
        self.root = root
        self.root.title(GUI_WINDOW_TITLE)
        self.root.geometry(f"{GUI_WINDOW_WIDTH}x{GUI_WINDOW_HEIGHT}")
        self.root.minsize(GUI_MIN_WIDTH, GUI_MIN_HEIGHT)
        self.root.configure(bg=GUI_COLOR_CREAM)

        self.trace_path = tk.StringVar(value="")
        self.cache_size = tk.StringVar(value=str(DEFAULT_CACHE_SIZE))
        self.block_size = tk.StringVar(value=str(DEFAULT_BLOCK_SIZE))
        self.ways = tk.StringVar(value=str(DEFAULT_WAYS))
        self.status_text = tk.StringVar(value="Load a trace file, set options, then Run Simulation.")

        self.stat_vars = {
            "mapping_policy": tk.StringVar(value="—"),
            "num_sets": tk.StringVar(value="—"),
            "offset_bits": tk.StringVar(value="—"),
            "index_bits": tk.StringVar(value="—"),
            "total_accesses": tk.StringVar(value="0"),
            "hits": tk.StringVar(value="0"),
            "misses": tk.StringVar(value="0"),
            "hit_rate": tk.StringVar(value="0.00%"),
        }

        self._build_styles()
        self._build_layout()

    def _build_styles(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=GUI_COLOR_CREAM)
        style.configure("Card.TFrame", background=GUI_COLOR_WHITE)
        style.configure("TLabel", background=GUI_COLOR_CREAM, foreground=GUI_COLOR_NAVY, font=GUI_FONT_BODY)
        style.configure("Card.TLabel", background=GUI_COLOR_WHITE, foreground=GUI_COLOR_NAVY, font=GUI_FONT_BODY)
        style.configure("Muted.TLabel", background=GUI_COLOR_CREAM, foreground=GUI_COLOR_MUTED, font=GUI_FONT_BODY)
        style.configure("Heading.TLabel", background=GUI_COLOR_WHITE, foreground=GUI_COLOR_NAVY, font=GUI_FONT_HEADING)
        style.configure("StatValue.TLabel", background=GUI_COLOR_WHITE, foreground=GUI_COLOR_NAVY, font=GUI_FONT_STAT_VALUE)
        style.configure("StatLabel.TLabel", background=GUI_COLOR_WHITE, foreground=GUI_COLOR_MUTED, font=GUI_FONT_STAT_LABEL)
        style.configure("TEntry", fieldbackground=GUI_COLOR_WHITE, font=GUI_FONT_BODY)
        style.configure("TCombobox", fieldbackground=GUI_COLOR_WHITE, font=GUI_FONT_BODY)
        style.configure(
            "Treeview",
            background=GUI_COLOR_WHITE,
            fieldbackground=GUI_COLOR_WHITE,
            foreground=GUI_COLOR_NAVY,
            rowheight=24,
            font=GUI_FONT_MONO,
        )
        style.configure(
            "Treeview.Heading",
            background=GUI_COLOR_NAVY,
            foreground=GUI_COLOR_WHITE,
            font=GUI_FONT_BODY_BOLD,
        )
        style.map("Treeview.Heading", background=[("active", GUI_COLOR_NAVY_MID)])

    def _build_layout(self):
        self._build_header()
        body = ttk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 8))

        left = ttk.Frame(body)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        self._build_config_panel(left)

        right = ttk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_stats_panel(right)
        self._build_log_panel(right)

        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=16, pady=(0, 12))
        ttk.Label(footer, textvariable=self.status_text, style="Muted.TLabel").pack(anchor=tk.W)

    def _build_header(self):
        header = tk.Frame(self.root, bg=GUI_COLOR_NAVY, height=72)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Cache Memory Simulator",
            bg=GUI_COLOR_NAVY,
            fg=GUI_COLOR_WHITE,
            font=GUI_FONT_TITLE,
        )
        title.pack(side=tk.LEFT, padx=20, pady=16)

        subtitle = tk.Label(
            header,
            text="Direct-Mapped  •  N-Way Set-Associative (LRU)",
            bg=GUI_COLOR_NAVY,
            fg=GUI_COLOR_GOLD,
            font=GUI_FONT_BODY,
        )
        subtitle.pack(side=tk.LEFT, padx=(0, 20), pady=22)

        gold_line = tk.Frame(self.root, bg=GUI_COLOR_GOLD, height=4)
        gold_line.pack(fill=tk.X)

    def _build_config_panel(self, parent):
        card = tk.Frame(parent, bg=GUI_COLOR_WHITE, highlightbackground=GUI_COLOR_BORDER, highlightthickness=1)
        card.pack(fill=tk.Y)

        inner = ttk.Frame(card, style="Card.TFrame")
        inner.pack(fill=tk.BOTH, padx=14, pady=14)

        ttk.Label(inner, text="Configuration", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 10))

        ttk.Label(inner, text="Trace file", style="Card.TLabel").pack(anchor=tk.W)
        file_row = ttk.Frame(inner, style="Card.TFrame")
        file_row.pack(fill=tk.X, pady=(2, 10))
        entry = ttk.Entry(file_row, textvariable=self.trace_path, width=28)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        browse_btn = tk.Button(
            file_row,
            text="Browse",
            command=self._browse_trace,
            bg=GUI_COLOR_NAVY_MID,
            fg=GUI_COLOR_WHITE,
            activebackground=GUI_COLOR_NAVY,
            activeforeground=GUI_COLOR_WHITE,
            relief=tk.FLAT,
            padx=10,
            cursor=GUI_CURSOR_POINTER,
            font=GUI_FONT_BODY_BOLD,
        )
        browse_btn.pack(side=tk.LEFT, padx=(6, 0))

        self._labeled_entry(inner, "Cache size (bytes)", self.cache_size)
        self._labeled_entry(inner, "Block size (bytes)", self.block_size)

        ttk.Label(inner, text="Ways (1 = direct-mapped)", style="Card.TLabel").pack(anchor=tk.W, pady=(4, 0))
        ways_box = ttk.Combobox(
            inner,
            textvariable=self.ways,
            values=[str(value) for value in GUI_WAYS_OPTIONS],
            width=26,
        )
        ways_box.pack(anchor=tk.W, pady=(2, 12))

        run_btn = tk.Button(
            inner,
            text="Run Simulation",
            command=self._run_simulation,
            bg=GUI_COLOR_GOLD,
            fg=GUI_COLOR_NAVY,
            activebackground="#B8923F",
            activeforeground=GUI_COLOR_NAVY,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor=GUI_CURSOR_POINTER,
            font=GUI_FONT_BODY_BOLD,
        )
        run_btn.pack(fill=tk.X, pady=(4, 6))

        clear_btn = tk.Button(
            inner,
            text="Clear Results",
            command=self._clear_results,
            bg=GUI_COLOR_NAVY,
            fg=GUI_COLOR_WHITE,
            activebackground=GUI_COLOR_NAVY_MID,
            activeforeground=GUI_COLOR_WHITE,
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor=GUI_CURSOR_POINTER,
            font=GUI_FONT_BODY_BOLD,
        )
        clear_btn.pack(fill=tk.X)

        tip = (
            "Tip: ways = 1 is direct-mapped.\n"
            "Higher ways use LRU replacement\n"
            "inside each set."
        )
        ttk.Label(inner, text=tip, style="Card.TLabel", foreground=GUI_COLOR_MUTED).pack(
            anchor=tk.W, pady=(14, 0)
        )

    def _labeled_entry(self, parent, label, variable):
        ttk.Label(parent, text=label, style="Card.TLabel").pack(anchor=tk.W, pady=(4, 0))
        entry = ttk.Entry(parent, textvariable=variable, width=28)
        entry.pack(anchor=tk.W, pady=(2, 6))

    def _build_stats_panel(self, parent):
        card = tk.Frame(parent, bg=GUI_COLOR_WHITE, highlightbackground=GUI_COLOR_BORDER, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 12))

        inner = ttk.Frame(card, style="Card.TFrame")
        inner.pack(fill=tk.X, padx=14, pady=12)

        ttk.Label(inner, text="Results", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 8))

        grid = ttk.Frame(inner, style="Card.TFrame")
        grid.pack(fill=tk.X)

        stats = [
            ("Hit Rate", "hit_rate"),
            ("Hits", "hits"),
            ("Misses", "misses"),
            ("Accesses", "total_accesses"),
            ("Sets", "num_sets"),
            ("Policy", "mapping_policy"),
        ]
        for index, (label, key) in enumerate(stats):
            cell = ttk.Frame(grid, style="Card.TFrame")
            cell.grid(row=index // 3, column=index % 3, sticky="nsew", padx=8, pady=6)
            ttk.Label(cell, text=label, style="StatLabel.TLabel").pack(anchor=tk.W)
            ttk.Label(cell, textvariable=self.stat_vars[key], style="StatValue.TLabel").pack(anchor=tk.W)

        for column in range(3):
            grid.columnconfigure(column, weight=1)

        meta = ttk.Frame(inner, style="Card.TFrame")
        meta.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(meta, text="Offset bits:", style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Label(meta, textvariable=self.stat_vars["offset_bits"], style="Card.TLabel").pack(side=tk.LEFT, padx=(4, 16))
        ttk.Label(meta, text="Index bits:", style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Label(meta, textvariable=self.stat_vars["index_bits"], style="Card.TLabel").pack(side=tk.LEFT, padx=(4, 0))

    def _build_log_panel(self, parent):
        card = tk.Frame(parent, bg=GUI_COLOR_WHITE, highlightbackground=GUI_COLOR_BORDER, highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        inner = ttk.Frame(card, style="Card.TFrame")
        inner.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        ttk.Label(inner, text="Access Log (Tag / Index / Offset)", style="Heading.TLabel").pack(
            anchor=tk.W, pady=(0, 8)
        )

        columns = ("address", "tag", "index", "offset", "result")
        self.log_tree = ttk.Treeview(inner, columns=columns, show="headings", selectmode="browse")
        headings = {
            "address": "Address",
            "tag": "Tag",
            "index": "Index",
            "offset": "Offset",
            "result": "Result",
        }
        widths = {"address": 140, "tag": 100, "index": 90, "offset": 90, "result": 90}
        for column in columns:
            self.log_tree.heading(column, text=headings[column])
            self.log_tree.column(column, width=widths[column], anchor=tk.CENTER)

        self.log_tree.tag_configure(RESULT_HIT, foreground=GUI_COLOR_HIT)
        self.log_tree.tag_configure(RESULT_MISS, foreground=GUI_COLOR_MISS)

        scroll_y = ttk.Scrollbar(inner, orient=tk.VERTICAL, command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scroll_y.set)
        self.log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def _browse_trace(self):
        initial_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traces")
        if not os.path.isdir(initial_dir):
            initial_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = filedialog.askopenfilename(
            title="Select memory address trace",
            initialdir=initial_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            self.trace_path.set(file_path)
            self.status_text.set(f"Selected: {os.path.basename(file_path)}")

    def _parse_positive_int(self, raw_value, field_name):
        try:
            value = int(str(raw_value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be a whole number.") from exc
        if value < 1:
            raise ValueError(f"{field_name} must be at least 1.")
        return value

    def _run_simulation(self):
        try:
            trace = self.trace_path.get().strip()
            if not trace:
                raise ValueError("Please choose a trace file first.")

            cache_size = self._parse_positive_int(self.cache_size.get(), "Cache size")
            block_size = self._parse_positive_int(self.block_size.get(), "Block size")
            ways = self._parse_positive_int(self.ways.get(), "Ways")

            addresses = read_trace_file(trace)
            stats, access_log = run_simulation(cache_size, block_size, ways, addresses)
            self._show_results(stats, access_log)
            self.status_text.set(
                f"Done: {stats['total_accesses']} accesses  |  "
                f"{stats['hits']} hits  |  {stats['misses']} misses  |  "
                f"hit rate {stats['hit_rate']:.{HIT_RATE_DECIMALS}f}%"
            )
        except (ValueError, FileNotFoundError, OSError) as error:
            messagebox.showerror("Simulation Error", str(error))
            self.status_text.set(f"Error: {error}")

    def _show_results(self, stats, access_log):
        self.stat_vars["mapping_policy"].set(stats["mapping_policy"])
        self.stat_vars["num_sets"].set(str(stats["num_sets"]))
        self.stat_vars["offset_bits"].set(str(stats["offset_bits"]))
        self.stat_vars["index_bits"].set(str(stats["index_bits"]))
        self.stat_vars["total_accesses"].set(str(stats["total_accesses"]))
        self.stat_vars["hits"].set(str(stats["hits"]))
        self.stat_vars["misses"].set(str(stats["misses"]))
        self.stat_vars["hit_rate"].set(f"{stats['hit_rate']:.{HIT_RATE_DECIMALS}f}%")

        self.log_tree.delete(*self.log_tree.get_children())
        for entry in access_log:
            result = entry["result"]
            self.log_tree.insert(
                "",
                tk.END,
                values=(
                    f"0x{entry['address']:08X}",
                    entry["tag"],
                    entry["index"],
                    entry["offset"],
                    result,
                ),
                tags=(result,),
            )

    def _clear_results(self):
        for key, variable in self.stat_vars.items():
            if key in ("total_accesses", "hits", "misses"):
                variable.set("0")
            elif key == "hit_rate":
                variable.set("0.00%")
            else:
                variable.set("—")
        self.log_tree.delete(*self.log_tree.get_children())
        self.status_text.set("Results cleared. Ready for another simulation.")


def launch_gui():
    """Create and run the GUI application."""
    root = tk.Tk()
    CacheSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
