"""Ghi Sprint 1 GIẢ LẬP lên Project #2 từ progress-data/sprint1.yaml, rồi sinh burndown + bảng cho progress-report.md.

Idempotent: chỉ ghi phần lệch —
  - item lá: Status = Status cuối sprint trong YAML; Done → đóng issue (kèm 1 bình luận ghi rõ giả lập), chưa Done mà đang đóng → mở lại;
  - issue cha / epic có con trong sprint: Status cộng dồn (sprint_sim.expected_parent_status), mọi lá Done thì đóng.
KHÔNG đụng trường SWP (SWP của issue đã đóng giữ nguyên). Mặc định ghi; --dry-run chỉ in kế hoạch.
Sau khi ghi: đọc lại Project → progress-data/burndown-sprint1.png, .csv và các bảng trong progress-report.md.

Chạy:  python tools/simulate-sprint.py [--dry-run]
"""
import sys

import sprint_report_render as rr
import sprint_sim as ss
from github_api import rest
from project_fields import F_STATUS

DATA_DIR = ss.SPRINT_PATH.parent
REPORT = DATA_DIR.parent / "progress-report.md"
MARKER = "<!-- sprint-sim: sprint1 -->"
CLOSE_NOTE = (f"{MARKER}\nĐóng theo kịch bản **Sprint 1 giả lập** (2026-11-02〜11-15) trong `progress-data/sprint1.yaml` — "
              "không phải tiến độ thật; bài thực hiện ngày 2026-10-30.")


def plan(ctx, sprint, sim):
    """[(số issue, Status mong muốn, việc với issue: 'close' | 'reopen' | None)] chỉ gồm item lệch."""
    leaves = ss.sprint_leaves(ctx, sprint["iteration"])
    if set(leaves) != set(sim):
        raise SystemExit(f"sprint1.yaml lệch Iteration trên Project: thiếu {sorted(set(leaves) - set(sim))}, "
                         f"thừa {sorted(set(sim) - set(leaves))}")
    for num, s in sim.items():
        if leaves[num]["id"] != s["id"]:
            raise SystemExit(f"#{num}: id trong YAML {s['id']} ≠ backlog {leaves[num]['id']}")
    want = {num: s["final"] for num, s in sim.items()}
    want.update(ss.expected_parent_status(ctx, sim))
    out = []
    for num, status in sorted(want.items()):
        have = ctx["board"][num]["values"].get(F_STATUS)
        state = ctx["issues"][num]["state"]
        action = "close" if status == "Done" and state == "OPEN" else (
            "reopen" if status != "Done" and state == "CLOSED" else None)
        if have != status or action:
            out.append((num, status, action))
    return out


def apply(ctx, steps):
    repo = ctx["meta"]["repo"]
    for num, status, action in steps:
        if ctx["board"][num]["values"].get(F_STATUS) != status:
            ctx["project"].update(ctx["board"][num]["item_id"], {F_STATUS: status})
        if action == "close":
            comments = rest("GET", f"repos/{repo}/issues/{num}/comments?per_page=100") or []
            if not any(MARKER in (c.get("body") or "") for c in comments):
                rest("POST", f"repos/{repo}/issues/{num}/comments", {"body": CLOSE_NOTE})
            rest("PATCH", f"repos/{repo}/issues/{num}", {"state": "closed", "state_reason": "completed"})
        elif action == "reopen":
            rest("PATCH", f"repos/{repo}/issues/{num}", {"state": "open"})
        print(f"  #{num} → {status}" + (f" ({action})" if action else ""))


def render(ctx, sprint, sim):
    """Đọc số liệu từ Project → ảnh, CSV, bảng trong progress-report.md."""
    blocks, leaves, rows = rr.build_blocks(ctx, sprint, sim)
    rr.render_chart(rows, DATA_DIR / "burndown-sprint1.png",
                    f"Burndown {sprint['iteration']} · {sprint['start']} – {sprint['end']} · SWP còn lại (GIẢ LẬP)")
    csv = ["day,ideal_swp_remaining,actual_swp_remaining,swp_done_that_day"]
    csv += [f"{d},{i:g},{a:g},{x:g}" for d, i, a, x in rows]
    (DATA_DIR / "burndown-sprint1.csv").write_text("\n".join(csv) + "\n", encoding="utf-8")
    text = REPORT.read_text(encoding="utf-8")
    REPORT.write_text(rr.fill_blocks(text, blocks), encoding="utf-8")
    print("\n\n".join(blocks.values()))


def main():
    dry = "--dry-run" in sys.argv
    sprint, sim = ss.load_sim()
    ctx = ss.read_board()
    steps = plan(ctx, sprint, sim)
    print(f"{'[dry-run] ' if dry else ''}{len(steps)} item cần ghi "
          f"({sum(a == 'close' for *_, a in steps)} đóng, {sum(a == 'reopen' for *_, a in steps)} mở lại)")
    if dry:
        for num, status, action in steps:
            print(f"  #{num} → {status}" + (f" ({action})" if action else ""))
        return
    apply(ctx, steps)
    if steps:
        ctx = ss.read_board()  # đọc lại sau khi ghi; bảng / ảnh chỉ dùng số liệu Project
        left = plan(ctx, sprint, sim)
        if left:
            raise SystemExit(f"Đọc lại còn {len(left)} item lệch: {left}")
    render(ctx, sprint, sim)


if __name__ == "__main__":
    main()
