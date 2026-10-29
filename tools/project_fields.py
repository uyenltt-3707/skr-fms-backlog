"""Đọc / ghi trường của GitHub Project (v2) cho các issue backlog.

Tên trường đúng như Project #2 dựng ở B1 (tools/setup-github-project.sh).
SWP KHÔNG được ghi ở đây (B3 mới chấm, chỉ ghi SWP đã review).
"""
from github_api import graphql, graphql_nodes

F_STATUS, F_TYPE, F_CONSTRAINT = "Status", "Item Type", "Constraint"
F_OWNER, F_HOURS, F_ITERATION = "担当(仮)", "見積時間 / Estimate (hours)", "Iteration"

_FIELDS_Q = """query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id url fields(first:50){nodes{
 ... on ProjectV2FieldCommon{id name dataType}
 ... on ProjectV2SingleSelectField{options{id name}}
 ... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}}"""

_ITEMS_Q = """query($o:String!,$n:Int!,$after:String){user(login:$o){projectV2(number:$n){items(first:100,after:$after){
 pageInfo{hasNextPage endCursor} nodes{id content{... on Issue{number repository{nameWithOwner}}}
 fieldValues(first:30){nodes{
  ... on ProjectV2ItemFieldSingleSelectValue{field{... on ProjectV2FieldCommon{name}} name}
  ... on ProjectV2ItemFieldNumberValue{field{... on ProjectV2FieldCommon{name}} number}
  ... on ProjectV2ItemFieldIterationValue{field{... on ProjectV2FieldCommon{name}} title}}}}}}}}"""


class Project:
    def __init__(self, owner, number):
        p = graphql(_FIELDS_Q, {"o": owner, "n": number})["user"]["projectV2"]
        self.owner, self.number, self.id, self.url = owner, number, p["id"], p["url"]
        self.fields = {}
        for f in p["fields"]["nodes"]:
            if not f:
                continue
            opts = {o["name"]: o["id"] for o in f.get("options", [])}
            conf = f.get("configuration") or {}
            iters = conf.get("iterations", []) + conf.get("completedIterations", [])  # sprint đã qua vẫn gán được
            opts.update({i["title"]: i["id"] for i in iters})
            self.fields[f["name"]] = {"id": f["id"], "type": f["dataType"], "options": opts}
        for name in (F_STATUS, F_TYPE, F_CONSTRAINT, F_OWNER, F_HOURS, F_ITERATION):
            if name not in self.fields:
                raise SystemExit(f"Project thiếu trường '{name}' — chạy tools/setup-github-project.sh trước.")

    def validate(self, wanted):
        """wanted: danh sách dict {trường: giá trị}. Dừng sớm nếu giá trị không có trong option của Project."""
        bad = {(name, v) for w in wanted for name, v in w.items()
               if v is not None and self.fields[name]["type"] in ("SINGLE_SELECT", "ITERATION")
               and v not in self.fields[name]["options"]}
        if bad:
            raise SystemExit(f"Giá trị không có trong option của Project: {sorted(bad)}")

    def items(self, repo):
        """Số issue -> {'item_id', 'values': {tên trường: giá trị hiển thị}} cho issue thuộc repo."""
        out = {}
        nodes = graphql_nodes(_ITEMS_Q, {"o": self.owner, "n": self.number}, ["user", "projectV2", "items"])
        for n in nodes:
            c = n.get("content") or {}
            if c.get("repository", {}).get("nameWithOwner") != repo:
                continue
            vals = {}
            for v in n["fieldValues"]["nodes"]:
                if v and v.get("field"):
                    vals[v["field"]["name"]] = v.get("name", v.get("number", v.get("title")))
            out[c["number"]] = {"item_id": n["id"], "values": vals}
        return out

    def add_item(self, content_node_id):
        q = "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}"
        return graphql(q, {"p": self.id, "c": content_node_id})["addProjectV2ItemById"]["item"]["id"]

    def update(self, item_id, changes):
        """changes: {tên trường: giá trị mong muốn | None (= xóa)}. Gộp mọi thay đổi vào một mutation."""
        parts, variables = [], {"p": self.id, "i": item_id}
        for k, (name, value) in enumerate(changes.items()):
            f = self.fields[name]
            if value is None:
                parts.append(f'c{k}:clearProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$i,fieldId:"{f["id"]}"}})'
                             "{clientMutationId}")
                continue
            if f["type"] == "NUMBER":
                val = f"{{number:{float(value)}}}"
            elif f["type"] == "ITERATION":
                val = f'{{iterationId:"{f["options"][value]}"}}'
            else:
                val = f'{{singleSelectOptionId:"{f["options"][value]}"}}'
            parts.append(f'u{k}:updateProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$i,fieldId:"{f["id"]}",'
                         f"value:{val}}}){{clientMutationId}}")
        if parts:
            graphql("mutation($p:ID!,$i:ID!){" + " ".join(parts) + "}", variables)


def desired_values(item, meta):
    """Giá trị trường mong muốn cho một item backlog. Status chỉ đặt Todo khi đang trống (không ghi đè tiến độ)."""
    sprint = meta["sprints"].get(item.sprint) if item.sprint else None
    return {
        F_TYPE: {"epic": "Epic", "issue": "Issue", "sub": "Sub-issue"}[item.level],
        F_CONSTRAINT: item.constraint,
        F_OWNER: item.owner,
        F_ITERATION: sprint,
        F_HOURS: item.hours,
    }


def diff_values(current, desired):
    """Trả về các trường cần đổi (so sánh số theo float, chuỗi theo nguyên văn)."""
    changes = {}
    for name, want in desired.items():
        have = current.get(name)
        same = (have is None and want is None) or (
            isinstance(want, (int, float)) and have is not None and float(have) == float(want)) or have == want
        if not same:
            changes[name] = want
    if not current.get(F_STATUS):
        changes[F_STATUS] = "Todo"
    return changes
