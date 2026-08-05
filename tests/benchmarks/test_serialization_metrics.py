import compas

if not compas.IPY:
    from benchmarks.serialization import metrics

    class DummyData:
        @property
        def __data__(self):
            return {"value": 1}

        def canonical_hash(self):
            return "hash"

    class CountingFormat:
        name = "counting"

        def __init__(self):
            self.dumps_calls = 0
            self.loads_calls = 0

        def dumps(self, obj):
            self.dumps_calls += 1
            return b"payload"

        def loads(self, blob):
            self.loads_calls += 1
            return DummyData()

    def test_measure_warms_up_dump_and_load_before_timing(monkeypatch):
        fmt = CountingFormat()
        original_time = metrics._time
        timed_call_counts = []

        def checking_time(callable_, repeat):
            timed_call_counts.append((fmt.dumps_calls, fmt.loads_calls))
            return original_time(callable_, repeat)

        monkeypatch.setattr(metrics, "_time", checking_time)

        result = metrics.measure(fmt, DummyData(), repeat=2)

        assert timed_call_counts == [(1, 1), (3, 1)]
        assert fmt.dumps_calls == 3  # warm-up + two timed calls
        assert fmt.loads_calls == 4  # warm-up + two timed calls + peak-memory probe
        assert result["lossless"] is True
