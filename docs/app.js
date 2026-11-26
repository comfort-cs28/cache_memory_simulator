const RESULT_HIT = "HIT";
const RESULT_MISS = "MISS";
const DIRECT_MAPPED_WAYS = 1;
const HEX_PREFIX = "0x";
const HIT_RATE_DECIMALS = 2;

const SAMPLE_TRACES = {
  hand_verified: {
    label: "hand_verified.txt (best first test)",
    text: `0x00
0x40
0x00
0x00
0x10
0x10`,
  },
  sample_addresses: {
    label: "sample_addresses.txt (general demo)",
    text: `0x0000
0x0004
0x0008
0x00C0
0x0000
0x00C4
0x0080
0x0004
0x00C8
0x0084
0x0008
0x00CC`,
  },
  associativity_demo: {
    label: "associativity_demo.txt (compare ways)",
    text: `0x0000
0x0040
0x0080
0x00C0
0x0000
0x0040
0x0080
0x00C0
0x0004
0x0044
0x0084
0x00C4`,
  },
};

const els = {
  trace_select: document.getElementById("trace_select"),
  trace_file: document.getElementById("trace_file"),
  cache_size: document.getElementById("cache_size"),
  block_size: document.getElementById("block_size"),
  ways: document.getElementById("ways"),
  run_btn: document.getElementById("run_btn"),
  clear_btn: document.getElementById("clear_btn"),
  status: document.getElementById("status"),
  log_body: document.getElementById("log_body"),
  stat_hit_rate: document.getElementById("stat_hit_rate"),
  stat_hits: document.getElementById("stat_hits"),
  stat_misses: document.getElementById("stat_misses"),
  stat_accesses: document.getElementById("stat_accesses"),
  stat_sets: document.getElementById("stat_sets"),
  stat_policy: document.getElementById("stat_policy"),
  stat_offset_bits: document.getElementById("stat_offset_bits"),
  stat_index_bits: document.getElementById("stat_index_bits"),
};

let uploaded_trace_text = null;

function is_power_of_two(value) {
  return value > 0 && (value & (value - 1)) === 0;
}

function parse_hex_address(raw_line, line_number) {
  let line = raw_line.trim().replace(/^\ufeff/, "");
  if (!line || line.startsWith("#")) {
    return null;
  }

  let text = line.toLowerCase();
  if (text.startsWith(HEX_PREFIX)) {
    text = text.slice(HEX_PREFIX.length);
  }
  if (!text) {
    throw new Error(`Line ${line_number}: empty address after '0x'.`);
  }

  const value = Number.parseInt(text, 16);
  if (Number.isNaN(value)) {
    throw new Error(`Line ${line_number}: invalid hexadecimal address '${line}'.`);
  }
  return value;
}

function parse_trace_text(raw_text) {
  const addresses = [];
  const lines = raw_text.split(/\r?\n/);
  lines.forEach((raw_line, index) => {
    const address = parse_hex_address(raw_line, index + 1);
    if (address !== null) {
      addresses.push(address);
    }
  });
  if (addresses.length === 0) {
    throw new Error("Trace contains no valid addresses.");
  }
  return addresses;
}

function build_decoder(cache_size, block_size, ways) {
  if (cache_size < 1 || block_size < 1 || ways < 1) {
    throw new Error("Cache size, block size, and ways must be at least 1.");
  }
  if (!is_power_of_two(cache_size) || !is_power_of_two(block_size)) {
    throw new Error("Cache size and block size must be powers of 2.");
  }
  if (cache_size % (block_size * ways) !== 0) {
    throw new Error("Cache size must be divisible by (block size × ways).");
  }

  const num_sets = cache_size / (block_size * ways);
  if (!is_power_of_two(num_sets)) {
    throw new Error("Number of sets must be a power of 2.");
  }

  const offset_bits = Math.log2(block_size);
  const index_bits = num_sets > 1 ? Math.log2(num_sets) : 0;
  const offset_mask = (1 << offset_bits) - 1;
  const index_mask = index_bits > 0 ? (1 << index_bits) - 1 : 0;

  return {
    cache_size,
    block_size,
    ways,
    num_sets,
    offset_bits,
    index_bits,
    decode(address) {
      const offset = address & offset_mask;
      const index = (address >> offset_bits) & index_mask;
      const tag = address >> (offset_bits + index_bits);
      return { tag, index, offset };
    },
  };
}

function run_simulation(cache_size, block_size, ways, addresses) {
  const decoder = build_decoder(cache_size, block_size, ways);
  const sets = Array.from({ length: decoder.num_sets }, () => []);
  let hits = 0;
  let misses = 0;
  const access_log = [];

  addresses.forEach((address) => {
    const { tag, index, offset } = decoder.decode(address);
    const cache_set = sets[index];
    const found_at = cache_set.indexOf(tag);

    let result;
    if (found_at >= 0) {
      cache_set.splice(found_at, 1);
      cache_set.push(tag);
      hits += 1;
      result = RESULT_HIT;
    } else {
      misses += 1;
      result = RESULT_MISS;
      if (cache_set.length >= ways) {
        cache_set.shift();
      }
      cache_set.push(tag);
    }

    access_log.push({ address, tag, index, offset, result });
  });

  const total_accesses = hits + misses;
  const hit_rate = total_accesses > 0 ? (hits / total_accesses) * 100 : 0;
  const mapping_policy =
    ways === DIRECT_MAPPED_WAYS
      ? "Direct-Mapped"
      : `${ways}-Way Set-Associative (LRU)`;

  return {
    stats: {
      mapping_policy,
      num_sets: decoder.num_sets,
      offset_bits: decoder.offset_bits,
      index_bits: decoder.index_bits,
      total_accesses,
      hits,
      misses,
      hit_rate,
    },
    access_log,
  };
}

function to_hex(address) {
  return `0x${address.toString(16).toUpperCase().padStart(8, "0")}`;
}

function clear_results() {
  els.stat_hit_rate.textContent = "0.00%";
  els.stat_hits.textContent = "0";
  els.stat_misses.textContent = "0";
  els.stat_accesses.textContent = "0";
  els.stat_sets.textContent = "—";
  els.stat_policy.textContent = "—";
  els.stat_offset_bits.textContent = "—";
  els.stat_index_bits.textContent = "—";
  els.log_body.innerHTML = "";
  els.status.textContent = "Results cleared. Ready for another simulation.";
}

function show_results(stats, access_log) {
  els.stat_hit_rate.textContent = `${stats.hit_rate.toFixed(HIT_RATE_DECIMALS)}%`;
  els.stat_hits.textContent = String(stats.hits);
  els.stat_misses.textContent = String(stats.misses);
  els.stat_accesses.textContent = String(stats.total_accesses);
  els.stat_sets.textContent = String(stats.num_sets);
  els.stat_policy.textContent = stats.mapping_policy;
  els.stat_offset_bits.textContent = String(stats.offset_bits);
  els.stat_index_bits.textContent = String(stats.index_bits);

  els.log_body.innerHTML = "";
  access_log.forEach((entry) => {
    const row = document.createElement("tr");
    const result_class = entry.result === RESULT_HIT ? "hit" : "miss";
    row.innerHTML = `
      <td>${to_hex(entry.address)}</td>
      <td>${entry.tag}</td>
      <td>${entry.index}</td>
      <td>${entry.offset}</td>
      <td class="${result_class}">${entry.result}</td>
    `;
    els.log_body.appendChild(row);
  });
}

function get_selected_addresses() {
  if (uploaded_trace_text) {
    return parse_trace_text(uploaded_trace_text);
  }
  const key = els.trace_select.value;
  return parse_trace_text(SAMPLE_TRACES[key].text);
}

function on_run() {
  try {
    const cache_size = Number(els.cache_size.value);
    const block_size = Number(els.block_size.value);
    const ways = Number(els.ways.value);
    const addresses = get_selected_addresses();
    const { stats, access_log } = run_simulation(
      cache_size,
      block_size,
      ways,
      addresses
    );
    show_results(stats, access_log);
    els.status.textContent =
      `Done: ${stats.total_accesses} accesses | ${stats.hits} hits | ` +
      `${stats.misses} misses | hit rate ${stats.hit_rate.toFixed(HIT_RATE_DECIMALS)}%`;
  } catch (error) {
    els.status.textContent = `Error: ${error.message}`;
    window.alert(error.message);
  }
}

function setup_trace_select() {
  Object.entries(SAMPLE_TRACES).forEach(([key, value]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = value.label;
    els.trace_select.appendChild(option);
  });
  els.trace_select.value = "hand_verified";
  els.cache_size.value = "64";
  els.block_size.value = "16";
  els.ways.value = "1";
}

els.trace_select.addEventListener("change", () => {
  uploaded_trace_text = null;
  els.trace_file.value = "";
  els.status.textContent = `Selected sample: ${SAMPLE_TRACES[els.trace_select.value].label}`;
});

els.trace_file.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) {
    return;
  }
  uploaded_trace_text = await file.text();
  els.status.textContent = `Uploaded: ${file.name}`;
});

els.run_btn.addEventListener("click", on_run);
els.clear_btn.addEventListener("click", clear_results);

setup_trace_select();
els.status.textContent =
  "Ready. Default trace: hand_verified.txt (cache 64, block 16, ways 1).";
