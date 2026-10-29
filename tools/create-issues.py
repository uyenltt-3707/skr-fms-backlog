"""Tạo / cập nhật epic → issue → sub-issue trên GitHub từ tools/backlog.yaml và điền trường Project #2.

Idempotent: mỗi issue mang marker `<!-- backlog-id: X -->` trong body; chạy lại thì tìm theo marker,
chỉ sửa phần lệch (tiêu đề, body, nhãn, cha, trường Project), không tạo trùng.
Kết quả mapping id nội bộ ↔ số issue ghi vào tools/issue-map.json.

Chạy:  python tools/create-issues.py [--dry-run]
Cần:   gh đã đăng nhập (scope repo + project), Python có PyYAML.
"""
import json
import re
import sys
import time

import backlog_model as bm
from github_api import graphql_nodes, rest, rest_all
from project_fields import Project, desired_values, diff_values

MARKER = re.compile(r"<!-- backlog-id: (\S+) -->")
LABEL_CHECK = {"要確認": ("d93f0b", "Cần hỏi lại PL / khách trước khi chốt")}
PAUSE = 0.8  # giây giữa các lệnh tạo nội dung, tránh secondary rate limit
_PARENTS_Q = """query($o:String!,$r:String!,$after:String){repository(owner:$o,name:$r){issues(first:100,after:$after){
 pageInfo{hasNextPage endCursor} nodes{number parent{number}}}}}"""


def creation_order(items, by_id):
    """Thứ tự tạo: cha trước con, item được phụ thuộc trước item phụ thuộc (để body có sẵn #số)."""
    done, out = set(), []

    def visit(it):
        if it.id in done:
            return
        done.add(it.id)
        if it.parent:
            visit(by_id[it.parent])
        for d in it.deps:
            visit(by_id[d])
        out.append(it)

    for it in items:
        visit(it)
    return out


def ensure_labels(repo, dry):
    have = {lb["name"] for lb in rest_all(f"repos/{repo}/labels?per_page=100")}
    for name, (color, desc) in LABEL_CHECK.items():
        if name not in have and not dry:
            rest("POST", f"repos/{repo}/labels", {"name": name, "color": color, "description": desc})
            print(f"+ label {name}")


def main():
    dry = "--dry-run" in sys.argv
    meta, items, by_id = bm.load()
    repo, owner, repo_name = meta["repo"], meta["project_owner"], meta["repo"].split("/")[1]
    project = Project(owner, meta["project_number"])
    project.validate([desired_values(it, meta) for it in items])  # dừng trước mọi lệnh ghi nếu option sai
    ensure_labels(repo, dry)

    existing = {}
    for iss in rest_all(f"repos/{repo}/issues?state=all&per_page=100"):
        m = MARKER.search(iss.get("body") or "")
        if m and "pull_request" not in iss:
            if m.group(1) in existing:
                raise SystemExit(f"Marker {m.group(1)} trùng ở #{existing[m.group(1)]['number']} và "
                                 f"#{iss['number']} — đóng / xóa bản thừa rồi chạy lại.")
            existing[m.group(1)] = iss
    numbers = {k: v["number"] for k, v in existing.items()}
    stats = {"created": 0, "updated": 0, "linked": 0, "added": 0, "fields": 0}

    # 1. Issue: tạo mới hoặc đồng bộ tiêu đề / body / nhãn
    for it in creation_order(items, by_id):
        body = bm.render_body(it, by_id, meta, numbers)
        labels = [it.label] if it.label else []
        cur = existing.get(it.id)
        if cur is None:
            print(f"+ tạo {it.id}: {it.title}")
            if not dry:
                cur = rest("POST", f"repos/{repo}/issues", {"title": it.title, "body": body, "labels": labels})
                existing[it.id], numbers[it.id] = cur, cur["number"]
                time.sleep(PAUSE)
            stats["created"] += 1
            continue
        have_labels = {lb["name"] for lb in cur.get("labels", [])}
        if cur["title"] != it.title or (cur.get("body") or "").strip() != body.strip() or not set(labels) <= have_labels:
            print(f"~ cập nhật #{cur['number']} {it.id}")
            if not dry:
                existing[it.id] = rest("PATCH", f"repos/{repo}/issues/{cur['number']}",
                                       {"title": it.title, "body": body, "labels": sorted(have_labels | set(labels))})
                time.sleep(PAUSE)
            stats["updated"] += 1
    if dry:
        print(f"[dry-run] {stats}")
        return

    # 2. Body lần đầu có thể thiếu #số của item tạo sau → đồng bộ lại
    for it in items:
        body = bm.render_body(it, by_id, meta, numbers)
        if (existing[it.id].get("body") or "").strip() != body.strip():
            rest("PATCH", f"repos/{repo}/issues/{numbers[it.id]}", {"body": body})
            existing[it.id]["body"] = body

    # 3. Sub-issue thật của GitHub: gắn con vào cha (đổi cha nếu lệch)
    parents = {n["number"]: (n["parent"] or {}).get("number")
               for n in graphql_nodes(_PARENTS_Q, {"o": owner, "r": repo_name}, ["repository", "issues"])}
    for it in items:
        if it.level == "epic":
            continue
        want = numbers[it.parent]
        have = parents.get(numbers[it.id])
        if have != want:
            rest("POST", f"repos/{repo}/issues/{want}/sub_issues",
                 {"sub_issue_id": existing[it.id]["id"], "replace_parent": have is not None})
            stats["linked"] += 1
            time.sleep(PAUSE)

    # 4. Project #2: thêm item + điền trường (không đụng SWP; Status chỉ đặt Todo khi trống)
    on_board = project.items(repo)
    for it in items:
        num = numbers[it.id]
        entry = on_board.get(num)
        if entry is None:
            entry = {"item_id": project.add_item(existing[it.id]["node_id"]), "values": {}}
            stats["added"] += 1
            time.sleep(PAUSE)
        changes = diff_values(entry["values"], desired_values(it, meta))
        if changes:
            project.update(entry["item_id"], changes)
            stats["fields"] += 1

    mapping = {it.id: {"number": numbers[it.id], "level": it.level, "title": it.title,
                       "url": f"https://github.com/{repo}/issues/{numbers[it.id]}"} for it in items}
    bm.MAP_PATH.write_text(json.dumps(dict(sorted(mapping.items(), key=lambda kv: kv[1]["number"])),
                                      ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"XONG {stats} · {len(items)} item · mapping → {bm.MAP_PATH.name} · Project {project.url}")


if __name__ == "__main__":
    main()
