"""Metrics for the serialization benchmark (PRD 10.3).

For a given fixture object and format, :func:`measure` reports:

* serialized size (bytes on the wire);
* serialize and deserialize time (median + spread over several runs);
* peak memory during deserialize (``tracemalloc``);
* round-trip fidelity: exact equality of ``__data__`` and of the format-independent
  ``canonical_hash`` (this is where a lossy profile such as protobuf-float32 would show up).
"""

import statistics
import time
import tracemalloc


def _time(callable_, repeat):
    samples = []
    result = None
    for _ in range(repeat):
        start = time.perf_counter()
        result = callable_()
        samples.append(time.perf_counter() - start)
    return result, samples


def _summarize(samples):
    return {
        "median_s": statistics.median(samples),
        "min_s": min(samples),
        "max_s": max(samples),
        "stdev_s": statistics.pstdev(samples) if len(samples) > 1 else 0.0,
    }


def _collect_numeric_pairs(a, b, out):
    """Walk two same-shaped structures in parallel, collecting (original, roundtrip) numeric leaves.

    Returns False if the shapes diverge (e.g. a lossy format dropped keys or changed the
    layout), in which case a coordinate error is not meaningful.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return False
        return all(_collect_numeric_pairs(a[k], b[k], out) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(_collect_numeric_pairs(x, y, out) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        out.append((float(a), float(b)))
        return True
    return a == b


def numeric_error(original, roundtrip):
    """Max-absolute and RMS error over paired numeric leaves of two ``__data__`` structures.

    This is where a lossy profile (e.g. protobuf float32) gets quantified (PRD 10.3).
    Returns ``None`` errors when the structures are not comparable leaf-for-leaf.
    """
    pairs = []
    if not _collect_numeric_pairs(original, roundtrip, pairs) or not pairs:
        return {"max_abs_error": None, "rms_error": None}
    diffs = [abs(x - y) for x, y in pairs]
    rms = (sum(d * d for d in diffs) / len(diffs)) ** 0.5
    return {"max_abs_error": max(diffs), "rms_error": rms}


def measure(fmt, obj, repeat=5):
    """Serialize/deserialize ``obj`` with ``fmt`` and return a metrics dict.

    Parameters
    ----------
    fmt : :class:`.formats.Format`
    obj : :class:`compas.data.Data`
    repeat : int, optional
        Number of timed runs; the median and spread are reported.

    Returns
    -------
    dict
    """
    blob, dump_samples = _time(lambda: fmt.dumps(obj), repeat)
    roundtrip, load_samples = _time(lambda: fmt.loads(blob), repeat)

    # Peak memory during a single, untimed deserialize (tracemalloc perturbs timing).
    tracemalloc.start()
    tracemalloc.reset_peak()
    fmt.loads(blob)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    data_equal = obj.__data__ == roundtrip.__data__
    hash_equal = obj.canonical_hash() == roundtrip.canonical_hash()
    error = numeric_error(obj.__data__, roundtrip.__data__)

    row = {
        "format": fmt.name,
        "size_bytes": len(blob),
        "peak_mem_bytes": peak_bytes,
        "lossless": bool(data_equal and hash_equal),
        "data_equal": bool(data_equal),
        "canonical_hash_equal": bool(hash_equal),
        "max_abs_error": error["max_abs_error"],
        "rms_error": error["rms_error"],
    }
    for key, value in _summarize(dump_samples).items():
        row["dump_" + key] = value
    for key, value in _summarize(load_samples).items():
        row["load_" + key] = value
    return row
