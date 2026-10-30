"""Lấy ảnh chụp issue + trường Project (chỉ đọc) làm đầu vào cho bước chấm.

Chạy:  python issue_snapshot.py --repo OWNER/REPO --project-owner OWNER --project-number N --out tmp/swp-snapshot.json
Issue đã đóng: lấy thêm MÔ TẢ BAN ĐẦU (bản sửa cũ nhất trong userContentEdits) để chấm theo mô tả gốc.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from gh_client import graphql, graphql_nodes

FIELD_SWP, FIELD_HOURS, FIELD_TYPE, FIELD_CONSTRAINT = "SWP", "見積時間 / Estimate (hours)", "Item Type", "Constraint"

_ISSUES_Q = """query($o:String!,$r:String!,$after:String){repository(owner:$o,name:$r){issues(first:50,after:$after){
 pageInfo{hasNextPage endCursor} nodes{number title url body state closedAt labels(first:20){nodes{name}}
 parent{number} subIssues{totalCount}}}}}"""
_ORIGINAL_Q = """query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){
 userContentEdits(last:1){nodes{createdAt diff}}}}}"""
_FIELDS_Q = """query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id url fields(first:50){nodes{
 ... on ProjectV2FieldCommon{id name dataType}}}}}}"""
_ITEMS_Q = """query($o:String!,$n:Int!,$after:String){user(login:$o){projectV2(number:$n){items(first:100,after:$after){
 pageInfo{hasNextPage endCursor} nodes{id content{... on Issue{number state repository{nameWithOwner}}}
 fieldValues(first:30){nodes{
  ... on ProjectV2ItemFieldSingleSelectValue{field{... on ProjectV2FieldCommon{name}} name}
  ... on ProjectV2ItemFieldNumberValue{field{... on ProjectV2FieldCommon{name}} number}}}}}}}}"""


def project_meta(owner, number):
    """{'id', 'url', 'fields': {tên: {'id', 'type'}}} của Project v2 (user-level)."""
    p = graphql(_FIELDS_Q, {"o": owner, "n": number})["user"]["projectV2"]
    fields = {f["name"]: {"id": f["id"], "type": f["dataType"]} for f in p["fields"]["nodes"] if f}
    return {"id": p["id"], "url": p["url"], "fields": fields}


def project_items(owner, number, repo):
    """Số issue -> {'item_id', 'state' (open / closed, live), 'values': {tên trường: giá trị}} cho issue thuộc repo."""
    out = {}
    for n in graphql_nodes(_ITEMS_Q, {"o": owner, "n": number}, ["user", "projectV2", "items"]):
        c = n.get("content") or {}
        if c.get("repository", {}).get("nameWithOwner") != repo:
            continue
        vals = {v["field"]["name"]: v.get("name", v.get("number"))
                for v in n["fieldValues"]["nodes"] if v and v.get("field")}
        out[c["number"]] = {"item_id": n["id"], "state": c["state"].lower(), "values": vals}
    return out


def _has_edits(owner, name, number):
    q = "query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){userContentEdits{totalCount}}}}"
    return graphql(q, {"o": owner, "r": name, "n": number})["repository"]["issue"]["userContentEdits"]["totalCount"] > 0


def original_body(owner, name, number):
    """Mô tả lúc tạo issue (bản sửa cũ nhất); None nếu issue chưa từng bị sửa (mô tả hiện tại là bản gốc)."""
    edits = graphql(_ORIGINAL_Q, {"o": owner, "r": name, "n": number})["repository"]["issue"]["userContentEdits"]
    nodes = edits["nodes"]
    return nodes[0]["diff"] if nodes and nodes[0].get("diff") is not None else None


def fetch(repo, project_owner, project_number):
    owner, name = repo.split("/")
    board = project_items(project_owner, project_number, repo)
    issues = []
    for n in graphql_nodes(_ISSUES_Q, {"o": owner, "r": name}, ["repository", "issues"]):
        vals = board.get(n["number"], {}).get("values", {})
        row = {
            "number": n["number"], "title": n["title"], "url": n["url"], "body": n["body"] or "",
            "state": n["state"].lower(), "closed_at": n["closedAt"],
            "labels": [lb["name"] for lb in n["labels"]["nodes"]],
            "parent": (n["parent"] or {}).get("number"), "is_leaf": n["subIssues"]["totalCount"] == 0,
            "on_project": n["number"] in board, "item_type": vals.get(FIELD_TYPE),
            "constraint": vals.get(FIELD_CONSTRAINT), "hours": vals.get(FIELD_HOURS), "swp_now": vals.get(FIELD_SWP),
        }
        if row["state"] == "closed":
            orig = original_body(owner, name, n["number"])
            row["original_body"] = orig if orig is not None else row["body"]
            # None = chưa từng sửa (body hiện tại là bản gốc) — chỉ cảnh báo khi có lịch sử sửa mà không đọc được bản gốc
            row["original_missing"] = orig is None and _has_edits(owner, name, n["number"])
            if row["original_missing"]:
                print(f"  CẢNH BÁO #{n['number']}: không đọc được mô tả ban đầu — chấm theo mô tả hiện tại, độ tin cậy thấp")
        issues.append(row)
    return {"repo": repo, "project_owner": project_owner, "project_number": project_number,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "issues": sorted(issues, key=lambda r: r["number"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--project-owner", required=True)
    ap.add_argument("--project-number", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    snap = fetch(a.repo, a.project_owner, a.project_number)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    closed = sum(r["state"] == "closed" for r in snap["issues"])
    print(f"Ảnh chụp: {len(snap['issues'])} issue ({closed} đã đóng) → {out}")


if __name__ == "__main__":
    main()
