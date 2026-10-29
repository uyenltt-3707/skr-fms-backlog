"""Đọc tools/backlog.yaml thành danh sách item phẳng (epic / issue / sub-issue) + tiện ích dùng chung.

Dùng bởi create-issues.py và check-backlog.py. Không gọi mạng ở module này.
"""
import sys
from pathlib import Path

import yaml

# Windows: stdout chuyển hướng (log, pipe) mặc định dùng code page ANSI → in tiếng Việt / Nhật bị lỗi.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

TOOLS_DIR = Path(__file__).resolve().parent
BACKLOG_PATH = TOOLS_DIR / "backlog.yaml"
MAP_PATH = TOOLS_DIR / "issue-map.json"
DEFAULT_CONSTRAINT = "なし"
ITEM_TYPE = {"epic": "Epic", "issue": "Issue", "sub": "Sub-issue"}
# Khóa hợp lệ của issue / sub-issue. Khóa lạ thường là dấu hiệu chuỗi chứa ", " không quote trong {...} bị YAML cắt.
KNOWN_KEYS = {"id", "title", "kind", "owner", "hours", "sprint", "done", "deps", "desc", "spec", "wu", "subs",
              "label", "constraint"}


class Item(dict):
    """Một node của cây backlog. Truy cập field bằng thuộc tính cho gọn."""

    __getattr__ = dict.get


def load(path=BACKLOG_PATH):
    """Trả về (meta, items theo thứ tự cây). Giờ / owner / sprint của cha được suy ra từ con."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    items = []
    for e in data["epics"]:
        constraint = e.get("constraint", DEFAULT_CONSTRAINT)
        epic = Item(id=e["id"], level="epic", parent=None, epic=e["id"], epic_name=e["name"],
                    title=f"[Epic] {e['id']} {e['name']}", kind="epic", owner="PM",
                    desc=e["desc"], done=None, wu=[], spec=[], deps=[], label=None,
                    constraint=constraint, children=[])
        items.append(epic)
        for i in e["issues"]:
            issue = _node(i, "issue", epic, constraint)
            epic.children.append(issue.id)
            items.append(issue)
            for s in i.get("subs", []):
                sub = _node(s, "sub", epic, constraint, parent=issue)
                issue.children.append(sub.id)
                items.append(sub)
    by_id = {it.id: it for it in items}
    _rollup(items, by_id)
    return data["meta"], items, by_id


def _node(raw, level, epic, constraint, parent=None):
    unknown = set(raw) - KNOWN_KEYS
    if unknown:
        raise ValueError(f"{raw.get('id')}: khóa lạ {sorted(unknown)} — quote chuỗi có dấu phẩy trong {{...}}")
    wu =raw.get("wu", []) if level == "issue" else parent.wu
    tag = wu[0] if wu else _bracket_tag(parent.raw_title if parent else raw["title"])
    raw_title = raw["title"]
    if level == "issue":
        title = f"[{wu[0]}] {raw_title}" if wu else raw_title
    else:
        title = f"[{tag}] {raw_title}" if tag else raw_title
    return Item(id=raw["id"], level=level, parent=parent.id if parent else epic.id, epic=epic.id,
                epic_name=epic.epic_name, raw_title=raw_title, title=title,
                kind=raw.get("kind"), owner=raw.get("owner"), hours=raw.get("hours"),
                sprint=raw.get("sprint"), deps=list(raw.get("deps", [])),
                wu=list(wu), spec=list(raw.get("spec", parent.spec if parent else [])),
                desc=raw.get("desc"), done=raw.get("done"), label=raw.get("label"),
                constraint=raw.get("constraint", constraint), children=[])


def _bracket_tag(title):
    """'[D33] ...' -> 'D33'; tiêu đề không có [..] -> None."""
    return title[1:title.index("]")] if title.startswith("[") and "]" in title else None


def _rollup(items, by_id):
    """Cha = tổng giờ con (chỉ cộng item lá); owner cha = người nhiều giờ nhất; sprint cha = sprint chung."""
    for it in reversed(items):  # con đứng sau cha → duyệt ngược để con xong trước
        if not it.children:
            it["is_leaf"] = True
            continue
        it["is_leaf"] = False
        kids = [by_id[c] for c in it.children]
        it["hours"] = sum(k.hours or 0 for k in kids)
        if it.level != "epic":
            per_owner = {}
            for leaf in leaves_of(it, by_id):
                per_owner[leaf.owner] = per_owner.get(leaf.owner, 0) + (leaf.hours or 0)
            it["owner"] = max(per_owner, key=per_owner.get)
            sprints = {leaf.sprint for leaf in leaves_of(it, by_id)}
            it["sprint"] = sprints.pop() if len(sprints) == 1 else None


def leaves_of(item, by_id):
    """Mọi item lá dưới item (chính nó nếu là lá)."""
    if not item.children:
        return [item]
    out = []
    for c in item.children:
        out.extend(leaves_of(by_id[c], by_id))
    return out


def dep_leaves(item, by_id):
    """Item lá mà item phụ thuộc: deps của chính nó + deps kế thừa từ issue cha (với sub-issue)."""
    deps = list(item.deps)
    if item.level == "sub":
        deps += by_id[item.parent].deps
    out = []
    for d in deps:
        if d in by_id:  # phụ thuộc không tồn tại do check-backlog.py báo lỗi, không crash ở đây
            out.extend(leaves_of(by_id[d], by_id))
    return out


def fmt_hours(h):
    return f"{h:g}"


def render_body(item, by_id, meta, numbers):
    """Body issue tiếng Việt. numbers: id nội bộ -> số issue GitHub (có thể thiếu khi chưa tạo)."""
    def ref(i):
        return f"#{numbers[i]} ({i})" if i in numbers else i

    lines = [f"<!-- backlog-id: {item.id} -->"]
    hours_note = "" if item.is_leaf else " (tổng con)"
    sprint = meta["sprints"].get(item.sprint, "chưa xếp (backlog)") if item.sprint else "chưa xếp (backlog)"
    lines.append(f"**Epic:** {item.epic} {item.epic_name} · **Loại:** {ITEM_TYPE[item.level]}"
                 + (f" / {item.kind}" if item.level != "epic" else "")
                 + f" · **担当(仮):** {item.owner} · **Constraint:** {item.constraint}")
    lines.append(f"**見積時間:** {fmt_hours(item.hours)}h{hours_note} · **Iteration:** {sprint}")
    if item.wu:
        lines.append(f"**WU nguồn:** {', '.join(item.wu)}")
    if item.spec:
        lines.append(f"**Spec (mã LAB-4):** {', '.join(item.spec)}")
    deps = item.deps
    if deps:
        lines.append("**Phụ thuộc:** " + ", ".join(ref(d) for d in deps))
    if item.desc:
        lines += ["", "### Mô tả", item.desc]
    if item.level == "epic":
        lines += ["", "### Tiêu chí xong",
                  "- Mọi issue con Done; tổng giờ epic = tổng item lá (script tự cộng)."]
    else:
        lines += ["", "### Tiêu chí xong"]
        if item.done:
            lines.append(f"- {item.done}")
        lines.append("- Đạt Định nghĩa xong chung: code + test + review + cập nhật tài liệu "
                     "(task-breakdown.md §1).")
    lines += ["", f"> Issue do `tools/create-issues.py` đồng bộ từ `tools/backlog.yaml`; muốn đổi nội dung thì đổi "
                  f"file YAML. Nguồn break: thiết kế LAB-4 @ {meta['source_commit']} (chỉ ghi mã)."]
    return "\n".join(lines)
