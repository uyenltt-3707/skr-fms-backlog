"""Thang điểm SWP TẠM (PL duyệt, B3a; PL sửa R1–R3, B3b) và luật chấm một item lá theo MÔ TẢ issue.

SWP = Scope (1–5) × Complexity (1–5). KHÔNG dùng số giờ: dòng 見積時間 bị xóa khỏi văn bản trước khi chấm.
Luật là từ khóa có trọng số trên văn bản issue (tiêu đề, loại, mô tả, tiêu chí xong) — tái lập được, giải thích được;
item không có dấu hiệu rõ nhận điểm mặc định và độ tin cậy thấp để PL kiểm.
"""
import re
import sys

for _stream in (sys.stdout, sys.stderr):  # Windows: stdout chuyển hướng mặc định code page ANSI
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ALLOWED_SWP = {s * c for s in range(1, 6) for c in range(1, 6)}  # SWP hợp lệ = tích hai điểm 1–5
PROVISIONAL_NOTE = ("SWP tạm — thang điểm do PL tự đặt, chờ skill chính thức của chương trình; "
                    "khi có sẽ chạy lại và thay thế")

SCOPE_SCALE = {
    1: "thay đổi rất nhỏ trong 1 thành phần, không đổi giao diện / DB",
    2: "một thành phần (1 API / 1 màn hình đơn giản / 1 bảng)",
    3: "hai lớp trong cùng chức năng",
    4: "xuyên UI + API + DB trong 1 chức năng hoặc ảnh hưởng nhiều màn hình",
    5: "nhiều chức năng, hạ tầng toàn hệ thống, migration",
}
COMPLEXITY_SCALE = {
    1: "CRUD thuần",
    2: "validation đơn giản, ít trạng thái",
    3: "nhiều nhánh / state machine, phân quyền",
    4: "logic nghiệp vụ nhiều biến (tiền, làm tròn, kỳ, version quy tắc), nguyên tử / đồng thời",
    5: "bất định cao — kết quả chưa biết trước: đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt (R1)",
}

# Complexity: dấu hiệu theo mức (chữ thường). Lấy mức cao nhất có dấu hiệu.
CX_SIGNALS = {
    # R1: chỉ dấu hiệu kết quả BẤT ĐỊNH (đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt)
    5: ["要確認", "未決", "chưa chốt", "câu hỏi khách", "khách trả lời", "rto", "số đo", "đo thời gian", "p95"],
    4: ["tiền", "jpy", "làm tròn", "交付率", "tier", "kỳ sau", "kỳ gốc", "kỳ 完納", "theo kỳ", "version", "発効日",
        "nguyên tử", "đồng thời", "song song", "race", "chạy trùng", "delta", "完納奨励金", "支払", "暫定", "thuế",
        "biên ngày", "theo hạn"],
    3: ["trạng thái", "state machine", "dd-", "差戻し", "承認", "却下", "取消", "公布", "quyền", "vai trò", "mfa",
        "aal2", "rls", "403", "audit", "nhánh", "mã lỗi", "người duyệt", "rpc", "保留", "締め解除", "確認者", "pin",
        "phiên", "khóa tạm", "ロールバック", "確定", "提出", "từ chối", "hitl", "secret", "backfill", "map trạng thái"],
    2: ["kiểm tra", "validation", "check", "ràng buộc", "msg", "thông báo", "biến thể", "lọc", "cảnh báo", "index",
        "lịch sử", "xử lý lỗi", "chặn", "csv", "xuất"],
    1: ["crud", "thêm cột", "đọc danh sách", "hiển thị", "tra cứu", "tài liệu"],
}
# Scope: mức cơ sở theo loại item, nâng khi có dấu hiệu phạm vi rộng hơn (trừ loại trong SCOPE_FIXED).
SCOPE_BY_KIND = {"要確認": 1, "tài liệu": 1, "DB": 2, "API": 2, "UI": 2, "hạ tầng": 2, "test": 2, "batch": 3,
                 "thiết kế": 3}
SCOPE_FIXED = {"要確認", "tài liệu"}  # câu hỏi / tài liệu không đổi giao diện / DB dù nói về phạm vi rộng
SCOPE_UP = [  # (loại áp dụng | None = mọi loại, mức, dấu hiệu)
    (None, 5, ["migration", "mọi bảng", "mọi api", "mọi rpc", "khoảng 30 endpoint", "69 endpoint", "toàn hệ thống",
               "結合テスト"]),
    # Test NFR toàn hệ thống: rộng (Scope 5) VÀ bất định (Complexity 5) — cố ý cho cùng dấu hiệu nâng cả hai trục
    ({"test"}, 5, ["security", "load test", "fig-load", "diễn tập", "restore"]),
    ({"hạ tầng"}, 5, ["môi trường production", "dump", "sao chép", "giám sát", "cảnh báo", "osaka", "khung job",
                      "timeout phiên"]),
    (None, 4, ["dùng chung", "khung chung", "header", "mọi màn", "e2e", "tích hợp", "xuyên", "kịch bản", "báo cáo ngày",
               "9 báo cáo"]),
    ({"thiết kế"}, 4, ["bảng", "database design", "dbt-"]),
    ({"DB"}, 3, ["rpc", "hàm", "trigger", "view"]),
    ({"API"}, 3, ["rpc", "signed url"]),
    ({"UI"}, 3, ["api"]),
]
# R1: chủ đề NFR — trước B3b là dấu hiệu Complexity 5; nay chỉ ghi chú, Complexity chấm theo dấu hiệu thực tế
NFR_TOPIC = ["nfr", "load test", "fig-load", "diễn tập", "restore", "security", "lỗ hổng"]
ROUGH_SIGNALS = ["概算", "詳細設計未作成"]
ROUGH_SCREEN = re.compile(r"^\[SCR-(\d+)(?:〜(\d+))?\]\s*(?:画面設計|実装\s*\d+/\d+)")  # R2: sub-issue màn 概算
LAB1_LEVEL = {"S": 2, "M": 3, "L": 4}  # R2: độ phức tạp màn LAB-1 → Complexity

# Bản sửa thang điểm của PL (B3b, sau khi review 14 mẫu) — áp cho MỌI item cùng loại, không chỉ mẫu
RULES_DATE = "2026-10-30"
PL_RULES = {
    "R1": "Complexity 5 chỉ khi kết quả bất định (đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt). Việc chủ đề NFR "
          "nhưng làm theo quy trình xác định → chấm theo độ phức tạp thực tế.",
    "R2": "Màn 概算 (画面設計 và 実装 k/n): Scope 2; Complexity theo độ phức tạp màn ở LAB-1: S → 2, M → 3, L → 4.",
    "R3": "Issue 要確認 (đi hỏi làm rõ): Scope 1 × Complexity 2 = 2.",
}
HOURS_LINE = re.compile(r"^.*見積時間.*$", re.M)  # bỏ hẳn dòng giờ: chấm không được nhìn số giờ


def strip_hours(text):
    return HOURS_LINE.sub("", text or "")


def _pattern(word):
    """Từ khóa Latin / tiếng Việt khớp theo ranh giới từ («view» không khớp «under_review»); có ký tự CJK thì khớp chuỗi con.
    Từ khóa kết thúc bằng '-' (vd. «dd-», «dbt-») là tiền tố mã nên không cần ranh giới phải."""
    if any(ord(ch) >= 0x3000 for ch in word):
        return re.compile(re.escape(word))
    tail = "" if word.endswith("-") else r"(?!\w)"
    return re.compile(r"(?<!\w)" + re.escape(word) + tail)


_PATTERNS = {}


def _hits(text, words):
    return [w for w in words if _PATTERNS.setdefault(w, _pattern(w)).search(text)]


def score_complexity(own, parent, kind):
    """Trả về (mức, lý do, độ tin cậy, quy tắc PL đã áp). own / parent đã chữ thường; parent chỉ dùng khi own không có
    dấu hiệu, và (R1) không cho Complexity 5 — bất định phải là của chính item."""
    if kind == "要確認":
        return 2, "2 — R3: issue 要確認 (đi hỏi làm rõ) → Complexity 2.", "cao", ["R3"]
    # Chủ đề NFR của issue cha chỉ tính khi item rơi xuống dùng mô tả cha (trước R1 mới có thể nhận 5 từ đó)
    nfr_own = _hits(own, NFR_TOPIC)
    nfr = nfr_own or _hits(parent, NFR_TOPIC)
    for source, label, top in ((own, "", 5), (parent, " (theo mô tả issue cha)", 4)):
        for level in range(top, 0, -1):
            hits = _hits(source, CX_SIGNALS[level])
            if hits:
                conf = "cao" if len(hits) >= 2 and not label else "vừa"
                quoted = ", ".join(f"«{h}»" for h in hits[:3])
                reason = f"{level} — {COMPLEXITY_SCALE[level]}: dấu hiệu {quoted}{label}."
                note = _r1_note(nfr if label else nfr_own, label and _hits(source, CX_SIGNALS[5])) if level < 5 else ""
                return level, reason + note, conf, ["R1"] if note else []
    note = _r1_note(nfr, _hits(parent, CX_SIGNALS[5]))
    return 2, "2 — mặc định: mô tả không có dấu hiệu rõ về logic." + note, "thấp", ["R1"] if note else []


def _r1_note(nfr, parent_uncertain):
    if nfr:
        return f" R1: «{nfr[0]}» là chủ đề NFR nhưng việc làm theo quy trình xác định → không chấm 5."
    if parent_uncertain:
        return f" R1: dấu hiệu bất định «{parent_uncertain[0]}» thuộc issue cha, không phải kết quả của item này."
    return ""


def score_rough_screen(title, screens):
    """R2: sub-issue 画面設計 / 実装 k/n của màn 概算 → Scope 2, Complexity theo S/M/L của LAB-1. None nếu không áp."""
    m = ROUGH_SCREEN.match(title)
    if not m or not screens:
        return None
    lo = int(m.group(1))
    ids = [f"SCR-{n:02d}" for n in range(lo, int(m.group(2) or lo) + 1)]
    sizes = [screens[i] for i in ids if screens.get(i) in LAB1_LEVEL]
    if not sizes:
        return None
    size = max(sizes, key=lambda x: LAB1_LEVEL.get(x, 0))
    cx = LAB1_LEVEL[size]
    label = ids[0] if len(ids) == 1 else f"{ids[0]}〜{ids[-1]}"
    return {"scope": 2, "complexity": cx, "swp": 2 * cx,
            "reason_scope": f"2 — {SCOPE_SCALE[2]}: R2 — màn 概算, mỗi phần là một thành phần.",
            "reason_complexity": f"{cx} — {COMPLEXITY_SCALE[cx]}: R2 — độ phức tạp màn {label} ở LAB-1 = {size}.",
            "confidence": "vừa", "confidence_note": f"màn 概算 — chấm theo R2 (LAB-1 {label}: {size})", "rules": ["R2"]}


def score_scope(own, kind):
    base = SCOPE_BY_KIND.get(kind)
    if base is None:
        return 2, f"2 — mặc định: loại «{kind}» không có trong thang.", "thấp"
    for kinds, level, words in ([] if kind in SCOPE_FIXED else SCOPE_UP):
        if level <= base or (kinds and kind not in kinds):
            continue
        hits = _hits(own, words)
        if hits:
            quoted = ", ".join(f"«{h}»" for h in hits[:3])
            return level, f"{level} — {SCOPE_SCALE[level]}: loại {kind}, dấu hiệu {quoted}.", "cao" if len(hits) > 1 else "vừa"
    if kind == "要確認":
        return base, f"{base} — {SCOPE_SCALE[base]}: R3 — issue 要確認 (đi hỏi làm rõ).", "cao"
    return base, f"{base} — {SCOPE_SCALE[base]}: theo loại {kind}.", "cao"


def score_leaf(title, kind, body, parent_title="", parent_text="", screens=None):
    """Chấm một item lá. body / parent_text là văn bản issue (hàm tự bỏ dòng giờ).

    parent_title: tiêu đề issue cha — Scope xét thêm (sub-issue là một phần của chức năng cha).
    parent_text: mô tả issue cha — Complexity chỉ dùng khi item không có dấu hiệu. Không truyền mô tả epic (quá rộng).
    screens: {SCR-xx: S/M/L} của LAB-1 cho R2; None = không áp R2.
    """
    own = (title + "\n" + strip_hours(body)).lower()
    parent = strip_hours(parent_text).lower()
    rough = _hits(own + parent, ROUGH_SIGNALS) and score_rough_screen(title, screens)
    if rough:
        return rough
    scope, r_scope, c_scope = score_scope(own + "\n" + parent_title.lower(), kind)
    cx, r_cx, c_cx, rules = score_complexity(own, parent, kind)
    order = ["thấp", "vừa", "cao"]
    conf = order[min(order.index(c_scope), order.index(c_cx))]
    note = ""
    if _hits(own + parent, ROUGH_SIGNALS):
        conf, note = "thấp", "màn chưa có thiết kế (概算) — phạm vi thật chưa rõ"
    return {"scope": scope, "complexity": cx, "swp": scope * cx, "reason_scope": r_scope,
            "reason_complexity": r_cx, "confidence": conf, "confidence_note": note, "rules": rules}
