# Encoded-format samples

Tiny, fully-inspectable fixtures encoded with the three main (uncompressed) formats, so you
can see the *shape* of each encoding. Regenerate with:

    python -m benchmarks.serialization.samples

Per subject:

| file | what it is |
|------|------------|
| `<subject>.json` | JSON wire format (text) |
| `<subject>.pb` | raw protobuf bytes |
| `<subject>.pb.json` | protobuf message deserialized + re-serialized to JSON (readable wire structure) |
| `<subject>.msgpack` | raw MessagePack bytes |
| `<subject>.msgpack.json` | decoded MessagePack tree as JSON (row-oriented `{dtype, data}`) |

`*.pb.json` shows the schema'd/columnar layout (flat vertex arrays, CSR faces, attribute
columns); `*.msgpack.json` shows the row-oriented dict tree.
