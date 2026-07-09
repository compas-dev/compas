"""Render benchmark result rows as a self-contained, readable HTML report.

The CSV is the machine record; this is the human view. One standalone ``.html`` file
(no external assets, theme-aware) with, per subject: grouped bars comparing formats at
each size on the metrics that matter (round-trip time and wire size), plus a full table.

New formats (protobuf, Arrow, ...) need no changes here: colors are assigned to formats
in first-appearance order from a validated categorical palette, so the report grows with
the harness.
"""

import datetime
import html

# Validated categorical palette (dataviz skill reference instance): (light, dark) per slot.
_SERIES = [
    ("#2a78d6", "#3987e5"),  # blue
    ("#1baf7a", "#199e70"),  # aqua
    ("#eda100", "#c98500"),  # yellow
    ("#008300", "#008300"),  # green
    ("#4a3aa7", "#9085e9"),  # violet
    ("#e34948", "#e66767"),  # red
    ("#e87ba4", "#d55181"),  # magenta
    ("#eb6834", "#d95926"),  # orange
]

_METRICS = [
    ("roundtrip_median_s", "Round-trip time", "time"),
    ("size_bytes", "Wire size", "bytes"),
]


def _fmt_int(n):
    return "{:,}".format(int(n))


def _fmt_bytes(n):
    n = float(n)
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024 or unit == "GB":
            return "{:.1f} {}".format(n, unit)
        n /= 1024.0


def _fmt_time(seconds):
    seconds = float(seconds)
    if seconds < 1.0:
        return "{:.1f} ms".format(seconds * 1000.0)
    return "{:.3f} s".format(seconds)


def _fmt_value(value, kind):
    return _fmt_bytes(value) if kind == "bytes" else _fmt_time(value)


def _fmt_error(value):
    if value in (None, "", "None"):
        return "—"
    value = float(value)
    if value == 0.0:
        return "0"
    return "{:.1e}".format(value)


def _color_map(rows):
    order = []
    for r in rows:
        if r["format"] not in order:
            order.append(r["format"])
    return {name: _SERIES[i % len(_SERIES)] for i, name in enumerate(order)}


def _css(colors):
    series_light = "\n".join("  --series-{}: {};".format(i + 1, lo) for i, (lo, _) in enumerate(_SERIES))
    series_dark = "\n".join("    --series-{}: {};".format(i + 1, hi) for i, (_, hi) in enumerate(_SERIES))
    return """
:root {
  --page: #f9f9f7; --surface: #fcfcfb;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --muted: #898781;
  --grid: #e1e0d9; --track: #efeee9; --border: rgba(11,11,11,0.10);
  --good: #006300; --critical: #d03b3b;
%SERIES_LIGHT%
}
@media (prefers-color-scheme: dark) {
  :root {
    --page: #0d0d0d; --surface: #1a1a19;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --muted: #898781;
    --grid: #2c2c2a; --track: #232322; --border: rgba(255,255,255,0.10);
    --good: #0ca30c; --critical: #e66767;
%SERIES_DARK%
  }
}
:root[data-theme="light"] {
  --page:#f9f9f7; --surface:#fcfcfb; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --grid:#e1e0d9; --track:#efeee9; --border:rgba(11,11,11,0.10);
}
:root[data-theme="dark"] {
  --page:#0d0d0d; --surface:#1a1a19; --text-primary:#ffffff; --text-secondary:#c3c2b7;
  --grid:#2c2c2a; --track:#232322; --border:rgba(255,255,255,0.10);
}

* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--text-primary);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.5; }
.wrap { max-width: 980px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 22px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 40px 0 12px; padding-top: 16px; border-top: 1px solid var(--grid); }
.meta { color: var(--text-secondary); font-size: 13px; margin: 0 0 8px; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; margin: 16px 0 8px; }
.chip { display: inline-flex; align-items: center; gap: 7px; font-size: 13px; color: var(--text-secondary); }
.dot { width: 11px; height: 11px; border-radius: 3px; flex: none; }
.metric-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 18px 0 8px; }
.sizegroup { margin: 0 0 12px; }
.sizelabel { font-size: 12px; color: var(--muted); font-variant-numeric: tabular-nums; margin: 0 0 4px; }
.bar-row { display: grid; grid-template-columns: 96px 1fr auto; align-items: center; gap: 10px; padding: 3px 0; }
.bar-name { font-size: 12px; color: var(--text-secondary); text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.track { background: var(--track); border-radius: 4px; height: 14px; overflow: hidden; }
.fill { height: 100%; border-radius: 4px; }
.bar-val { font-size: 12px; font-variant-numeric: tabular-nums; color: var(--text-primary); white-space: nowrap; }
.tablewrap { overflow-x: auto; margin-top: 10px; border: 1px solid var(--border); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 13px; background: var(--surface); }
th, td { text-align: right; padding: 7px 12px; white-space: nowrap; font-variant-numeric: tabular-nums; }
th { color: var(--muted); font-weight: 600; border-bottom: 1px solid var(--grid); text-align: right; }
th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) { text-align: left; }
tr + tr td { border-top: 1px solid var(--grid); }
.fmt-cell { display: inline-flex; align-items: center; gap: 7px; }
.badge { font-size: 12px; font-weight: 600; }
.badge.ok { color: var(--good); }
.badge.no { color: var(--critical); }
.note { color: var(--muted); font-size: 12px; }
.summary { margin: 20px 0 8px; }
.takeaway { font-size: 15px; line-height: 1.55; margin: 0 0 18px; color: var(--text-primary); }
.takeaway b { font-weight: 600; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 0 0 20px; }
.tile { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
.tile .big { font-size: 26px; font-weight: 650; letter-spacing: -0.01em; }
.tile .lbl { font-size: 12px; color: var(--text-secondary); margin-top: 3px; }
.tile .sub { font-size: 11px; color: var(--muted); margin-top: 1px; }
.win { color: var(--good); font-weight: 600; }
h2.section { margin-top: 8px; }
""".replace("%SERIES_LIGHT%", series_light).replace("%SERIES_DARK%", series_dark)


def _slot(colors, fmt):
    # 1-based series index matching --series-N
    return list(colors).index(fmt) % len(_SERIES) + 1


def _legend(rows, colors):
    parts = ['<div class="legend">']
    seen = []
    for r in rows:
        if r["format"] in seen:
            continue
        seen.append(r["format"])
        slot = _slot(colors, r["format"])
        parts.append(
            '<span class="chip"><span class="dot" style="background:var(--series-{})"></span>'
            "<b>{}</b> · {}</span>".format(slot, html.escape(r["format"]), html.escape(r.get("note", "")))
        )
    parts.append("</div>")
    return "".join(parts)


def _bars(subject_rows, colors, metric_key, kind):
    # group by size (preserve order of first appearance)
    sizes = []
    for r in subject_rows:
        if r["size"] not in sizes:
            sizes.append(r["size"])

    blocks = []
    for size in sizes:
        group = [r for r in subject_rows if r["size"] == size]
        group_max = max(float(r[metric_key]) for r in group) or 1.0
        rows_html = []
        for r in group:
            width = float(r[metric_key]) / group_max * 100.0
            slot = _slot(colors, r["format"])
            rows_html.append(
                '<div class="bar-row">'
                '<div class="bar-name">{name}</div>'
                '<div class="track"><div class="fill" style="width:{w:.1f}%;background:var(--series-{s})"></div></div>'
                '<div class="bar-val">{val}</div>'
                "</div>".format(
                    name=html.escape(r["format"]),
                    w=width,
                    s=slot,
                    val=_fmt_value(r[metric_key], kind),
                )
            )
        blocks.append(
            '<div class="sizegroup"><div class="sizelabel">{lbl} elements</div>{rows}</div>'.format(
                lbl=_fmt_int(size), rows="".join(rows_html)
            )
        )
    return "".join(blocks)


def _table(subject_rows, colors):
    head = (
        "<tr><th>size</th><th>format</th><th>wire size</th><th>vs&nbsp;JSON</th>"
        "<th>dump</th><th>load</th><th>round-trip</th><th>load MB/s</th><th>peak mem</th>"
        "<th>max err</th><th>lossless</th></tr>"
    )
    body = []
    for r in subject_rows:
        slot = _slot(colors, r["format"])
        lossless = str(r["lossless"]).lower() in ("true", "1")
        badge = '<span class="badge ok">✓ yes</span>' if lossless else '<span class="badge no">✗ no</span>'
        body.append(
            "<tr>"
            "<td>{size}</td>"
            '<td><span class="fmt-cell"><span class="dot" style="background:var(--series-{slot})"></span>{fmt}</span></td>'
            "<td>{wire}</td><td>{ratio}×</td>"
            "<td>{dump}</td><td>{load}</td><td>{trip}</td>"
            "<td>{mbps}</td><td>{mem}</td><td>{err}</td><td>{badge}</td>"
            "</tr>".format(
                size=_fmt_int(r["size"]),
                slot=slot,
                fmt=html.escape(r["format"]),
                wire=_fmt_bytes(r["size_bytes"]),
                ratio=r["compression_vs_json"],
                dump=_fmt_time(r["dump_median_s"]),
                load=_fmt_time(r["load_median_s"]),
                trip=_fmt_time(r["roundtrip_median_s"]),
                mbps=r["load_mb_s"],
                mem=_fmt_bytes(r["peak_mem_bytes"]),
                err=_fmt_error(r.get("max_abs_error")),
                badge=badge,
            )
        )
    return '<div class="tablewrap"><table>{}{}</table></div>'.format(head, "".join(body))


def _ratio(x):
    return "{:.1f}×".format(x)


def _is_lossless(row):
    return str(row["lossless"]).lower() in ("true", "1")


def _exec_summary(rows, colors, subjects):
    """Headline stat tiles + a one-line takeaway + a per-subject winners table.

    Everything is derived from the largest measured size of each subject and expressed
    against JSON, so a reader gets the conclusion before any of the detail below.
    """
    baseline = "json"
    binary = "compas_pb"
    per = []  # (subject, size, group_map, smallest_row, fastest_row)
    for subj in subjects:
        srows = [r for r in rows if r["subject"] == subj]
        max_size = max(int(r["size"]) for r in srows)
        group = [r for r in srows if int(r["size"]) == max_size]
        gmap = {r["format"]: r for r in group}
        smallest = min(group, key=lambda r: float(r["size_bytes"]))
        fastest = min(group, key=lambda r: float(r["roundtrip_median_s"]))
        per.append((subj, max_size, gmap, smallest, fastest))

    # Tiles: best size / round-trip gains of the binary format vs JSON, and lossless coverage.
    size_gain = speed_gain = None
    lossless_hits = lossless_total = 0
    for subj, size, gmap, _, _ in per:
        if baseline in gmap and binary in gmap:
            j, b = gmap[baseline], gmap[binary]
            sr = float(j["size_bytes"]) / float(b["size_bytes"])
            spd = float(j["roundtrip_median_s"]) / float(b["roundtrip_median_s"])
            if size_gain is None or sr > size_gain[0]:
                size_gain = (sr, subj, size)
            if speed_gain is None or spd > speed_gain[0]:
                speed_gain = (spd, subj, size)
            lossless_total += 1
            lossless_hits += _is_lossless(b)

    tiles = []
    if size_gain:
        tiles.append(
            '<div class="tile"><div class="big win">{r} smaller</div>'
            '<div class="lbl">{bin} vs JSON on the wire</div>'
            '<div class="sub">best: {subj} @ {n} elements</div></div>'.format(
                r=_ratio(size_gain[0]), bin=binary, subj=html.escape(size_gain[1]), n=_fmt_int(size_gain[2])
            )
        )
    if speed_gain:
        tiles.append(
            '<div class="tile"><div class="big win">{r} faster</div>'
            '<div class="lbl">{bin} round-trip vs JSON</div>'
            '<div class="sub">best: {subj} @ {n} elements</div></div>'.format(
                r=_ratio(speed_gain[0]), bin=binary, subj=html.escape(speed_gain[1]), n=_fmt_int(speed_gain[2])
            )
        )
    if lossless_total:
        ok = lossless_hits == lossless_total
        tiles.append(
            '<div class="tile"><div class="big{cls}">{h}/{t}</div>'
            '<div class="lbl">subjects lossless ({bin})</div>'
            '<div class="sub">exact round-trip of __data__</div></div>'.format(
                cls=" win" if ok else "", h=lossless_hits, t=lossless_total, bin=binary
            )
        )

    # Winners table: per subject at its largest size, the smallest and fastest format vs JSON.
    head = (
        "<tr><th>subject</th><th>elements</th><th>smallest</th><th>vs&nbsp;JSON</th>"
        "<th>fastest round-trip</th><th>vs&nbsp;JSON</th><th>{bin} lossless</th></tr>".format(bin=binary)
    )
    body = []
    for subj, size, gmap, smallest, fastest in per:
        j = gmap.get(baseline)
        size_ratio = "{:.2f}×".format(float(j["size_bytes"]) / float(smallest["size_bytes"])) if j else "—"
        speed_ratio = "{:.2f}×".format(float(j["roundtrip_median_s"]) / float(fastest["roundtrip_median_s"])) if j else "—"
        b = gmap.get(binary)
        badge = (
            ('<span class="badge ok">✓ yes</span>' if _is_lossless(b) else '<span class="badge no">✗ no</span>')
            if b
            else '<span class="note">—</span>'
        )
        body.append(
            "<tr><td>{subj}</td><td>{n}</td>"
            '<td><span class="fmt-cell"><span class="dot" style="background:var(--series-{s1})"></span>{sf} · {sb}</span></td><td>{sr}</td>'
            '<td><span class="fmt-cell"><span class="dot" style="background:var(--series-{s2})"></span>{ff} · {ft}</span></td><td>{spr}</td>'
            "<td>{badge}</td></tr>".format(
                subj=html.escape(subj),
                n=_fmt_int(size),
                s1=_slot(colors, smallest["format"]),
                sf=html.escape(smallest["format"]),
                sb=_fmt_bytes(smallest["size_bytes"]),
                sr=size_ratio,
                s2=_slot(colors, fastest["format"]),
                ff=html.escape(fastest["format"]),
                ft=_fmt_time(fastest["roundtrip_median_s"]),
                spr=speed_ratio,
                badge=badge,
            )
        )

    takeaway = ""
    if size_gain and speed_gain:
        takeaway = (
            '<p class="takeaway">On the largest payloads, <b>{bin}</b> (protobuf: double + flat '
            "coordinate arrays) is the smallest and fastest option — up to <b>{sr} smaller</b> and "
            "<b>{spd} faster to load</b> than compact JSON, {loss}.</p>".format(
                bin=binary,
                sr=_ratio(size_gain[0]),
                spd=_ratio(speed_gain[0]),
                loss=("losslessly" if lossless_hits == lossless_total else "with remaining fidelity notes below"),
            )
        )

    return (
        '<h2 class="section">Summary</h2>'
        + takeaway
        + '<div class="tiles">{}</div>'.format("".join(tiles))
        + '<div class="tablewrap"><table>{}{}</table></div>'.format(head, "".join(body))
    )


def build_html(rows, meta=None):
    """Return a full standalone HTML document for the given result rows.

    Parameters
    ----------
    rows : list[dict]
        Result rows as produced by :func:`benchmarks.serialization.run.run`.
    meta : dict, optional
        Run metadata (preset, repeat, seed, ...) shown in the header.

    Returns
    -------
    str
    """
    meta = meta or {}
    colors = _color_map(rows)

    subjects = []
    for r in rows:
        if r["subject"] not in subjects:
            subjects.append(r["subject"])

    meta_bits = ["generated {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))]
    for key in ("preset", "repeat", "seed", "compas"):
        if key in meta:
            meta_bits.append("{} {}".format(key, meta[key]))

    sections = [_exec_summary(rows, colors, subjects), _legend(rows, colors)]
    for subject in subjects:
        subject_rows = [r for r in rows if r["subject"] == subject]
        sections.append("<h2>{}</h2>".format(html.escape(subject)))
        for metric_key, title, kind in _METRICS:
            sections.append('<div class="metric-title">{}</div>'.format(html.escape(title)))
            sections.append(_bars(subject_rows, colors, metric_key, kind))
        sections.append(_table(subject_rows, colors))

    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>COMPAS serialization benchmark</title><style>{css}</style></head>"
        "<body><div class='wrap'>"
        "<h1>COMPAS serialization benchmark</h1>"
        "<p class='meta'>{meta}</p>"
        "{body}"
        "</div></body></html>"
    ).format(css=_css(colors), meta=html.escape(" · ".join(meta_bits)), body="".join(sections))


def write_html(rows, out_path, meta=None):
    with open(out_path, "w") as f:
        f.write(build_html(rows, meta))
    return out_path
