"""Xuất báo cáo HTML tự chứa (không tải tài nguyên ngoài) từ swp-scores.yaml.

Chạy:  python render-swp-report.py --scores swp-report/swp-scores.yaml --out swp-report/swp-report-YYMMDD.html
"""
import argparse
from html import escape as e
from pathlib import Path

import yaml

from report_data import BUCKETS, DEVIATION_LIMIT, cross_check, distribution, final_swp
from swp_rubric import COMPLEXITY_SCALE, PROVISIONAL_NOTE, SCOPE_SCALE

CSS = """body{font-family:"Noto Sans JP","Hiragino Sans","Yu Gothic UI","Meiryo","Segoe UI",sans-serif;margin:0;
background:#f7f7f5;color:#1d1d1b;font-size:14px;line-height:1.5}main{max-width:1200px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:8px 0}h2{font-size:17px;margin:28px 0 8px;border-bottom:2px solid #d9d6cf;padding-bottom:4px}
.tam{background:#fff3cd;border:2px solid #c99700;padding:10px 14px;border-radius:6px;font-weight:600}
table{border-collapse:collapse;width:100%;background:#fff;margin:6px 0}th,td{border:1px solid #ddd;padding:4px 6px;
vertical-align:top;text-align:left}th{background:#efede8;position:sticky;top:0}td.n{text-align:right;white-space:nowrap}
.sample{background:#fff8e6}.flag{color:#a4161a;font-weight:600}.low{color:#a4161a}.mid{color:#8a6d00}.high{color:#2b7a3d}
.bar{display:inline-block;height:10px;background:#5b7db1;vertical-align:middle;margin-right:4px}
.wrap{overflow-x:auto}input{padding:6px;width:320px;max-width:100%}.muted{color:#666;font-size:12px}
.samplebox{border:2px solid #c99700;background:#fffdf5;padding:8px;border-radius:6px}"""
JS = """function f(q){q=q.toLowerCase();document.querySelectorAll('#all tbody tr').forEach(function(r){
r.style.display=r.textContent.toLowerCase().indexOf(q)>-1?'':'none'})}"""
CONF_CLASS = {"thấp": "low", "vừa": "mid", "cao": "high"}


def link(r):
    return f'<a href="{e(r["url"])}">#{r["number"]}</a>'


def scale_table():
    rows = "".join(f"<tr><td class=n>{k}</td><td>{e(SCOPE_SCALE[k])}</td><td>{e(COMPLEXITY_SCALE[k])}</td></tr>"
                   for k in range(1, 6))
    return f"<table><tr><th>Điểm</th><th>Scope</th><th>Complexity</th></tr>{rows}</table>"


def dist_table(dist):
    head = "".join(f"<th>SWP {lo}–{hi}</th>" for lo, hi in BUCKETS)
    peak = max(st["swp"] for label, st in dist if label != "Tổng") or 1
    body = ""
    for label, st in dist:
        bar = "" if label == "Tổng" else f'<span class=bar style="width:{120 * st["swp"] / peak:.0f}px"></span>'
        cells = "".join(f"<td class=n>{b}</td>" for b in st["buckets"])
        body += (f"<tr><td>{e(label)}</td><td class=n>{st['count']}</td><td>{bar}{st['swp']:g}</td>"
                 f"<td class=n>{st['mean']:.1f}</td>{cells}<td class=n>{st['low_conf']}</td></tr>")
    return (f"<table><tr><th>Epic</th><th>Item lá</th><th>Tổng SWP</th><th>SWP TB</th>{head}"
            f"<th>Độ tin cậy thấp</th></tr>{body}</table>")


def item_cells(r):
    conf = f'<span class={CONF_CLASS[r["confidence"]]}>{e(r["confidence"])}</span>'
    if r.get("confidence_note"):
        conf += f'<div class=muted>{e(r["confidence_note"])}</div>'
    return (f"<td>{link(r)}</td><td>{e(r['epic'])}</td><td>{e(r['title'])}</td><td>{e(r['kind'])}</td>"
            f"<td class=n>{r['scope']}</td><td class=n>{r['complexity']}</td><td class=n><b>{r['swp']}</b></td>"
            f"<td>{e(r['reason_scope'])}<br>{e(r['reason_complexity'])}</td><td>{conf}</td>")


ITEM_HEAD = ("<th>Issue</th><th>Epic</th><th>Tiêu đề</th><th>Loại</th><th>Scope</th><th>Cx</th><th>SWP</th>"
             "<th>Lý do (Scope / Complexity)</th><th>Độ tin cậy</th>")


def sample_table(rows):
    body = "".join(f"<tr class=sample>{item_cells(r)}<td>{'<br>'.join(e(x) for x in r['sample_reasons'])}</td>"
                   f"<td>{e(str(r['pl_final'] or ''))}</td><td>{e(r['pl_reason'] or '')}</td></tr>" for r in rows)
    return (f"<div class='wrap samplebox'><table><tr>{ITEM_HEAD}<th>Lý do chọn mẫu</th><th>PL chốt</th>"
            f"<th>Lý do PL</th></tr>{body}</table></div>")


def cross_tables(epics, flagged, total):
    body = "".join(f"<tr><td>{e(x['epic'])}</td><td class=n>{x['hours']:g}</td><td class=n>{x['swp']:g}</td>"
                   f"<td class=n>{x['h_per_swp']:.2f}</td><td class='n{' flag' if x['flag'] else ''}'>"
                   f"{x['deviation']:+.0%}</td></tr>" for x in epics)
    t1 = (f"<table><tr><th>Epic</th><th>Giờ (lá)</th><th>SWP</th><th>Giờ / SWP</th><th>Lệch so với chung "
          f"({total['h_per_swp']:.2f})</th></tr>{body}</table>")
    body = "".join(f"<tr><td>{link(r)}</td><td>{e(r['epic'])}</td><td>{e(r['title'])}</td><td class=n>"
                   f"{float(r['hours_ref']):g}</td><td class=n>{final_swp(r)}</td><td class=n>{r['ratio']:.2f}</td>"
                   f"<td class=n>{r['epic_ratio']:.2f}</td><td class='n flag'>{r['deviation']:+.0%}</td></tr>"
                   for r in flagged)
    t2 = (f"<div class=wrap><table><tr><th>Issue</th><th>Epic</th><th>Tiêu đề</th><th>Giờ</th><th>SWP</th>"
          f"<th>Giờ / SWP</th><th>TB epic</th><th>Lệch</th></tr>{body}</table></div>")
    return t1, t2


def render(data):
    meta, rows = data["meta"], data["items"]
    samples = [r for r in rows if r["sample"]]
    dist = distribution(rows)
    epics, flagged, total = cross_check(rows)
    t_epic, t_items = cross_tables(epics, flagged, total)
    all_rows = "".join(f"<tr{' class=sample' if r['sample'] else ''}>{item_cells(r)}</tr>" for r in rows)
    lim = f"±{DEVIATION_LIMIT:.0%}"
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>SWP tạm — báo cáo chấm</title>
<style>{CSS}</style></head><body><main>
<h1>Báo cáo chấm SWP tạm — {e(meta['repo'])} · Project {e(meta['project'])}</h1>
<p class=tam>「{e(PROVISIONAL_NOTE)}」</p>
<p class=muted>Tạo lúc {e(meta['generated_at'])} (UTC) từ ảnh chụp {e(meta['snapshot_fetched_at'])} · seed chọn mẫu
{meta['seed']} · {meta['leaf_count']} item lá · {meta['sample_count']} mẫu. Trạng thái: {e(meta.get('status', ''))}.</p>
<h2>1. Thang điểm và công thức</h2>
<p><b>{e(meta['formula'])}</b>. Chấm item lá theo <b>mô tả issue</b> (tiêu đề, loại, mô tả, tiêu chí xong; issue con không
có mô tả thì dùng mô tả issue cha làm ngữ cảnh); <b>không</b> dựa vào số giờ đã ước. Issue cha và epic không chấm riêng.</p>
{scale_table()}
<h2>2. Mẫu cần PL kiểm ({len(samples)} item)</h2>
<p>PL điền <code>pl_final</code> và <code>pl_reason</code> trong <code>swp-scores.yaml</code>. Chỉ ghi lên Project khi mọi mẫu
đã có quyết định.</p>{sample_table(samples)}
<h2>3. Phân bố SWP theo epic</h2>{dist_table(dist)}
<h2>4. Kiểm tra chéo giờ / SWP (lệch &gt; {lim} → rà lại)</h2>
<p>Theo epic, so với tỉ lệ chung:</p>{t_epic}
<p>Item lá lệch quá {lim} so với tỉ lệ giờ / SWP của epic chứa nó: <b>{len(flagged)}</b> item. Giờ chỉ dùng ở mục này.</p>
{t_items}
<h2>5. Mọi item lá ({len(rows)})</h2>
<p><input placeholder="Lọc theo số issue, epic, tiêu đề, độ tin cậy…" oninput="f(this.value)"></p>
<div class=wrap><table id=all><thead><tr>{ITEM_HEAD}</tr></thead><tbody>{all_rows}</tbody></table></div>
</main><script>{JS}</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = yaml.safe_load(Path(a.scores).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    print(f"Báo cáo → {a.out}")


if __name__ == "__main__":
    main()
