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

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "results")

# Per-subject sizes. Mesh sizes are vertex counts; pointcloud sizes are point counts.
PRESETS = {
    "quick": {
        "mesh": [1000, 10000],
        "mesh_attrs": [1000, 10000],
        "pointcloud": [10000, 100000],
    },
    "full": {  # PRD 10.1
        "mesh": [1000, 100000, 1000000, 5000000],
        "mesh_attrs": [1000, 100000, 1000000, 5000000],
        "pointcloud": [10000, 1000000, 10000000, 50000000],
    },
}

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
    sizes_by_subject = PRESETS[preset]

    for subject in subjects:
        factory = fixtures.SUBJECTS[subject]
        for size in sizes_by_subject[subject]:
            obj = factory(size, seed)
            measured = {f.name: metrics.measure(f, obj, repeat=repeat) for f in active_formats}
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
    args = parser.parse_args()

    rows = run(args.subjects, args.preset, args.formats, args.repeat, args.seed)
    print_table(rows)
    out = write_csv(rows, args.out)
    meta = {"preset": args.preset, "repeat": args.repeat, "seed": args.seed, "compas": compas.__version__}
    html_out = report.write_html(rows, os.path.splitext(out)[0] + ".html", meta=meta)
    print("\nWrote {} rows to {}\nWrote report to {}".format(len(rows), out, html_out))


if __name__ == "__main__":
    main()
