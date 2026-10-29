#!/usr/bin/env bash
# Dựng GitHub Project (user-level, public) "SKR-FMS Backlog" + trường + view.
# Idempotent: chạy lại nhiều lần không tạo trùng; chỉ bổ sung phần còn thiếu.
# Yêu cầu: gh đã đăng nhập với scope `project` và `repo` (gh auth refresh -s project).
#
# Biến môi trường (tùy chọn):
#   REPO           tên repo để liên kết          (mặc định: skr-fms-backlog)
#   TITLE          tên Project                   (mặc định: SKR-FMS Backlog)
#   SPRINT1_START  ngày bắt đầu Sprint 1 GIẢ LẬP (mặc định: 2026-11-02, thứ Hai)
#   SPRINT_COUNT   số Sprint tạo sẵn             (mặc định: 3)
set -euo pipefail

REPO="${REPO:-skr-fms-backlog}"
TITLE="${TITLE:-SKR-FMS Backlog}"
SPRINT1_START="${SPRINT1_START:-2026-11-02}"
SPRINT_COUNT="${SPRINT_COUNT:-3}"
SPRINT_DAYS=14

# Tên trường (đúng như đề: Japanese + English)
F_SWP="SWP"
F_HOURS="見積時間 / Estimate (hours)"
F_ASSIGNEE="担当(仮)"
# "Type" bị GitHub giữ chỗ (reserved) -> dùng "Item Type"
F_TYPE="Item Type"
F_CONSTRAINT="Constraint"
F_ITERATION="Iteration"

log() { printf '[setup] %s\n' "$*" >&2; }

OWNER="$(gh api user --jq .login)"
log "owner=$OWNER repo=$REPO"

# ---------- 1. Project ----------
NUM="$(gh project list --owner "$OWNER" --limit 100 --format json \
  --jq ".projects[] | select(.title==\"$TITLE\") | .number" | head -n1)"
if [ -z "$NUM" ]; then
  NUM="$(gh project create --owner "$OWNER" --title "$TITLE" --format json --jq .number)"
  log "created project #$NUM"
else
  log "project exists #$NUM"
fi

gh project edit "$NUM" --owner "$OWNER" --visibility PUBLIC \
  --description "LAB-5 Product A: epic/issue/sub-issue, SWP (đã review), giờ ước lượng. Sprint & người phụ trách là GIẢ LẬP." \
  >/dev/null
PROJECT_ID="$(gh project view "$NUM" --owner "$OWNER" --format json --jq .id)"
PROJECT_URL="$(gh project view "$NUM" --owner "$OWNER" --format json --jq .url)"

# ---------- 2. Liên kết repo ----------
if gh project link "$NUM" --owner "$OWNER" --repo "$OWNER/$REPO" >/dev/null 2>&1; then
  log "linked repo $OWNER/$REPO"
else
  log "repo link skipped (đã liên kết hoặc không có quyền)"
fi

# ---------- helpers ----------
# Trả về id của field theo tên (rỗng nếu chưa có)
field_id() {
  gh project field-list "$NUM" --owner "$OWNER" --limit 100 --format json \
    --jq ".fields[] | select(.name==\"$1\") | .id"
}
ensure_field() { # name data-type [options csv]
  local name="$1" type="$2" opts="${3:-}"
  if [ -n "$(field_id "$name")" ]; then log "field exists: $name"; return; fi
  if [ -n "$opts" ]; then
    gh project field-create "$NUM" --owner "$OWNER" --name "$name" --data-type "$type" \
      --single-select-options "$opts" >/dev/null
  else
    gh project field-create "$NUM" --owner "$OWNER" --name "$name" --data-type "$type" >/dev/null
  fi
  log "created field: $name"
}

# ---------- 3. Status (field built-in): Todo / In Progress / In Review / Done ----------
STATUS_ID="$(field_id Status)"
CUR_STATUS="$(gh project field-list "$NUM" --owner "$OWNER" --limit 100 --format json \
  --jq '.fields[] | select(.name=="Status") | [.options[].name] | join(",")')"
WANT_STATUS="Todo,In Progress,In Review,Done"
if [ "$CUR_STATUS" != "$WANT_STATUS" ]; then
  gh api graphql --input - >/dev/null <<EOF
{"query":"mutation(\$f:ID!){updateProjectV2Field(input:{fieldId:\$f,singleSelectOptions:[{name:\"Todo\",color:GRAY,description:\"Chưa bắt đầu\"},{name:\"In Progress\",color:YELLOW,description:\"Đang làm\"},{name:\"In Review\",color:ORANGE,description:\"Đang review\"},{name:\"Done\",color:GREEN,description:\"Xong theo định nghĩa xong\"}]}){projectV2Field{... on ProjectV2SingleSelectField{id}}}}","variables":{"f":"$STATUS_ID"}}
EOF
  log "status options set: $WANT_STATUS"
else
  log "status options ok"
fi

# ---------- 4. Trường tùy biến ----------
ensure_field "$F_TYPE"       SINGLE_SELECT "Epic,Issue,Sub-issue"
ensure_field "$F_CONSTRAINT" SINGLE_SELECT "完納奨励金,なし"
ensure_field "$F_ASSIGNEE"   SINGLE_SELECT "FE-A,FE-B,BE-A,BE-B,QA-A,PM"
ensure_field "$F_SWP"        NUMBER   # để trống; chỉ ghi SWP đã review
ensure_field "$F_HOURS"      NUMBER

# Iteration: gh CLI chưa hỗ trợ -> dùng GraphQL. Sprint 1 bắt đầu ngày GIẢ LẬP.
if [ -z "$(field_id "$F_ITERATION")" ]; then
  ITERS=""
  for i in $(seq 1 "$SPRINT_COUNT"); do
    start="$(date -d "$SPRINT1_START + $(( (i-1) * SPRINT_DAYS )) days" +%F)"
    ITERS="$ITERS{\"title\":\"Sprint $i (giả lập)\",\"startDate\":\"$start\",\"duration\":$SPRINT_DAYS},"
  done
  ITERS="[${ITERS%,}]"
  gh api graphql --input - >/dev/null <<EOF
{"query":"mutation(\$p:ID!,\$n:String!,\$c:ProjectV2IterationFieldConfigurationInput!){createProjectV2Field(input:{projectId:\$p,dataType:ITERATION,name:\$n,iterationConfiguration:\$c}){projectV2Field{... on ProjectV2IterationField{id}}}}","variables":{"p":"$PROJECT_ID","n":"$F_ITERATION","c":{"startDate":"$SPRINT1_START","duration":$SPRINT_DAYS,"iterations":$ITERS}}}
EOF
  log "created iteration field: $SPRINT_COUNT sprints x ${SPRINT_DAYS}d from $SPRINT1_START"
else
  log "field exists: $F_ITERATION"
fi

# ---------- 5. Views: Board (theo Status) + Table ----------
views() {
  gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{views(first:20){nodes{id name layout}}}}}' \
    -f p="$PROJECT_ID" --jq ".data.node.views.nodes[] | [.id,.name,.layout] | @tsv"
}
CUR_VIEWS="$(views)"

# View mặc định (TABLE_LAYOUT, thường tên "View 1") -> đổi tên thành "Table"
if ! printf '%s\n' "$CUR_VIEWS" | cut -f2 | grep -qx "Table"; then
  DEFAULT_TABLE_ID="$(printf '%s\n' "$CUR_VIEWS" | awk -F'\t' '$3=="TABLE_LAYOUT"{print $1; exit}')"
  if [ -n "$DEFAULT_TABLE_ID" ]; then
    gh api graphql -f query='mutation($v:ID!){updateProjectV2View(input:{viewId:$v,name:"Table"}){projectV2View{id}}}' \
      -f v="$DEFAULT_TABLE_ID" >/dev/null
  else
    gh api graphql -f query='mutation($p:ID!){createProjectV2View(input:{projectId:$p,name:"Table",layout:TABLE_LAYOUT}){projectV2View{id}}}' \
      -f p="$PROJECT_ID" >/dev/null
  fi
  log "view ready: Table"
else
  log "view exists: Table"
fi

if ! printf '%s\n' "$CUR_VIEWS" | cut -f2 | grep -qx "Board"; then
  gh api graphql -f query='mutation($p:ID!){createProjectV2View(input:{projectId:$p,name:"Board",layout:BOARD_LAYOUT}){projectV2View{id}}}' \
    -f p="$PROJECT_ID" >/dev/null
  log "view created: Board"
else
  log "view exists: Board"
fi

log "DONE  number=$NUM"
log "URL   $PROJECT_URL"
echo "$PROJECT_URL"
