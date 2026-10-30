---
name: swp-provisional
description: Chấm SWP TẠM (Scope × Complexity) cho item lá của backlog GitHub Project theo mô tả issue, cộng cho cha / epic, chọn issue mẫu cho PL kiểm, xuất báo cáo HTML tự chứa, và (chỉ khi PL đã quyết mọi mẫu + có cờ xác nhận) ghi SWP đã review lên Project. Dùng khi cần chấm / chấm lại SWP, lập báo cáo SWP, hoặc ghi SWP lên Project của repo backlog.
---

# swp-provisional — chấm SWP TẠM

> **「SWP tạm — thang điểm do PL tự đặt, chờ skill chính thức của chương trình; khi có sẽ chạy lại và thay thế」**

## Mục đích

Đề LAB-5 yêu cầu chấm SWP bằng skill (Scope × Complexity → SWP), skill chọn issue mẫu để người kiểm, báo cáo HTML đặt
trong repo, trường point trên Project chỉ ghi SWP đã review. Skill chính thức của chương trình **chưa có** → PL quyết định
dùng skill tự viết này làm bản TẠM.

## Giới hạn (TẠM)

- Thang điểm do PL tự đặt, chưa hiệu chỉnh với dữ liệu thật; luật chấm là **từ khóa có trọng số** trên văn bản issue — tái lập
  được, giải thích được, nhưng không "hiểu" nghiệp vụ. Item không có dấu hiệu rõ nhận điểm mặc định và độ tin cậy **thấp**.
- Item lá thuộc màn chưa có thiết kế (概算) luôn độ tin cậy thấp — phạm vi thật chưa biết.
- Khi skill chính thức có: chạy skill chính thức trên cùng Project, **thay** toàn bộ giá trị SWP; không trộn hai thang.

## Đầu vào

- Repo GitHub có issue dạng epic → issue → sub-issue (sub-issue thật của GitHub) và Project v2 (user-level) có trường số `SWP`,
  `見積時間 / Estimate (hours)`, single-select `Item Type`, `Constraint`.
- `gh` đã đăng nhập (scope `repo`, `project`); Python 3 có PyYAML.
- Mô tả issue: mục `### Mô tả` và `### Tiêu chí xong` (không có thì lấy toàn body trừ dòng metadata). Loại item đọc từ dòng
  `**Loại:** … / <loại>`.

## Đầu ra

| File | Nội dung |
|---|---|
| `swp-report/swp-scores.yaml` | Mọi item lá: Scope, Complexity, SWP, lý do từng trục, độ tin cậy, cờ mẫu + lý do chọn, `pl_final` / `pl_reason` (PL điền); cha / epic: tổng con |
| `swp-report/swp-report-<yymmdd>.html` | Báo cáo tự chứa (không tải tài nguyên ngoài): nhãn TẠM, thang điểm, mẫu cần PL kiểm, phân bố theo epic, kiểm chéo giờ / SWP, bảng mọi item |
| Trường `SWP` trên Project | Chỉ sau khi PL quyết mọi mẫu và chạy `write-swp-to-project.py --confirm` |

## Quy trình

```bash
S=skills/swp-provisional/scripts          # hoặc .claude/skills/swp-provisional/scripts sau khi cài
python $S/issue_snapshot.py --repo OWNER/REPO --project-owner OWNER --project-number N --out tmp/swp-snapshot.json
python $S/score-issues.py --snapshot tmp/swp-snapshot.json --out swp-report/swp-scores.yaml
python $S/render-swp-report.py --scores swp-report/swp-scores.yaml --out swp-report/swp-report-$(date +%y%m%d).html
# DỪNG: PL đọc báo cáo, điền pl_final + pl_reason cho mọi mẫu trong swp-scores.yaml
python $S/score-issues.py ... && python $S/render-swp-report.py ... --out swp-report/swp-report-<yymmdd>-final.html \
  --notes swp-report/cross-check-notes.yaml   # chạy lại: giữ quyết định PL + bộ mẫu + điểm nháp; giữ file nháp để so
python $S/write-swp-to-project.py --scores swp-report/swp-scores.yaml            # dry-run: xem kế hoạch + điểm chặn
python $S/write-swp-to-project.py --scores swp-report/swp-scores.yaml --confirm  # ghi thật
```

Agent dùng skill: chạy 3 lệnh đầu, đọc lại các item độ tin cậy thấp và mẫu để kiểm lý do có hợp mô tả không, báo PL danh sách
mẫu; **không** tự điền `pl_final`, **không** chạy `--confirm` khi PL chưa yêu cầu.

## Thang điểm (PL đã duyệt)

SWP = **Scope × Complexity** (1–25). Chấm **item lá** theo **mô tả issue**, KHÔNG dựa vào số giờ đã ước (dòng 見積時間 bị xóa
khỏi văn bản trước khi chấm; giờ chỉ dùng ở mục kiểm chéo của báo cáo). Issue cha và epic: SWP = **tổng các con**, không chấm riêng.

| Điểm | Scope | Complexity |
|---|---|---|
| 1 | thay đổi rất nhỏ trong 1 thành phần, không đổi giao diện / DB | CRUD thuần |
| 2 | một thành phần (1 API / 1 màn hình đơn giản / 1 bảng) | validation đơn giản, ít trạng thái |
| 3 | hai lớp trong cùng chức năng | nhiều nhánh / state machine, phân quyền |
| 4 | xuyên UI + API + DB trong 1 chức năng hoặc ảnh hưởng nhiều màn hình | logic nghiệp vụ nhiều biến (tiền, làm tròn, kỳ, version quy tắc), nguyên tử / đồng thời |
| 5 | nhiều chức năng, hạ tầng toàn hệ thống, migration | bất định cao — kết quả chưa biết trước: đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt (R1) |

### Bản sửa thang điểm của PL — 2026-10-30 (B3b, sau khi review 14 mẫu)

Áp cho **mọi** item cùng loại (không chỉ mẫu); chạy lại `score-issues.py` là chấm lại toàn bộ. Mỗi item ghi quy tắc đã áp
(`rules`) và giữ điểm nháp đầu tiên (`scope_draft` / `complexity_draft` / `swp_draft`) để so trước / sau.

| # | Quy tắc | Cách luật áp |
|---|---|---|
| R1 | Complexity 5 **chỉ** khi kết quả bất định (đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt). Việc chủ đề NFR nhưng làm theo quy trình xác định → chấm theo độ phức tạp thực tế. | Dấu hiệu mức 5 chỉ còn: 要確認, 未決, chưa chốt, câu hỏi khách, khách trả lời, rto, số đo, đo thời gian, p95. «nfr», «security», «lỗ hổng», «load test», «fig-load», «diễn tập», «restore» thành chủ đề NFR — chỉ ghi chú R1, Complexity lấy theo dấu hiệu mức 4–1. Bất định phải là của **chính item**: mô tả issue cha cho tối đa Complexity 4. |
| R2 | Màn 概算 (画面設計 và 実装 k/n): Scope 2; Complexity theo độ phức tạp màn ở LAB-1: S → 2, M → 3, L → 4. | Item có dấu hiệu 概算 và tiêu đề `[SCR-xx] 画面設計` / `[SCR-xx] 実装 k/n` (mọi n, không chỉ /3); độ phức tạp đọc từ `04_screens.yaml` của LAB-1 (`--lab1-screens`, chỉ đọc; thiếu file → dừng). Màn gộp (SCR-34〜36) lấy mức cao nhất. Độ tin cậy vừa. 結合テスト・概算 không thuộc R2. |
| R3 | Issue 要確認 (đi hỏi làm rõ): Scope 1 × Complexity 2 = 2. | Theo loại item 要確認. |

Mẫu PL đã kiểm: `pl_final` + `pl_reason` (bắt buộc), `pl_scope` / `pl_complexity` (tùy chọn, tích phải = `pl_final`).
Khi PL đã quyết ít nhất một mẫu, chạy lại **giữ nguyên bộ mẫu** (không chọn lại).

Cách luật áp (`scripts/swp_rubric.py`):
- **Scope:** mức cơ sở theo loại item (要確認 / tài liệu 1 · DB / API / UI / hạ tầng / test 2 · batch / thiết kế 3), nâng lên khi
  mô tả có dấu hiệu phạm vi rộng hơn (vd. «rpc» ở API / DB → 3, «dùng chung», «e2e» → 4, «migration», «結合テスト», «dump» → 5).
- **Complexity:** mức cao nhất có dấu hiệu trong mô tả của chính item; không có thì dùng mô tả issue cha (ghi rõ trong lý do);
  vẫn không có → 2, độ tin cậy thấp. Item 要確認 → 2 (R3; trước 2026-10-30 là 5).
- Từ khóa Latin / tiếng Việt khớp theo **ranh giới từ** («view» không khớp «under_review»); từ khóa tiếng Nhật khớp chuỗi con.
  Mỗi từ khóa chỉ nâng một trục, trừ test NFR toàn hệ thống (security, load test, diễn tập restore) — cố ý nâng cả Scope và Complexity.
- **Độ tin cậy:** cao (≥ 2 dấu hiệu, từ chính item) · vừa (1 dấu hiệu hoặc lấy từ issue cha) · thấp (mặc định, màn 概算, hoặc
  issue đã đóng mà không đọc được mô tả ban đầu).
- Mỗi item có lý do 1 câu cho từng trục, nêu dấu hiệu đã khớp.

## Quy tắc chọn mẫu (12–15 item, `scripts/sample_selection.py`)

1. 3 item SWP cao nhất (hòa điểm thì mỗi issue cha một item); 2. 2 item SWP thấp nhất (hòa thì số issue nhỏ hơn);
3. mọi item độ tin cậy thấp — tối đa 5; quá 5 thì ưu tiên item thấp vì **không có dấu hiệu** (lỗi chấm tiềm ẩn) trước item thấp
   vì màn 概算, trong mỗi nhóm chọn ngẫu nhiên và rải mỗi epic một item;
4. đủ ≥ 3 item Constraint = 完納奨励金 (tính cả item đã chọn ở trên);
5. 2 item ngẫu nhiên; bù ngẫu nhiên cho đủ 12. Seed cố định `20261030` → chạy lại ra cùng mẫu khi dữ liệu không đổi.
Mỗi mẫu ghi đủ lý do chọn (một item trúng nhiều quy tắc thì ghi nhiều lý do).

## Quy tắc an toàn

- **Mặc định dry-run.** Chỉ ghi Project khi có cờ `--confirm` **và** mọi mẫu đã có `pl_final` + `pl_reason`.
- Chỉ ghi trường `SWP`; không đụng trường khác. Giá trị lá = `pl_final` (nếu PL chốt) hoặc Scope × Complexity, phải là tích của
  hai số 1–5 → **không** ghi được SP Fibonacci (13, 21…) hay giờ (7.5…) vào trường SWP. Cha / epic = tổng con, tính lại khi ghi.
- **Không ghi đè** SWP của issue đã đóng (trạng thái lấy **live** lúc ghi, mọi cấp lá / cha / epic; tổng của cha cộng giá trị đang
  giữ). Issue đã đóng mà mới chấm → chấm theo **mô tả ban đầu** (bản sửa cũ nhất) và gắn nhãn 「chấm sau khi đóng」 trước khi ghi SWP.
- `pl_final` ngoài tập tích Scope × Complexity → `score-issues.py` dừng ngay, không đưa vào báo cáo.
- Không đọc / in token; mọi lời gọi GitHub qua `gh`. Snapshot để ở `tmp/` (không commit).

## Cài cho Claude Code

`python skills/swp-provisional/scripts/install-skill.py` → copy sang `.claude/skills/swp-provisional/`. Nguồn chuẩn là `skills/`;
sửa ở `skills/` rồi cài lại.
