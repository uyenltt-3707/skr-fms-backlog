"""Sinh bảng Markdown + ảnh burndown cho progress-report.md từ số liệu đọc ở Project (sprint_sim.py).

Bảng được ghi vào progress-report.md giữa hai marker `<!-- sprint-sim:KEY -->` … `<!-- /sprint-sim:KEY -->`
để không gõ tay số liệu. Ảnh: matplotlib (backend Agg, không cần màn hình).
"""
import re

import sprint_sim as ss
from sprint_sim import STATUSES

ACTUAL, IDEAL, INK, MUTED, GRID, SURFACE = "#2a78d6", "#898781", "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"


def _n(x):
    return f"{x:,.1f}".rstrip("0").rstrip(".")


def status_table_md(table, leaves):
    """Bảng §2: Trạng thái · Số issue · Tổng SWP · Ghi chú (Ghi chú: số issue thuộc trạng thái, Done = đã đóng)."""
    lines = ["| Trạng thái | Số issue | Tổng SWP | Ghi chú |", "|---|---|---|---|"]
    for s in STATUSES:
        count, swp, hours = table[s]
        nums = sorted(n for n, lf in leaves.items() if lf["status"] == s)
        if s == "Done":
            closed = sum(leaves[n]["state"] == "CLOSED" for n in nums)
            note = f"{_n(hours)}h · issue đã đóng {closed} / {count}"
        else:
            note = f"{_n(hours)}h · carry-over: " + ", ".join(f"#{n}" for n in nums) if nums else "—"
        lines.append(f"| {s} | {count} | {_n(swp)} | {note} |")
    total = [sum(table[s][k] for s in STATUSES) for k in range(3)]
    done = table["Done"]
    lines.append(f"| **Tổng Sprint 1** | **{total[0]}** | **{_n(total[1])}** | {_n(total[2])}h · hoàn thành "
                 f"{done[0]} / {total[0]} item ({done[0] / total[0]:.0%}), {_n(done[1])} / {_n(total[1])} SWP "
                 f"({done[1] / total[1]:.1%}) |")
    return "\n".join(lines)


def owner_table_md(leaves):
    """Bảng phụ §2: theo 担当(仮) — giờ kế hoạch / Done / còn lại (trường 見積時間 trên Project), item chưa Done."""
    lines = ["| 担当(仮) | Giờ kế hoạch | Giờ Done | Tỷ lệ Done | Item chưa Done |", "|---|---|---|---|---|"]
    for who in sorted({lf["owner"] for lf in leaves.values()}):
        mine = {n: lf for n, lf in leaves.items() if lf["owner"] == who}
        plan = sum(lf["hours"] for lf in mine.values())
        done = sum(lf["hours"] for lf in mine.values() if lf["status"] == "Done")
        rest = ", ".join(f"#{n} ({mine[n]['status']})" for n in sorted(mine) if mine[n]["status"] != "Done") or "—"
        lines.append(f"| {who} | {_n(plan)} | {_n(done)} | {done / plan:.0%} | {rest} |")
    return "\n".join(lines)


def load_md(planned, added, capacity, name, added_label):
    """Bảng tải một sprint: giờ đã xếp (Iteration `name` trên Project) + giờ item thêm vào (`added`), so trần từng người.

    Dòng Tổng: "Vượt" = cộng phần vượt của từng người; "ròng" = tổng giờ − tổng trần (bù trừ cả người còn dư).
    """
    lines = [f"| 担当(仮) | {name}: đã xếp (h) | + {added_label} (h) | = Tổng (h) | Trần (h) | Vượt (h) |",
             "|---|---|---|---|---|---|"]
    tot_a = tot_b = tot_cap = over = 0.0
    for who, cap in capacity.items():
        a = sum(lf["hours"] for lf in planned.values() if lf["owner"] == who)
        b = sum(lf["hours"] for lf in added.values() if lf["owner"] == who)
        tot_a, tot_b, tot_cap, over = tot_a + a, tot_b + b, tot_cap + cap, over + max(0, a + b - cap)
        lines.append(f"| {who} | {_n(a)} | {_n(b)} | {_n(a + b)} | {_n(cap)} | {_n(a + b - cap) if a + b > cap else '—'} |")
    lines.append(f"| **Tổng** | {_n(tot_a)} | {_n(tot_b)} | **{_n(tot_a + tot_b)}** | {_n(tot_cap)} | "
                 f"{_n(over)} (ròng {_n(tot_a + tot_b - tot_cap):s}) |")
    return "\n".join(lines)


def burndown_table_md(rows):
    lines = ["| Ngày | Kế hoạch lý tưởng (SWP còn) | Thực tế giả lập (SWP còn) | Lệch | SWP xong trong ngày |",
             "|---|---|---|---|---|"]
    for day, ideal, actual, done in rows:
        lines.append(f"| {day} | {_n(ideal)} | {_n(actual)} | {actual - ideal:+.1f} | {_n(done)} |")
    return "\n".join(lines)


def render_chart(rows, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = ["Đầu"] + [d[5:].replace("-", "/") for d, *_ in rows[1:]]
    x = list(range(len(rows)))
    ideal, actual = [r[1] for r in rows], [r[2] for r in rows]
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.plot(x, ideal, color=IDEAL, lw=2, ls="--", label="Kế hoạch lý tưởng")
    ax.plot(x, actual, color=ACTUAL, lw=2, marker="o", ms=5, label="Thực tế (giả lập)")
    for i in (len(rows) - 1,):  # nhãn trực tiếp ở điểm cuối, không ghi số mọi điểm
        ax.annotate(f"còn {_n(actual[i])} SWP", (x[i], actual[i]), xytext=(-6, -16), textcoords="offset points",
                    ha="right", color=INK, fontsize=9)
    ax.set_xticks(x, labels, fontsize=8, color=MUTED)
    ax.tick_params(axis="y", colors=MUTED, labelsize=8)
    ax.set_ylim(0, max(ideal + actual) * 1.08)
    ax.set_ylabel("SWP còn lại", color=MUTED, fontsize=9)
    ax.grid(axis="y", color=GRID, lw=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.set_title(title, color=INK, fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9, labelcolor=MUTED)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def build_blocks(ctx, sprint, sim):
    """Mọi bảng của progress-report.md, tính từ Project: (blocks {KEY: markdown}, leaves, rows burndown)."""
    leaves = ss.sprint_leaves(ctx, sprint["iteration"])
    rows = ss.burndown(sprint, sim, leaves)
    s2, s3 = (ss.sprint_leaves(ctx, ctx["meta"]["sprints"][k]) for k in (2, 3))
    carry = {n: lf for n, lf in leaves.items() if lf["status"] != "Done"}
    pushed = {n: s2[n] for n in sprint.get("replan_push_to_sprint3", []) if n in s2}
    cap = ctx["meta"]["capacity"]
    blocks = {"status": status_table_md(ss.status_table(leaves), leaves), "owner": owner_table_md(leaves),
              "sprint2": load_md(s2, carry, cap, ctx["meta"]["sprints"][2], "carry-over Sprint 1"),
              "sprint3": load_md(s3, pushed, cap, ctx["meta"]["sprints"][3], "rút từ Sprint 2 (đề xuất)"),
              "burndown": burndown_table_md(rows)}
    return blocks, leaves, rows


def fill_blocks(text, blocks):
    """Thay nội dung giữa marker cho từng KEY; báo lỗi nếu thiếu marker."""
    for key, body in blocks.items():
        pat = re.compile(rf"(<!-- sprint-sim:{key} -->\n)(?:.*?\n)?(<!-- /sprint-sim:{key} -->)", re.S)
        if not pat.search(text):
            raise SystemExit(f"progress-report.md thiếu marker sprint-sim:{key}")
        text = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)
    return text
