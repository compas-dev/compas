"""Runner for the serialization benchmark (PRD section 10).

Iterates subjects x sizes x formats, builds each fixture once, measures every format
against it, prints a readable table, and writes a CSV. Targets for the PRD's N1
("binary/columnar materially faster than JSON") are set from the numbers this emits.

Examples
--------
Quick baseline (default, small sizes, fast)::

    python -m benchmarks.serialization.run

Full PRD corpus (large; slow and memory-hungry)::

    python -m benchmarks.serialization.run --preset full

Subset::

    python -m benchmarks.serialization.run --subjects mesh pointcloud --formats json
"""

import argparse
import csv
import os

import compas
from benchmarks.serialization import fixtures
from benchmarks.serialization import formats
from benchmarks.serialization import metrics
from benchmarks.serialization import report
from benchmarks.serialization import samples

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "results")

# Sizes are element counts (vertices / points / nodes / primitives). DEFAULT_SIZES applies
# to any subject not given explicit sizes in PRESETS.
#
# The PRD (10.1) lists 5e6 vertices / 5e7 points as the largest sizes; the "full" preset caps
# at 1e6 / 1e7 so a run completes in reasonable time and memory on a workstation. The scaling
# trend for the N1 targets (binary/columnar vs JSON) is already clear at those sizes; bump the
# caps here for a machine that can take it.
DEFAULT_SIZES = {
    "quick": [1000, 10000],
    "full": [1000, 100000, 1000000],
}
PRESETS = {
    "quick": {
        "pointcloud": [10000, 100000],
    },
    "full": {
        "mesh": [1000, 100000, 1000000],
        "mesh_attrs": [1000, 100000, 1000000],
        "pointcloud": [10000, 1000000, 10000000],
    },
}


def _sizes_for(preset, subject):
    return PRESETS[preset].get(subject, DEFAULT_SIZES[preset])

CSV_COLUMNS = [
    "subject",
    "size",
    "format",
    "size_bytes",
    "compression_vs_json",
    # timing (seconds; median over --repeat runs, with spread)
    "dump_median_s",
    "dump_stdev_s",
    "load_median_s",
    "load_stdev_s",
    "roundtrip_median_s",
    # throughput on the serialized payload (MB of wire per second)
    "dump_mb_s",
    "load_mb_s",
    "peak_mem_bytes",
    "lossless",
    "data_equal",
    "canonical_hash_equal",
    # fidelity of lossy profiles (float32 etc.) — quantified coordinate error
    "max_abs_error",
    "rms_error",
    "note",
]


def _mb_per_s(size_bytes, seconds):
    if not seconds:
        return float("nan")
    return round((size_bytes / 1e6) / seconds, 3)


def _human_bytes(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024 or unit == "GB":
            return "{:.1f}{}".format(n, unit)
        n /= 1024.0


def run(subjects, preset, format_names, repeat, seed):
    active_formats = [f for f in formats.formats() if f.available and (not format_names or f.name in format_names)]
    if not active_formats:
        raise SystemExit("No matching available formats.")

    rows = []

    for subject in subjects:
        factory = fixtures.SUBJECTS[subject]
        for size in _sizes_for(preset, subject):
            # Build a fresh fixture per format: serializing accesses .guid on some paths (JSON
            # forces it), which would mutate a shared object and unfairly change what a later
            # format encodes. A pristine object per format keeps each measurement independent.
            measured = {f.name: metrics.measure(f, factory(size, seed), repeat=repeat) for f in active_formats}
            json_size = measured.get("json", {}).get("size_bytes")

            for fmt in active_formats:
                m = measured[fmt.name]
                ratio = (json_size / m["size_bytes"]) if json_size else float("nan")
                roundtrip = m["dump_median_s"] + m["load_median_s"]
                rows.append(
                    {
                        "subject": subject,
                        "size": size,
                        "format": fmt.name,
                        "size_bytes": m["size_bytes"],
                        "compression_vs_json": round(ratio, 3),
                        "dump_median_s": round(m["dump_median_s"], 6),
                        "dump_stdev_s": round(m["dump_stdev_s"], 6),
                        "load_median_s": round(m["load_median_s"], 6),
                        "load_stdev_s": round(m["load_stdev_s"], 6),
                        "roundtrip_median_s": round(roundtrip, 6),
                        "dump_mb_s": _mb_per_s(m["size_bytes"], m["dump_median_s"]),
                        "load_mb_s": _mb_per_s(m["size_bytes"], m["load_median_s"]),
                        "peak_mem_bytes": m["peak_mem_bytes"],
                        "lossless": m["lossless"],
                        "data_equal": m["data_equal"],
                        "canonical_hash_equal": m["canonical_hash_equal"],
                        "max_abs_error": m["max_abs_error"],
                        "rms_error": m["rms_error"],
                        "note": fmt.note,
                    }
                )
    return rows


def print_table(rows):
    header = "{:<12} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>8}".format(
        "subject", "size", "format", "size", "dump_s", "load_s", "trip_s", "peak", "lossless"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            "{:<12} {:>10} {:>10} {:>10} {:>10.5f} {:>10.5f} {:>10.5f} {:>10} {:>8}".format(
                r["subject"],
                r["size"],
                r["format"],
                _human_bytes(r["size_bytes"]),
                r["dump_median_s"],
                r["load_median_s"],
                r["roundtrip_median_s"],
                _human_bytes(r["peak_mem_bytes"]),
                str(r["lossless"]),
            )
        )


def write_csv(rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="COMPAS serialization benchmark (PRD phase 1).")
    parser.add_argument("--subjects", nargs="+", choices=sorted(fixtures.SUBJECTS), default=sorted(fixtures.SUBJECTS))
    parser.add_argument("--preset", choices=sorted(PRESETS), default="quick")
    parser.add_argument("--formats", nargs="*", default=None, help="Subset of format names; default all available.")
    parser.add_argument("--repeat", type=int, default=5, help="Timed runs per measurement (median reported).")
    parser.add_argument("--seed", type=int, default=fixtures.DEFAULT_SEED)
    parser.add_argument("--out", default=os.path.join(RESULTS_DIR, "baseline_quick.csv"), help="CSV output path.")
    parser.add_argument("--no-samples", action="store_true", help="Skip writing encoded-format samples.")
    args = parser.parse_args()

    rows = run(args.subjects, args.preset, args.formats, args.repeat, args.seed)
    print_table(rows)
    out = write_csv(rows, args.out)
    meta = {"preset": args.preset, "repeat": args.repeat, "seed": args.seed, "compas": compas.__version__}
    html_out = report.write_html(rows, os.path.splitext(out)[0] + ".html", meta=meta)
    print("\nWrote {} rows to {}\nWrote report to {}".format(len(rows), out, html_out))

    if not args.no_samples:
        sample_files = samples.dump_samples(os.path.join(os.path.dirname(out) or ".", "samples"), seed=args.seed)
        print("Wrote {} encoded-format samples to {}/samples/".format(len(sample_files), os.path.dirname(out) or "."))


if __name__ == "__main__":
    main()
