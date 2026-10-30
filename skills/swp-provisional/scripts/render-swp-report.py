"""Xuất báo cáo HTML tự chứa (không tải tài nguyên ngoài) từ swp-scores.yaml.

Chạy:  python render-swp-report.py --scores swp-report/swp-scores.yaml --out swp-report/swp-report-YYMMDD[-final].html
       [--notes swp-report/cross-check-notes.yaml]   # giải thích kiểm chéo theo epic do PL / người chấm viết
"""
import argparse
from html import escape as e
from pathlib import Path

import yaml

from report_data import BUCKETS, DEVIATION_LIMIT, cross_check, distribution, draft_swp, final_swp
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
.samplebox{border:2px solid #c99700;background:#fffdf5;padding:8px;border-radius:6px}.chg{background:#e8f1fb}"""
JS = """function f(q){q=q.toLowerCase();document.querySelectorAll('#all tbody tr').forEach(function(r){
r.style.display=r.textContent.toLowerCase().indexOf(q)>-1?'':'none'})}"""
CONF_CLASS = {"thấp": "low", "vừa": "mid", "cao": "high"}
EFFECT_LABEL = {"R1": "R1", "R2": "R2", "R3": "R3", "pl_samples": "PL chốt mẫu (skill chấm lại → Bạn chốt)",
                "total": "Tổng mọi item lá"}


def link(r):
    return f'<a href="{e(r["url"])}">#{r["number"]}</a>'


def axes(s, c, v):
    return f"{s} × {c} → <b>{v}</b>" if s is not None else f"<b>{v}</b>"


def scale_table():
    rows = "".join(f"<tr><td class=n>{k}</td><td>{e(SCOPE_SCALE[k])}</td><td>{e(COMPLEXITY_SCALE[k])}</td></tr>"
                   for k in range(1, 6))
    return f"<table><tr><th>Điểm</th><th>Scope</th><th>Complexity</th></tr>{rows}</table>"


def rules_section(meta):
    rules, eff = meta.get("pl_rules"), meta.get("rule_effects")
    if not rules or not eff:
        return "<p>Chưa có quy tắc PL bổ sung.</p>"
    body = ""
    for key, st in eff.items():
        text = e(rules[key]) if key in rules else ""
        body += (f"<tr><td><b>{e(EFFECT_LABEL.get(key, key))}</b></td><td>{text}</td><td class=n>{st['items']}</td>"
                 f"<td class=n>{st['changed']}</td><td class=n>{st['swp_before']:,}</td><td class=n>{st['swp_after']:,}"
                 f"</td><td class=n>{st['swp_after'] - st['swp_before']:+,}</td></tr>")
    return (f"<p>PL sửa thang điểm ngày <b>{e(str(rules['date']))}</b> sau khi review mẫu; áp cho <b>mọi</b> item cùng loại "
            f"(không chỉ mẫu), chấm lại toàn bộ. Dòng Rx: bản nháp → skill chấm lại theo quy tắc; dòng PL: skill chấm lại → giá trị "
            f"PL chốt; dòng tổng: bản nháp → giá trị ghi lên Project.</p>"
            f"<table><tr><th>Quy tắc</th><th>Nội dung</th><th>Item áp</th><th>Item đổi SWP</th><th>SWP trước</th>"
            f"<th>SWP sau</th><th>Chênh</th></tr>{body}</table>")


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
    fin, chg = final_swp(r), " chg" if final_swp(r) != draft_swp(r) else ""
    return (f"<td>{link(r)}</td><td>{e(r['epic'])}</td><td>{e(r['title'])}</td><td>{e(r['kind'])}</td>"
            f"<td class=n>{r['scope']}</td><td class=n>{r['complexity']}</td><td class=n>{r['swp']}</td>"
            f"<td class=n>{draft_swp(r)}</td><td class='n{chg}'><b>{fin}</b></td><td>{e(' '.join(r.get('rules') or []))}"
            f"</td><td>{e(r['reason_scope'])}<br>{e(r['reason_complexity'])}</td><td>{conf}</td>")


ITEM_HEAD = ("<th>Issue</th><th>Epic</th><th>Tiêu đề</th><th>Loại</th><th>Scope</th><th>Cx</th><th>SWP skill</th>"
             "<th>Nháp</th><th>Chốt</th><th>Quy tắc</th><th>Lý do (Scope / Complexity)</th><th>Độ tin cậy</th>")


def sample_table(rows):
    body = "".join(
        f"<tr class=sample><td>{link(r)}</td><td>{e(r['epic'])}</td><td>{e(r['title'])}</td>"
        f"<td class=n>{axes(r.get('scope_draft'), r.get('complexity_draft'), draft_swp(r))}</td>"
        f"<td class=n>{axes(r['scope'], r['complexity'], r['swp'])}<div class=muted>{e(' '.join(r.get('rules') or []))}"
        f"</div></td><td class=n>{axes(r.get('pl_scope'), r.get('pl_complexity'), r.get('pl_final') or '—')}</td>"
        f"<td>{e(r.get('pl_reason') or '')}</td><td class=muted>{'<br>'.join(e(x) for x in r['sample_reasons'])}</td>"
        f"</tr>" for r in rows)
    return (f"<div class='wrap samplebox'><table><tr><th>Issue</th><th>Epic</th><th>Tiêu đề</th><th>Skill chấm (nháp)"
            f"<br>Scope × Cx → SWP</th><th>Skill chấm lại<br>(R1–R3)</th><th>Bạn chốt</th><th>Lý do</th>"
            f"<th>Lý do chọn mẫu</th></tr>{body}</table></div>")


def cross_tables(rows, notes):
    epics, flagged, total = cross_check(rows)
    draft = {x["epic"]: x for x in cross_check([{**r, "pl_final": None, "swp": draft_swp(r)} for r in rows])[0]}
    body = "".join(f"<tr><td>{e(x['epic'])}</td><td class=n>{x['hours']:g}</td><td class=n>{x['swp']:g}</td>"
                   f"<td class=n>{x['h_per_swp']:.2f}</td><td class='n{' flag' if draft[x['epic']]['flag'] else ''}'>"
                   f"{draft[x['epic']]['deviation']:+.0%}</td><td class='n{' flag' if x['flag'] else ''}'>"
                   f"{x['deviation']:+.0%}</td><td>{e(notes.get(x['epic'], ''))}</td></tr>" for x in epics)
    t1 = (f"<table><tr><th>Epic</th><th>Giờ (lá)</th><th>SWP</th><th>Giờ / SWP</th><th>Lệch (nháp)</th><th>Lệch so với "
          f"chung ({total['h_per_swp']:.2f})</th><th>Giải thích</th></tr>{body}</table>")
    over = [f"{x['epic']} {x['deviation']:+.0%}" for x in epics if x["flag"]]
    was = [f"{k} {v['deviation']:+.0%}" for k, v in draft.items() if v["flag"]]
    verdict = (f"Epic còn lệch quá ±{DEVIATION_LIMIT:.0%}: <b>{e(', '.join(over))}</b>." if over else
               f"<b>Không epic nào lệch quá ±{DEVIATION_LIMIT:.0%}</b> sau review"
               + (f" (bản nháp: {e(', '.join(was))})." if was else "."))
    body = "".join(f"<tr><td>{link(r)}</td><td>{e(r['epic'])}</td><td>{e(r['title'])}</td><td class=n>"
                   f"{float(r['hours_ref']):g}</td><td class=n>{final_swp(r)}</td><td class=n>{r['ratio']:.2f}</td>"
                   f"<td class=n>{r['epic_ratio']:.2f}</td><td class='n flag'>{r['deviation']:+.0%}</td></tr>"
                   for r in flagged)
    t2 = (f"<div class=wrap><table><tr><th>Issue</th><th>Epic</th><th>Tiêu đề</th><th>Giờ</th><th>SWP</th>"
          f"<th>Giờ / SWP</th><th>TB epic</th><th>Lệch</th></tr>{body}</table></div>")
    return t1, verdict, t2, len(flagged)


def render(data, notes):
    meta, rows = data["meta"], data["items"]
    samples = [r for r in rows if r["sample"]]
    t_epic, verdict, t_items, n_flag = cross_tables(rows, notes)
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
<h2>2. Quy tắc PL bổ sung R1–R3</h2>{rules_section(meta)}
<h2>3. Mẫu PL đã kiểm ({len(samples)} item)</h2>
<p>Giá trị ghi lên Project của mẫu = <b>Bạn chốt</b> (<code>pl_final</code>); item khác = skill chấm lại theo R1–R3.</p>
{sample_table(samples)}
<h2>4. Phân bố SWP theo epic (giá trị chốt)</h2>{dist_table(distribution(rows))}
<h2>5. Kiểm tra chéo giờ / SWP (lệch &gt; {lim} → rà lại)</h2>
<p>Theo epic, so với tỉ lệ chung. {verdict}</p>{t_epic}
<p>Item lá lệch quá {lim} so với tỉ lệ giờ / SWP của epic chứa nó: <b>{n_flag}</b> item. Giờ chỉ dùng ở mục này.</p>
{t_items}
<h2>6. Mọi item lá ({len(rows)})</h2>
<p><input placeholder="Lọc theo số issue, epic, tiêu đề, quy tắc, độ tin cậy…" oninput="f(this.value)">
<span class=muted>Ô «Chốt» tô xanh = khác bản nháp.</span></p>
<div class=wrap><table id=all><thead><tr>{ITEM_HEAD}</tr></thead><tbody>{all_rows}</tbody></table></div>
</main><script>{JS}</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--notes", help="YAML {epic: giải thích} cho bảng kiểm chéo theo epic")
    a = ap.parse_args()
    data = yaml.safe_load(Path(a.scores).read_text(encoding="utf-8"))
    notes = yaml.safe_load(Path(a.notes).read_text(encoding="utf-8")) or {} if a.notes else {}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data, notes), encoding="utf-8")
    print(f"Báo cáo → {a.out}")


if __name__ == "__main__":
    main()
