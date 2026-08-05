"""Render benchmark result rows as HTML or a GitHub job summary.

The CSV is the machine record; this is the human view. One standalone ``.html`` file
(no external assets, theme-aware) with, per subject: grouped bars comparing formats at
each size on the metrics that matter (round-trip time and wire size), plus a full table.

The Markdown summary contains the executive view for CI, where GitHub does not render
standalone HTML reports directly on a workflow run's summary page.

New formats (protobuf, Arrow, ...) need no changes here: colors are assigned to formats
in first-appearance order from a validated categorical palette, so the report grows with
the harness.
"""

import argparse
import csv
import datetime
import html
import json
import statistics

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

# Client-side filter + summary re-render. __SLOTS__ is replaced with a {format: seriesSlot} map.
_FILTER_JS = """
var SLOT = __SLOTS__;
var ROWS = JSON.parse(document.getElementById('rows-data').textContent);
function isCompressed(f){ return f.indexOf('zip') >= 0 || f.indexOf('zstd') >= 0; }
function inGroup(f, g){ return g === 'all' || (g === 'compressed') === isCompressed(f); }
function isPb(f){ return f.indexOf('compas_pb') === 0; }
function fmtInt(n){ return (+n).toLocaleString('en-US'); }
function fmtBytes(n){ var u=['B','KB','MB','GB'],i=0; n=+n; while(n>=1024&&i<3){n/=1024;i++;} return n.toFixed(1)+' '+u[i]; }
function fmtTime(s){ s=+s; return s<1 ? (s*1000).toFixed(1)+' ms' : s.toFixed(3)+' s'; }
function ratio(x){ return x.toFixed(1)+'\\u00d7'; }
function dot(f){ return '<span class="dot" style="background:var(--series-'+(SLOT[f]||1)+')"></span>'; }
function median(a){ if(!a.length) return 0; var s=a.slice().sort(function(x,y){return x-y;}); var m=Math.floor(s.length/2); return s.length%2 ? s[m] : (s[m-1]+s[m])/2; }
function range(a){ return 'range '+Math.min.apply(null,a).toFixed(1)+'\\u2013'+Math.max.apply(null,a).toFixed(1)+'\\u00d7 across '+a.length+' subjects'; }
function currentGroup(){ var b=document.querySelector('.segmented button.active'); return b ? b.getAttribute('data-value') : 'all'; }
function minBy(a, f){ return a.reduce(function(x,y){return f(y)<f(x)?y:x;}); }
function tile(big, cls, lbl, sub){ return '<div class="tile"><div class="big'+cls+'">'+big+'</div><div class="lbl">'+lbl+'</div><div class="sub">'+sub+'</div></div>'; }
function factor(r, better, worse){ return r>=1 ? ratio(r)+' '+better : ratio(1/r)+' '+worse; }

function renderSummary(rows){
  var subjects=[]; rows.forEach(function(r){ if(subjects.indexOf(r.subject)<0) subjects.push(r.subject); });
  var baseName = rows.some(function(r){return r.format==='json';}) ? 'json'
               : (rows.some(function(r){return r.format==='json_zip';}) ? 'json_zip' : null);
  var baseLabel = baseName || 'baseline';
  var per = subjects.map(function(subj){
    var sr = rows.filter(function(r){return r.subject===subj;});
    var maxSize = Math.max.apply(null, sr.map(function(r){return r.size;}));
    return { subj: subj, size: maxSize, group: sr.filter(function(r){return r.size===maxSize;}) };
  });
  var sizeRatios=[], speedRatios=[], smallWins=0, fastWins=0, winTot=0;
  per.forEach(function(p){
    var base = p.group.filter(function(r){return r.format===baseName;})[0];
    var pbs = p.group.filter(function(r){return isPb(r.format);});
    if(base && pbs.length){
      sizeRatios.push(base.size_bytes / minBy(pbs, function(r){return r.size_bytes;}).size_bytes);
      speedRatios.push(base.roundtrip / minBy(pbs, function(r){return r.roundtrip;}).roundtrip);
      winTot++;
      if(isPb(minBy(p.group, function(r){return r.size_bytes;}).format)) smallWins++;
      if(isPb(minBy(p.group, function(r){return r.roundtrip;}).format)) fastWins++;
    }
  });
  var tiles='';
  if(sizeRatios.length){ var ms=median(sizeRatios); tiles+=tile(factor(ms,'smaller','larger'), ms>=1?' win':'', 'median wire size vs '+baseLabel, range(sizeRatios)); }
  if(speedRatios.length){ var mt=median(speedRatios); tiles+=tile(factor(mt,'faster','slower'), mt>=1?' win':'', 'median round-trip vs '+baseLabel, range(speedRatios)); }
  if(winTot) tiles+=tile(smallWins+'/'+winTot, (smallWins===winTot?' win':''), 'subjects where compas_pb is smallest', 'and fastest to load on '+fastWins+'/'+winTot);
  var head='<tr><th>subject</th><th>elements</th><th>smallest</th><th>vs '+baseLabel
         +'</th><th>fastest round-trip</th><th>vs '+baseLabel+'</th><th>lossless</th></tr>';
  var body='';
  per.forEach(function(p){
    if(!p.group.length) return;
    var base = p.group.filter(function(r){return r.format===baseName;})[0];
    var smallest = minBy(p.group, function(r){return r.size_bytes;});
    var fastest = minBy(p.group, function(r){return r.roundtrip;});
    var sr = base ? (base.size_bytes/smallest.size_bytes).toFixed(2)+'\\u00d7' : '\\u2014';
    var spr = base ? (base.roundtrip/fastest.roundtrip).toFixed(2)+'\\u00d7' : '\\u2014';
    var pb = p.group.filter(function(r){return isPb(r.format);})[0];
    var badge = pb ? (pb.lossless ? '<span class="badge ok">\\u2713 yes</span>' : '<span class="badge no">\\u2717 no</span>') : '<span class="note">\\u2014</span>';
    body+='<tr><td>'+p.subj+'</td><td>'+fmtInt(p.size)+'</td>'
        +'<td><span class="fmt-cell">'+dot(smallest.format)+smallest.format+' \\u00b7 '+fmtBytes(smallest.size_bytes)+'</span></td><td>'+sr+'</td>'
        +'<td><span class="fmt-cell">'+dot(fastest.format)+fastest.format+' \\u00b7 '+fmtTime(fastest.roundtrip)+'</span></td><td>'+spr+'</td>'
        +'<td>'+badge+'</td></tr>';
  });
  return '<h2 class="section">Summary</h2><div class="tiles">'+tiles+'</div><div class="tablewrap"><table>'+head+body+'</table></div>';
}

function applyFilter(){
  var g = currentGroup();
  document.querySelectorAll('[data-format]').forEach(function(el){
    el.style.display = inGroup(el.getAttribute('data-format'), g) ? '' : 'none';
  });
  document.querySelectorAll('.sizegroup').forEach(function(sg){
    var fills = [].slice.call(sg.querySelectorAll('.bar-row')).filter(function(r){return r.style.display!=='none';})
                  .map(function(r){return r.querySelector('.fill');});
    var max = Math.max.apply(null, fills.map(function(f){return parseFloat(f.dataset.value);}).concat([0]));
    fills.forEach(function(f){ f.style.width = max>0 ? (parseFloat(f.dataset.value)/max*100).toFixed(1)+'%' : '0%'; });
  });
  document.getElementById('summary-body').innerHTML = renderSummary(ROWS.filter(function(r){return inGroup(r.format, g);}));
}
document.querySelectorAll('.segmented button').forEach(function(b){
  b.addEventListener('click', function(){
    document.querySelectorAll('.segmented button').forEach(function(x){ x.classList.remove('active'); });
    b.classList.add('active');
    applyFilter();
  });
});
applyFilter();
"""


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
.controls { margin: 14px 0 4px; display: flex; align-items: center; gap: 12px; }
.controls-label { font-size: 13px; color: var(--text-secondary); }
.segmented { display: inline-flex; background: var(--track); border: 1px solid var(--border);
  border-radius: 9px; padding: 2px; gap: 2px; }
.segmented button { font: inherit; font-size: 13px; color: var(--text-secondary); cursor: pointer;
  background: transparent; border: 0; border-radius: 7px; padding: 5px 14px; line-height: 1.4; }
.segmented button:hover { color: var(--text-primary); }
.segmented button.active { background: var(--surface); color: var(--text-primary); font-weight: 600;
  box-shadow: 0 1px 2px rgba(0,0,0,0.10); }
.tile .rng { font-size: 11px; color: var(--muted); margin-top: 2px; font-variant-numeric: tabular-nums; }
.coverage { margin: 18px 0 0; font-size: 13px; color: var(--text-secondary);
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px; }
.coverage b { color: var(--text-primary); font-weight: 650; }
.coverage .miss { color: var(--muted); font-size: 12px; }
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
            '<span class="chip" data-format="{fmt}"><span class="dot" style="background:var(--series-{slot})"></span>'
            "<b>{fmt}</b> · {note}</span>".format(
                slot=slot, fmt=html.escape(r["format"]), note=html.escape(r.get("note", ""))
            )
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
                '<div class="bar-row" data-format="{name}">'
                '<div class="bar-name">{name}</div>'
                '<div class="track"><div class="fill" style="width:{w:.1f}%;background:var(--series-{s})" data-value="{dv}"></div></div>'
                '<div class="bar-val">{val}</div>'
                "</div>".format(
                    name=html.escape(r["format"]),
                    w=width,
                    s=slot,
                    dv=float(r[metric_key]),
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
            '<tr data-format="{fmt}">'
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


def _coverage_banner(coverage):
    """Static banner: how many of compas_pb's serializable types the corpus benchmarks."""
    if not coverage:
        return ""
    n, total = coverage["benchmarked"], coverage["serializable"]
    missing = coverage.get("missing") or []
    if missing:
        tail = ' <span class="miss">not yet covered: {}</span>'.format(html.escape(", ".join(missing)))
    else:
        tail = " — full coverage."
    return '<div class="coverage"><b>{}/{}</b> of compas_pb\'s serializable types are benchmarked.{}</div>'.format(
        n, total, tail
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

    controls = (
        '<div class="controls"><span class="controls-label">Show formats</span>'
        '<div class="segmented" id="fmtfilter" role="tablist">'
        '<button type="button" data-value="uncompressed" role="tab">Uncompressed</button>'
        '<button type="button" data-value="compressed" role="tab">Compressed</button>'
        '<button type="button" data-value="all" class="active" role="tab">All</button>'
        "</div></div>"
    )
    sections = [
        controls,
        _coverage_banner(meta.get("coverage")),
        '<div id="summary-body"></div>',
        _legend(rows, colors),
    ]
    for subject in subjects:
        subject_rows = [r for r in rows if r["subject"] == subject]
        sections.append("<h2>{}</h2>".format(html.escape(subject)))
        for metric_key, title, kind in _METRICS:
            sections.append('<div class="metric-title">{}</div>'.format(html.escape(title)))
            sections.append(_bars(subject_rows, colors, metric_key, kind))
        sections.append(_table(subject_rows, colors))

    data_rows = [
        {
            "subject": r["subject"],
            "size": int(r["size"]),
            "format": r["format"],
            "size_bytes": int(r["size_bytes"]),
            "roundtrip": float(r["roundtrip_median_s"]),
            "lossless": str(r["lossless"]).lower() in ("true", "1"),
        }
        for r in rows
    ]
    slot_map = {r["format"]: _slot(colors, r["format"]) for r in rows}
    script = (
        '<script id="rows-data" type="application/json">{data}</script>'
        "<script>{js}</script>"
    ).format(data=json.dumps(data_rows), js=_FILTER_JS.replace("__SLOTS__", json.dumps(slot_map)))

    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>COMPAS serialization benchmark</title><style>{css}</style></head>"
        "<body><div class='wrap'>"
        "<h1>COMPAS serialization benchmark</h1>"
        "<p class='meta'>{meta}</p>"
        "{body}{script}"
        "</div></body></html>"
    ).format(
        css=_css(colors),
        meta=html.escape(" · ".join(meta_bits)),
        body="".join(sections),
        script=script,
    )


def write_html(rows, out_path, meta=None):
    with open(out_path, "w") as f:
        f.write(build_html(rows, meta))
    return out_path


def _is_lossless(value):
    return str(value).lower() in ("true", "1")


def _comparison(base, result, kind):
    """Describe how a smaller/faster result compares with its baseline."""
    base = float(base)
    result = float(result)
    if not base or not result:
        return "—"
    ratio = base / result
    if 0.995 <= ratio <= 1.005:
        return "the same"
    if ratio > 1:
        return "{:.2f}× {}".format(ratio, "smaller" if kind == "size" else "faster")
    return "{:.2f}× {}".format(1.0 / ratio, "larger" if kind == "size" else "slower")


def _markdown_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_markdown_summary(rows, artifact_url=None):
    """Return the largest-size executive summary as GitHub-flavored Markdown."""
    subjects = []
    for row in rows:
        if row["subject"] not in subjects:
            subjects.append(row["subject"])

    groups = []
    for subject in subjects:
        subject_rows = [row for row in rows if row["subject"] == subject]
        largest_size = max(int(row["size"]) for row in subject_rows)
        groups.append((subject, largest_size, [row for row in subject_rows if int(row["size"]) == largest_size]))

    baseline_name = None
    formats = {row["format"] for row in rows}
    if "json" in formats:
        baseline_name = "json"
    elif "json_zip" in formats:
        baseline_name = "json_zip"

    size_ratios = []
    time_ratios = []
    smallest_wins = 0
    fastest_wins = 0
    compared = 0
    table_rows = []
    for subject, largest_size, group in groups:
        smallest = min(group, key=lambda row: float(row["size_bytes"]))
        fastest = min(group, key=lambda row: float(row["roundtrip_median_s"]))
        baseline = next((row for row in group if row["format"] == baseline_name), None)
        protobuf_rows = [row for row in group if row["format"].startswith("compas_pb")]

        size_comparison = "—"
        time_comparison = "—"
        if baseline:
            size_comparison = _comparison(baseline["size_bytes"], smallest["size_bytes"], "size")
            time_comparison = _comparison(baseline["roundtrip_median_s"], fastest["roundtrip_median_s"], "time")
        if baseline and protobuf_rows:
            best_protobuf_size = min(float(row["size_bytes"]) for row in protobuf_rows)
            best_protobuf_time = min(float(row["roundtrip_median_s"]) for row in protobuf_rows)
            size_ratios.append(float(baseline["size_bytes"]) / best_protobuf_size)
            time_ratios.append(float(baseline["roundtrip_median_s"]) / best_protobuf_time)
            compared += 1
            smallest_wins += smallest["format"].startswith("compas_pb")
            fastest_wins += fastest["format"].startswith("compas_pb")

        if protobuf_rows:
            protobuf_lossless = "✅ yes" if all(_is_lossless(row["lossless"]) for row in protobuf_rows) else "❌ no"
        else:
            protobuf_lossless = "—"

        table_rows.append(
            "| {} | {} | `{}` · {} | {} | `{}` · {} | {} | {} |".format(
                _markdown_cell(subject),
                _fmt_int(largest_size),
                _markdown_cell(smallest["format"]),
                _fmt_bytes(smallest["size_bytes"]),
                size_comparison,
                _markdown_cell(fastest["format"]),
                _fmt_time(fastest["roundtrip_median_s"]),
                time_comparison,
                protobuf_lossless,
            )
        )

    lines = ["## Serialization benchmark", ""]
    if artifact_url:
        lines.extend(["[Download the full interactive HTML report, CSV, and encoded samples]({})".format(artifact_url), ""])
    if compared:
        lines.extend(
            [
                "At the largest measured size for each subject, relative to `{}`, the best `compas_pb` variant is typically **{}** in wire size and **{}** in round-trip time. "
                "A `compas_pb` variant is smallest for **{}/{}** subjects and fastest for **{}/{}**.".format(
                    baseline_name,
                    _comparison(1.0, 1.0 / statistics.median(size_ratios), "size"),
                    _comparison(1.0, 1.0 / statistics.median(time_ratios), "time"),
                    smallest_wins,
                    compared,
                    fastest_wins,
                    compared,
                ),
                "",
            ]
        )

    baseline_label = baseline_name or "baseline"
    lines.extend(
        [
            "| Subject | Elements | Smallest | vs {} | Fastest round-trip | vs {} | `compas_pb` lossless |".format(baseline_label, baseline_label),
            "|:--|--:|:--|:--|:--|:--|:--|",
        ]
    )
    lines.extend(table_rows)
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Render a benchmark CSV as a GitHub job summary.")
    parser.add_argument("csv_path", help="Benchmark CSV to summarize")
    parser.add_argument("--artifact-url", help="URL for the complete downloadable artifact")
    args = parser.parse_args()

    with open(args.csv_path, newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    print(build_markdown_summary(rows, artifact_url=args.artifact_url))


if __name__ == "__main__":
    main()
