import compas

try:
    import System

    def test_decimal():
        before = System.Decimal(100.0)

        after = compas.json_loads(compas.json_dumps(before))
        assert after == 100.0

except ImportError:
    pass
