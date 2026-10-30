"""Sprint giả lập: đọc progress-data/sprint1.yaml + trạng thái thật trên Project #2, tính bảng trạng thái và burndown.

Dùng bởi simulate-sprint.py (ghi Project), check-progress-report.py và check-backlog.py (kiểm). Không ghi gì ở module này.
Mọi con số báo cáo (số issue, SWP) lấy từ Project; YAML chỉ cho lịch sử trạng thái theo ngày.
"""
import json
from pathlib import Path

import yaml

import backlog_model as bm
from github_api import graphql_nodes
from project_fields import F_HOURS, F_ITERATION, F_OWNER, F_STATUS, Project

SPRINT_PATH = bm.TOOLS_DIR.parent / "progress-data" / "sprint1.yaml"
STATUSES = ["Done", "In Review", "In Progress", "Todo"]
_ISSUES_Q = """query($o:String!,$r:String!,$after:String){repository(owner:$o,name:$r){issues(first:100,after:$after){
 pageInfo{hasNextPage endCursor} nodes{number state parent{number}}}}}"""


def load_sim(path=SPRINT_PATH):
    """(thông tin sprint, {số issue: item}) — item có 'final' = Status cuối sprint. Báo lỗi nếu Status / ngày sai."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sprint, days = data["sprint"], data["sprint"]["workdays"]
    items = {}
    for it in data["items"]:
        hist = [(str(d), s) for d, s in it["history"]]
        for d, s in hist:
            if s not in STATUSES or d not in days:
                raise SystemExit(f"#{it['number']}: lịch sử sai ({d}, {s}) — Status phải thuộc {STATUSES}, ngày thuộc workdays")
        if [d for d, _ in hist] != sorted(d for d, _ in hist):
            raise SystemExit(f"#{it['number']}: lịch sử không theo thứ tự ngày")
        items[it["number"]] = {**it, "history": hist, "final": status_on(hist, days[-1])}
    return sprint, items


def status_on(hist, day):
    """Status cuối ngày `day` (chuỗi YYYY-MM-DD)."""
    status = "Todo"
    for d, s in hist:
        if d <= day:
            status = s
    return status


def read_board():
    """Đọc Project + issue thật: (meta, items backlog, by_id, mapping, board, issues).

    board: số issue → {'item_id', 'values'} · issues: số issue → {'state', 'parent'}.
    """
    meta, items, by_id = bm.load()
    mapping = json.loads(bm.MAP_PATH.read_text(encoding="utf-8"))
    project = Project(meta["project_owner"], meta["project_number"])
    board = project.items(meta["repo"])
    nodes = graphql_nodes(_ISSUES_Q, {"o": meta["project_owner"], "r": meta["repo"].split("/")[1]},
                          ["repository", "issues"])
    issues = {n["number"]: {"state": n["state"], "parent": (n["parent"] or {}).get("number")} for n in nodes}
    return {"meta": meta, "items": items, "by_id": by_id, "mapping": mapping, "project": project,
            "board": board, "issues": issues}


def sprint_leaves(ctx, iteration):
    """Item lá có Iteration = `iteration` trên Project: số issue → {'id', 'status', 'swp', 'hours', 'owner', 'state'}."""
    num_of = {k: v["number"] for k, v in ctx["mapping"].items()}
    out = {}
    for it in ctx["items"]:
        num = num_of.get(it.id)
        vals = ctx["board"].get(num, {}).get("values", {})
        if it.is_leaf and vals.get(F_ITERATION) == iteration:
            out[num] = {"id": it.id, "status": vals.get(F_STATUS), "swp": float(vals.get("SWP") or 0),
                        "hours": float(vals.get(F_HOURS) or 0), "owner": vals.get(F_OWNER),
                        "state": ctx["issues"].get(num, {}).get("state")}
    return out


def status_table(leaves):
    """Status → (số item, tổng SWP, tổng giờ), đủ 4 Status theo thứ tự STATUSES."""
    table = {s: [0, 0.0, 0.0] for s in STATUSES}
    for lf in leaves.values():
        row = table.setdefault(lf["status"] or "(trống)", [0, 0.0, 0.0])
        row[0] += 1
        row[1] += lf["swp"]
        row[2] += lf["hours"]
    return table


def burndown(sprint, sim, leaves):
    """[(nhãn ngày, lý tưởng, thực tế còn lại, SWP xong trong ngày)] — điểm 0 = đầu sprint, rồi cuối mỗi ngày làm việc.

    SWP từng item lấy từ Project (`leaves`); ngày Done lấy từ lịch sử giả lập.
    """
    days = sprint["workdays"]
    total = sum(lf["swp"] for lf in leaves.values())
    rows, prev = [("đầu sprint", total, total, 0.0)], total
    for k, day in enumerate(days, 1):
        remaining = sum(lf["swp"] for n, lf in leaves.items() if status_on(sim[n]["history"], day) != "Done")
        rows.append((day, round(total - total * k / len(days), 1), remaining, prev - remaining))
        prev = remaining
    return rows


def expected_parent_status(ctx, sim):
    """Status mong muốn của issue cha / epic có con trong sprint: mọi lá Done → Done; mọi lá Todo → Todo; còn lại In Progress.

    Lá ngoài sprint coi là Todo. Trả về số issue cha → Status.
    """
    num_of = {k: v["number"] for k, v in ctx["mapping"].items()}
    by_id = ctx["by_id"]
    touched = set()
    for num, s in sim.items():
        node = by_id[s["id"]]
        while node.parent:
            node = by_id[node.parent]
            touched.add(node.id)
    out = {}
    for pid in touched:
        finals = [sim.get(num_of[lf.id], {}).get("final", "Todo") for lf in bm.leaves_of(by_id[pid], by_id)]
        out[num_of[pid]] = ("Done" if all(f == "Done" for f in finals)
                            else "Todo" if all(f == "Todo" for f in finals) else "In Progress")
    return out


def verify_sprint_state(ctx, sprint, sim):
    """Lỗi trạng thái Sprint giả lập trên Project: lá trong sprint = YAML và Status = Status cuối; Done ⇔ issue đóng;
    cha / epic = Status cộng dồn; lá ngoài sprint vẫn Todo và đang mở."""
    errs = []
    leaves = sprint_leaves(ctx, sprint["iteration"])
    if set(leaves) != set(sim):
        errs.append(f"Iteration {sprint['iteration']}: Project {sorted(leaves)} ≠ YAML {sorted(sim)}")
    want = {n: s["final"] for n, s in sim.items()}
    want.update(expected_parent_status(ctx, sim))
    num_of = {k: v["number"] for k, v in ctx["mapping"].items()}
    for it in ctx["items"]:
        n = num_of.get(it.id)
        if n is None or n not in ctx["board"]:
            continue  # item chưa lên Project do check_remote báo
        have, state = ctx["board"][n]["values"].get(F_STATUS), ctx["issues"].get(n, {}).get("state")
        expect = want.get(n, "Todo")
        if have != expect:
            errs.append(f"#{n} {it.id}: Status = {have}, mong đợi {expect} (sprint1.yaml)")
        if (state == "CLOSED") != (expect == "Done"):
            errs.append(f"#{n} {it.id}: issue {state} nhưng Status mong đợi {expect}")
    return errs
