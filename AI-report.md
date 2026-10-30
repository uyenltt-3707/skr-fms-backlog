# AI Report — LAB-5 (B1〜B5)

Công cụ: Claude Code trong VS Code (B1: Claude Sonnet 5.5 · B2〜B5: Claude Opus 5.5) · GitHub CLI `gh` (REST + GraphQL) · Python 3 (PyYAML, matplotlib).

## 1. Skill và prompt đã dùng

| Việc | Skill / công cụ | Prompt (tóm tắt) | Kết quả |
|---|---|---|---|
| Dựng repo + Project (B1) | Claude Code + `gh` GraphQL | Repo public, Project user-level với Status / Iteration / SWP / giờ / 担当(仮) / Item Type / Constraint, 2 view, script idempotent | `tools/setup-github-project.sh`, Project #2 |
| Break task (B2) | Claude Code; tham khảo `tkm:estimate` → sub-skill `task-breakdown` | "Sửa khung file theo đề; từ `lab5_handoff.yaml` tạo epic / issue / sub-issue tiếng Việt giữ thuật ngữ Nhật; 完納奨励金 tách issue riêng; WU-092〜095 và D33 có bước thiết kế đầu; 担当(仮) theo loại; Sprint 1 = nền tảng vừa sức đội; script idempotent dùng sub-issue thật; kiểm WU, ≤ 15h, cha = tổng con, Constraint, chép nguyên văn" | `tools/backlog.yaml` (263 item), `create-issues.py`, `check-backlog.py`, `scan-content.py` |
| Quy giờ (B2) | Claude Code | "Giữ 8 quy tắc B1, sửa quy tắc 4: cha / epic cũng điền giờ = tổng con, script tự cộng; tổng chỉ cộng lá" | `estimate.md` §3–§5; giờ từng lá ước theo bảng tham chiếu §3 |
| Xếp Iteration (B2) | Script tạm (greedy theo phụ thuộc + trần giờ từng người + tầng ưu tiên nghiệp vụ) | "Sprint 1 = E01, DB lõi, một phần E02 / E03, 6 người × 10 ngày × 7.5h trừ buffer và họp" | Sprint 1 240h / 2 222h / 3 165h; kết quả ghi cứng vào YAML |
| Sửa sau duyệt (B2b) | Claude Code + script tạm (sửa YAML theo cấu trúc dữ liệu, ghi lại cùng định dạng; so LAB-1 đọc thẳng xlsx WBS) | "Thêm màn baseline LAB-1 ngoài 16 màn cốt lõi (画面設計 + 実装, ước thô theo S/M/L LAB-1); so LAB-1 cùng phạm vi bằng bảng quy đổi pha; tách 12 báo cáo E07; +hoàn thiện production cho WU sửa từ prototype; chuyển API đơn giản sang FE, không sprint nào vượt sức, FE không rảnh ở Sprint 3" | 17 issue + 86 sub-issue mới; 2,909.5h; `estimate.md` §5 viết lại |
| Bổ sung issue theo quyết định PL (B3a) | Claude Code + `create-issues.py` | "Test tích hợp theo luồng nghiệp vụ (không theo màn), giờ theo §3, lá ≤ 15h, QA-A; luồng dùng màn ước thô → 概算; E12 thêm security test theo NFR bảo mật LAB-4 + restore lần 2; kiểm load test đo dump có chưa" | 5 luồng #374〜#387, #367, #371; #233 ghi rõ điều kiện ADR-010; +182h |
| Chấm SWP (B3a) | Skill tự viết `skills/swp-provisional/` — 「SWP tạm — thang điểm do PL tự đặt, chờ skill chính thức của chương trình; khi có sẽ chạy lại và thay thế」 | "Skill TẠM: thang Scope × Complexity PL duyệt, chấm lá theo mô tả (không theo giờ), cha = tổng con, lý do + độ tin cậy, chọn 12–15 mẫu theo quy tắc, báo cáo HTML tự chứa, ghi Project mặc định dry-run" | 286 item lá, SWP tạm 2,546, 14 mẫu, `swp-report/swp-report-261030.html` |
| Áp review PL (B3b) | Skill trên, sửa luật | "Ghi NGUYÊN VĂN quyết định PL cho 14 mẫu (`pl_final`, `pl_reason`); thêm 3 quy tắc R1–R3 vào thang điểm (có ngày), áp cho MỌI item cùng loại, chấm lại toàn bộ; đếm item ảnh hưởng theo từng quy tắc, tổng trước / sau; báo cáo bản chốt giữ file nháp; kiểm chéo giờ / SWP theo epic" | 2,546 → 2,516; R1 7 / R2 57 / R3 4 item đổi; `swp-report/swp-report-261030-final.html` |
| Agent ghi SWP lên Project (B3b) | `write-swp-to-project.py` + `tools/check-backlog.py --remote` | "Dry-run trước; PL đồng ý thì `--confirm`; đọc lại bằng API đối chiếu từng item với `swp-scores.yaml`, cha / epic = tổng con; check-backlog: SWP phải CÓ trên mọi item" | Ghi 389 item (286 lá + 103 cha / epic); đọc lại: 0 item cần ghi, 389 / 389 khớp, check ĐẠT |
| Sprint giả lập (B4) | Claude Code + script tự viết `tools/simulate-sprint.py` (module `sprint_sim.py`, `sprint_report_render.py`) | "Iteration Sprint 1 (2026-11-02〜11-15), GHI RÕ giả lập; kịch bản cuối sprint có lý do gắn backlog (BE nút cổ chai, chờ 要確認, giới hạn Supabase, review chậm), không tô hồng; Status trên Project, Done thì đóng issue, không sửa SWP issue đã đóng; script idempotent, lịch sử theo ngày ở `progress-data/sprint1.yaml`" | 29 lá: Done 20 (đóng 20 issue) · In Review 3 · In Progress 5 · Todo 1; cha / epic cộng dồn (48 item ghi); chạy lại 0 thay đổi |
| Báo cáo tiến độ (B4) | Như trên + `tools/check-progress-report.py` | "progress-report.md đúng 4 phần của đề; bảng Trạng thái · Số issue · Tổng SWP · Ghi chú lấy từ Project bằng API, không gõ tay; burndown theo SWP còn lại (lý tưởng vs thực tế) PNG + bảng; rủi ro kèm mốc, hành động, ai / khi nào; phụ lục 5–8 dòng tiếng Nhật gửi khách, không số liệu nội bộ" | Bảng do script điền giữa marker; burndown 281 → 99 SWP; bảng tải Sprint 2 / 3; 7 rủi ro; phụ lục JA |
| Rà báo cáo tiến độ (B4) | Agent `reviewer` (subagent độc lập, không viết báo cáo, tự đọc Project bằng API) | "Đối chiếu progress-report.md với Project: tìm tô hồng, bỏ sót (carry-over, item bị chặn, rủi ro thiếu), câu không có nguồn, số lệch; kiểm phụ lục JA gửi khách được" | `progress-data/review-progress.md` (§2) |
| Hoàn thiện (B5) | Claude Code | "README 5 phần đúng đề; AI-report 3 phần; rà PREMISE / task-breakdown / estimate cho khớp Project; check-backlog --remote, quét repo, request không đăng nhập HTTP 200" | §2 bảng cổng review; kết quả kiểm cuối ở `process_log.md` |

Skill `tkm:estimate` → sub-skill `task-breakdown` (B2) ở chế độ trước-estimate không sinh số giờ → chỉ dùng cấu trúc epic → story → task làm tham khảo; giờ do
quy tắc `estimate.md` §3.

**Skill SWP tạm (`skills/swp-provisional/`)**
- **Vì sao tự viết:** đề yêu cầu chấm SWP bằng skill (Scope × Complexity), skill chọn mẫu cho người kiểm, báo cáo HTML trong repo,
  Project chỉ ghi SWP đã review — skill chính thức của chương trình chưa có. PL quyết dùng bản TẠM, gắn nhãn 「SWP tạm …」 ở SKILL.md,
  YAML, báo cáo; khi có skill chính thức thì chạy lại và thay toàn bộ, không trộn hai thang.
- **Thang điểm:** Scope 1–5 (một thành phần → nhiều chức năng / hạ tầng) × Complexity 1–5 (CRUD → bất định); luật là từ khóa có
  trọng số trên mô tả issue (không nhìn giờ — dòng 見積時間 bị xóa trước khi chấm); cha / epic = tổng con; mỗi trục có lý do 1 câu
  + độ tin cậy. B3b thêm bản sửa của PL R1–R3 (ngày 2026-10-30) — xem §2.
- **Chọn mẫu (14):** 3 SWP cao nhất (rải theo issue cha), 2 thấp nhất, tối đa 5 độ tin cậy thấp (ưu tiên "không dấu hiệu", rải theo
  epic), đủ 3 item 完納奨励金, 2 ngẫu nhiên; seed cố định → tái lập. Khi PL đã quyết, chạy lại **giữ nguyên** bộ mẫu.
- **Cách Agent ghi SWP lên Project:** (1) **dry-run** mặc định — in kế hoạch + điểm chặn, không ghi; (2) **xác nhận** — chỉ ghi khi
  có `--confirm` (PL đồng ý ở B3b) **và** mọi mẫu có `pl_final` + `pl_reason`; giá trị phải là tích Scope × Complexity (không thể là
  giờ hay SP Fibonacci); chỉ ghi trường `SWP`; (3) **chặn issue đã đóng** — trạng thái lấy live mọi cấp, issue đã đóng đã có SWP thì
  không ghi đè, cha cộng giá trị đang giữ; đã đóng mà mới chấm → gắn nhãn 「chấm sau khi đóng」 trước khi ghi (B3b: 0 issue đóng);
  (4) **đọc lại kiểm tra** — chạy lại dry-run phải ra 0 item cần ghi, `check-backlog.py --remote` đối chiếu từng item với
  `swp-scores.yaml` và cha / epic = tổng con thật trên Project.

## 2. Review output AI

**Cổng review theo bước** (số liệu từ `process_log.md` và commit):

| Bước | Commit | Con người review ở đâu | AI tự kiểm / reviewer độc lập | Kết quả |
|---|---|---|---|---|
| B1 dựng repo, Project | `f8ca8aa`, `98f919f` | PL duyệt khung file + 8 quy tắc quy giờ | — | Khung file viết lại theo đề ở B2; sửa quy tắc 4 |
| B2 break + giờ | `b31976a` | PL duyệt backlog | AI: lịch greedy sai ưu tiên, phụ thuộc bước thiết kế ngược, 10 dòng YAML cụt, 7 mô tả trùng nguồn · reviewer: 3 High + 5 Medium | Sửa 7 điểm script; idempotent |
| B2b sửa sau duyệt | `371a2b2`, `75a66e1` | **PL: 3 vấn đề** — thiếu 19 màn baseline, so LAB-1 lệch phạm vi, cân tải BE / FE | AI: FE-A Sprint 3 chỉ 12h → chuyển item | +17 issue màn 概算; so LAB-1 bằng bảng quy đổi pha; FE nhận API đơn giản |
| B3a bổ sung + SWP nháp | `bf1e65b`, `6452d3e` | PL: thiếu test tích hợp theo luồng, security test, restore lần 2 | AI: luật chấm lệch trên dữ liệu thật · reviewer: 1 High + 5 Medium + 5 Low | +23 item; skill sửa hết điểm review |
| B3b review SWP | `8626f4a` | **PL: 14 mẫu** (6 giữ, 1 sửa lý do, 7 đổi) + **R1–R3** | AI: cách cài R1 (bất định của chính item) · reviewer: 1 High + 4 Medium | 2,546 → 2,516; ghi 389 item; PL xác nhận cách cài R1 / R2 (B4 Phần 0) |
| B4 sprint giả lập + báo cáo tiến độ | commit B4/B5 | **PL duyệt báo cáo tiến độ** sau khi đọc kết quả cổng | AI tự kiểm `check-progress-report.py` · reviewer độc lập `review-progress.md` | AI tự kiểm 23 đạt / 0 lệch; reviewer 3 vòng: CHƯA ĐẠT (3 High + 7 Medium + 8 Low) → CHƯA ĐẠT (N1 + 3 Low) → **ĐẠT**; **PL duyệt 2026-10-30 — 受入** |

**Cổng chất lượng báo cáo tiến độ (B4):** (1) **AI tự kiểm đạt** — `tools/check-progress-report.py` sinh lại 5 bảng từ Project
(giống từng ký tự); kiểm 18 câu khẳng định trong lời văn (item bị chặn theo phụ thuộc, đề xuất rút item, ảnh hưởng mốc), tìm nguồn cho mọi con số còn lại (`progress-data/self-check-progress-report.txt`);
(2) **reviewer đạt** — vòng 3 (`progress-data/review-progress.md`, 3 vòng: High / Medium sửa hết); (3) **PL duyệt 2026-10-30 — 受入**. Nhận xét của PL khi duyệt (nguyên văn): «Báo cáo tiến độ do AI tổng hợp có số liệu khớp hoàn toàn với Project nhưng vẫn có câu làm nhẹ rủi ro và một câu tiếng Nhậthứa sai với khách. Số đúng chưa đủ để gửi khách; người phải đọc lại giọng văn và cam kết trước khi gửi.»


| Bước | Ai review | Phát hiện | Xử lý |
|---|---|---|---|
| Khung file B1 | PL | Tiêu đề mục đoán từ tóm tắt đề, không khớp đề | B2 viết lại 6 file theo đúng thứ tự phần của đề |
| Quy tắc quy giờ | PL | Quy tắc 4 bản B1 ("chỉ lá mang giờ") không cho xem tổng trên Project | Sửa: cha / epic điền tổng con do script cộng |
| Lịch Sprint (AI tự kiểm) | AI, chờ PL | Greedy thuần xếp diễn tập DR vào Sprint 2, FS-03 (đường găng) không vào sprint nào; BE-A nhiều hơn BE-B 89h | Thêm tầng ưu tiên nghiệp vụ, để diễn tập DR / E2E / tài liệu API về cuối; chuyển 5 item BE-A → BE-B |
| Phụ thuộc bước thiết kế (AI tự kiểm) | AI | Sub-issue thiết kế kế thừa phụ thuộc của issue cha nên bị xếp **sau** phần cài đặt | Chuyển phụ thuộc xuống sub-issue cài đặt |
| YAML (AI tự kiểm, trước khi tạo issue) | AI | Chuỗi có dấu phẩy trong `{...}` bị YAML cắt — 10 tiêu đề / tiêu chí xong bị cụt (dry-run lộ ra) | Quote toàn bộ 150 dòng; `backlog_model.py` báo lỗi khi gặp khóa lạ |
| Chép nguyên văn (script) | `scan-content.py` | 7 mô tả trùng ≥ 40 ký tự với handoff; câu chân body trùng một câu ở repo LAB-4 | Viết lại; quét lại ĐẠT |
| Script công cụ | Agent `reviewer` (độc lập, chỉ đọc) | POST tạo issue được thử lại khi lỗi 5xx → có thể tạo trùng; in tiếng Việt crash khi stdout chuyển hướng trên Windows; sprint đã kết thúc không còn trong option Iteration; PATCH 2 lần; crash thay vì báo lỗi validate | Sửa 7 điểm; chạy lại `create-issues.py` cho 0 thay đổi (idempotent) |
| Phạm vi backlog (B2) | PL | **Thiếu 19 màn baseline LAB-1** ngoài 16 màn cốt lõi — AI chỉ lấy phạm vi handoff LAB-4, không đối chiếu SP4 LAB-1 | Thêm 17 issue ước thô (PREMISE P1-6, G14) |
| So LAB-1 (B2) | PL | So giờ LAB-5 với riêng I (製造・単体) là **khác phạm vi**: LAB-5 còn gồm một phần 結合テスト và 詳細設計 của màn chưa thiết kế; E07 gộp 12 báo cáo khác định dạng; WU sửa prototype chưa tính hoàn thiện production | Lập bảng quy đổi pha rồi mới so (−29.8%); tách 12 báo cáo; +25% cho 80 item lá (`estimate.md` §3, §5) |
| Cân tải (B2) | PL | AI giữ cứng quy tắc API → BE nên BE nút cổ chai, FE-A rảnh ở Sprint 3 (4h) | Chuyển API đơn giản sang FE; Sprint 3 FE-A 48h / FE-B 45h (`progress-report.md` §4) |
| Toàn bộ backlog, giờ, Iteration (sau B2b) | PL | Thiếu test tích hợp theo luồng, security test, restore lần 2; load test dump chưa ghi rõ là điều kiện ADR-010; BE quá tải | Thêm issue (P3-7, P3-8); BE: không thêm người, hành động có điều kiện ở `progress-report.md` §4 |
| Constraint của issue mới (AI tự kiểm) | AI | Sub-issue lấy Constraint của **epic**, không của issue cha → 2 sub-issue luồng 完納奨励金 bị なし | Ghi Constraint trực tiếp cho sub-issue; đồng bộ lại |
| Luật chấm SWP (AI tự kiểm trên dữ liệu giả lập rồi dữ liệu thật) | AI | Tài liệu / 要確認 bị nâng Scope 5 vì nói về hạ tầng; mô tả **epic** làm ngữ cảnh đẩy Complexity của item lá lên 5; «hiển thị» (mức 1) át 確定 / 提出; 5 mẫu tin cậy thấp đều là màn 概算 | Khóa Scope cho tài liệu / 要確認; chỉ lấy mô tả issue cha (không lấy epic); thêm dấu hiệu; ưu tiên mẫu "không dấu hiệu" |
| Script skill (B3a) | Agent `reviewer` (độc lập, chỉ đọc) | High: chặn ghi đè SWP issue đã đóng chỉ xét item lá và dùng trạng thái cũ. Medium: nhãn 「chấm sau khi đóng」 mất khi chạy lại sau lỗi; tổng cha lệch khi con bị giữ nguyên; từ khóa khớp chuỗi con («view» trong «under_review»); một từ khóa nâng cả hai trục → top-3 dồn một cụm; thiếu mô tả gốc không cảnh báo | Sửa hết: trạng thái live mọi cấp, gắn nhãn trước khi ghi, cha cộng giá trị đang giữ, khớp theo ranh giới từ, tách từ khóa (trừ test NFR), top-3 rải theo issue cha, cảnh báo + độ tin cậy thấp; kiểm `pl_final` sớm; dry-run vẫn chặn ghi |
| **SWP nháp — 14 mẫu (B3b)** | **PL** | 6 / 14 mẫu giữ nguyên. **#175** tổng 8 đúng nhưng **lý do sai**: skill cho Scope 4 (thấy «dùng chung», «mọi màn») × Complexity 2 (không thấy dấu hiệu) — thật ra là 1 hàm DB (Scope 2) với logic nhiều biến (Complexity 4). **#207** thiếu Complexity: tải CSV kiểm / báo lỗi từng dòng, chặn khi 確定, phân quyền → 3 × 3. **#243** skill coi "NFR / load test" = bất định → 25; PL: tạo dữ liệu + kịch bản là việc xác định → 15. 5 mẫu màn 概算 (#271, #307, #308, #342, #359) chấm theo từ khóa ra 2–12, không theo cỡ màn. Giữ #234 / #241 (25) vì bất định thật — #241 do phụ thuộc bên ngoài mà mô tả không ghi | Ghi nguyên văn `pl_final` / `pl_reason` (+ `pl_scope` / `pl_complexity`) |
| **Lỗi có hệ thống rút ra từ mẫu (B3b)** | **PL** | Ba lỗi lặp ở nhiều item, không chỉ mẫu: (R1) từ khóa NFR / security / restore / load test bị coi là bất định → Complexity 5; (R2) màn 概算 chấm theo từ khóa trong tiêu đề phần 1/3, 2/3… thay vì cỡ màn đã có ở LAB-1; (R3) issue 要確認 bị chấm Complexity 5 dù việc chỉ là đi hỏi | PL đặt 3 quy tắc R1–R3 (thang điểm có ngày trong `SKILL.md`), AI cài vào luật, chấm lại toàn bộ: R1 đổi 7 item (135 → 79), R2 57 / 73 (427 → 452), R3 4 (20 → 8), PL chốt mẫu +13; tổng 2,546 → 2,516. Kiểm chéo theo epic: E05 / E06 hết vượt ±50% |
| Cài R1 thành luật (AI tự kiểm) | AI | Chỉ bỏ từ khóa NFR khỏi mức 5 vẫn để #240 / #372 (viết thủ tục restore) ở 5 vì mô tả issue cha có «RTO» | Bất định phải của chính item: mô tả cha cho tối đa 4 — ghi rõ để PL xác nhận (`estimate.md` §2) |
| Script B3b | Agent `reviewer` (độc lập, chỉ đọc) | High: item không có dấu hiệu, issue cha nói NFR → đổi điểm mà không gắn R1. Medium: mẫu cũ rời ảnh chụp → crash; `pl_complexity` trống → crash; ảnh hưởng quy tắc trộn với ghi đè của PL (#241 trông như R1 không đổi); check-backlog báo sai khi issue đã đóng giữ SWP cũ | Sửa hết; tách 2 bước (quy tắc → PL chốt) trong bảng ảnh hưởng; chạy lại: 0 item đổi mà không có quy tắc / quyết định PL, Project 0 item cần ghi |

| Mô tả issue #241 (B4 Phần 0) | **PL** | PL giữ #241 = 25 vì phụ thuộc bên ngoài (giới hạn Supabase: không chọn được region backup, không có region Osaka) — nhưng mô tả issue không ghi, nên skill chấm theo từ khóa chỉ cho 10. **Bài học chất lượng ticket:** điều làm việc bất định phải viết ở chính mô tả item | Bổ sung mô tả #241 (qua `backlog.yaml` → `create-issues.py`, chỉ #241 đổi); KHÔNG đổi SWP đã ghi; ghi bài học vào `SKILL.md` |
| Xác nhận cách cài R1–R2 (B4 Phần 0) | **PL** | Đồng ý: bất định phải ở chính item (cha cho tối đa 4); R2 áp mọi 実装 k/n; SCR-34〜36 lấy mức cao nhất; 結合テスト・概算 không áp R2 | Ghi "PL đã xác nhận 2026-10-30" ở `estimate.md` §2, `SKILL.md` |
| Kịch bản Sprint 1 (AI tự kiểm) | AI | Lần chạy thật đầu: Project ghi xong nhưng điền bảng lỗi vì regex marker không nhận khối rỗng; ảnh thiếu glyph 〜 | Sửa regex, đổi ký tự; chạy lại: 0 item cần ghi (idempotent), bảng / ảnh sinh lại |
| progress-report.md (AI tự kiểm, `check-progress-report.py`) | AI | 1 LỆCH: dòng carry-over nhắc «#14» làm lý do → danh sách #số không đúng 9 item. Lời văn: «Ngày 2–5 bám gần» trong khi lệch tăng mỗi ngày (+35 → +54); «BE-B Done thấp nhất» sai (QA-A 0%). Lỗi của chính script kiểm: số dính đơn vị («1,096h») bị cắt thành «1» nên báo có nguồn | Sửa lời văn; thêm kiểm "lệch tăng mỗi ngày"; sửa bộ tách số, đánh dấu số nhỏ ≤ 10 là khớp yếu; thay «≈ 1,096h» bằng số có nguồn (543h + 553h). Kết quả: 12 đạt, 0 lệch |
| progress-report.md — vòng 1 (B4) | Agent `reviewer` (độc lập, tự đọc 389 item Project bằng API) | Số liệu khớp hết (trạng thái, giờ, burndown, 20 issue đóng = Done); nhãn giả lập rõ. **CHƯA ĐẠT: 3 High** — (1) không nói Sprint 2 vượt trần khi nhận carry-over (319.5h / 292.5h, BE-B 76h); (2) phụ lục JA 「合意済みの前提」 hứa sai với khách (P2-3 là giả định nội bộ); (3) chuỗi ADR-010 thiếu I-075 (#230, #231 FE-B Sprint 2) → không nói quyết định B′ / B có thể trễ. **7 Medium** — nguyên nhân BE (xếp 99–100% trần), câu không nguồn («người review duy nhất»), thiếu item bị chặn (#188, #189, #226…), lời văn nhẹ («không do một item lớn»: 3 item giữ 57% SWP còn), bỏ qua tín hiệu ước thiếu (#14, #243, chuỗi DR giờ / SWP thấp), JA dòng 1 lạc quan, không có kết luận / ảnh hưởng mốc. **8 Low** (#165 là cha của #166, 25% không nguồn, lý do #244 sai, 11-10 thu hẹp, …) | AI kiểm lại bằng dữ liệu → đúng cả 3 High. Sửa hết: bảng tải Sprint 2 sinh từ Project + hành động rút item cụ thể; viết lại JA; thêm I-075 và ảnh hưởng NFR-AVL-03; kết luận đầu §2; dòng item bị chặn; ghi chú nguồn vào `sprint1.yaml`; script tự kiểm thêm 6 kiểm câu khẳng định (18 đạt, 0 lệch) |
| progress-report.md — vòng 2 | Agent `reviewer` | 3 High đã đóng (tự tính lại tải Sprint 2, kiểm item rút không có item phụ thuộc). Còn: Medium — ảnh hưởng mốc chưa có con số; **mới N1** — rút item sang Sprint 3 làm Sprint 3 vượt trần (FE-A 58, FE-B 61, BE-A 60) → quá tải chỉ dời đi; Low — ghi chú nội bộ nằm trong phụ lục gửi khách; ô «Vượt» dòng Tổng khác cách tính; **ghi chú SCR-28 gắn nhầm cho #23** (lỗi thay chuỗi của AI: `replace` áp mọi chỗ trùng lịch sử) | Đề xuất rút item thành dữ liệu (`replan_push_to_sprint3`) → bảng tải Sprint 3 sinh từ Project; câu ảnh hưởng mốc «87.5h ≈ 0.3 sprint, lùi ≥ ~0.3 sprint, dồn vào BE»; chuyển ghi chú ra ngoài phụ lục; dòng Tổng ghi cả vượt cộng từng người và ròng; xóa ghi chú ở #23; tự kiểm thêm kiểm đề xuất rút + 0.3 sprint (22 đạt, 0 lệch) |
| progress-report.md — vòng 3 | Agent `reviewer` | **ĐẠT.** Kiểm lại N1〜N4 bằng API + `backlog.yaml`; còn 2 Low: «0.3 sprint» chưa nói cách tính (chỉ là mức tối đa), chưa nói ai gánh phần vượt cuối (BE-B 23.5h) | Viết lại câu ảnh hưởng mốc: tối đa ~0.3 sprint, BE-B gánh phần vượt cuối, mốc lùi giữa ~0.1 và 0.3 sprint; tự kiểm thêm kiểm này (23 đạt, 0 lệch) |

## 3. Điểm đặc biệt

**Hiệu quả**
- **Một nguồn dữ liệu → mọi nơi:** `tools/backlog.yaml` sinh issue, trường Project, mapping và bảng tài liệu; chạy lại không tạo trùng.
  Sửa mô tả #241 chỉ cần sửa YAML + chạy đồng bộ (1 issue đổi).
- **Số liệu báo cáo không gõ tay:** bảng trạng thái, bảng 担当, burndown do script đọc Project rồi điền vào `progress-report.md`;
  script tự kiểm sinh lại và so từng ký tự → báo cáo không lệch Project.
- **Chốt an toàn khi AI ghi lên Project:** dry-run mặc định, `--confirm`, đọc lại, chặn ghi SWP issue đã đóng; sprint giả lập không đụng
  trường SWP và `check-backlog.py` xác nhận SWP 389 / 389 vẫn khớp sau khi đóng 20 issue. Giới hạn: chốt chặn nằm ở script, còn
  tài khoản thì dùng chung — tài khoản có quyền project ghi được cả Project dự án thật → khi làm thật tách tài khoản / quyền (Nhận xét của PL).
- **Hai lớp review khác nhau bắt lỗi khác nhau:** script bắt sai số / lệch nguồn; reviewer độc lập bắt tô hồng và bỏ sót; PL bắt lỗi
  phạm vi (19 màn, so LAB-1) mà cả AI lẫn reviewer không thấy vì chỉ đọc nguồn được giao.

**Chưa tốt, cần cải thiện khi làm thật** (kèm lý do chưa làm)

| Điểm | Cần làm khi làm thật | Lý do chưa làm |
|---|---|---|
| SWP là **SWP tạm** do skill tự viết, thang điểm PL đặt | Chạy lại toàn bộ bằng skill chính thức của chương trình, thay hết, không trộn hai thang | Chưa có skill chính thức (chưa có giải pháp) |
| Chấm SWP theo **từ khóa** → phụ thuộc chất lượng mô tả ticket (#241: phụ thuộc Supabase không ghi → luật cho 10 thay vì 25) | Mẫu ticket bắt buộc mục "Bất định / phụ thuộc ngoài"; người làm chấm lại (planning poker) và đối chiếu | Thời gian: 286 item, PL chỉ kiểm 14 mẫu + 3 quy tắc |
| **Sprint là giả lập**: kịch bản do AI viết theo hướng PL, không có tiến độ thật | Lấy Status từ hoạt động thật (PR, review), burndown từ lịch sử thật | Bài làm trước khi sprint bắt đầu (chưa có giải pháp trong phạm vi bài) |
| **Thiếu dữ liệu velocity thật** — điều kiện "thêm 1 BE từ Sprint 4" và rủi ro −25.4% so LAB-1 chưa kiểm được | Ghi giờ thực tế từng item từ Sprint 2; epic lệch quá 25% thì ước lại phần còn lại (`estimate.md` §3 quy tắc 9); kiểm lại ước tính và quy tắc SWP bằng dữ liệu thực tế trước khi cam kết tiến độ với khách (Nhận xét của PL) | Chưa có dữ liệu thật |
| Project không lưu lịch sử Status theo ngày → burndown lấy ngày Done từ YAML, chỉ SWP và trạng thái cuối đọc từ Project | Dùng lịch sử thật (sự kiện issue / Project) hoặc chụp số liệu hằng ngày bằng job | Thời gian; Projects API không trả lịch sử trường |
| Tự kiểm số trong lời văn là **khớp theo giá trị**: số nhỏ (≤ 10) hay số trùng ngẫu nhiên vẫn "có nguồn" | Gắn nguồn tường minh cho từng câu (vd. chú thích ID số liệu) | Token / thời gian; reviewer độc lập bù phần ngữ nghĩa |
| Giờ do AI đề xuất cho item lá; PL duyệt quy tắc, chưa duyệt từng con số; lịch Sprint xếp bằng thuật toán | Người làm từng phần ước lại; xếp sprint ở planning có cả đội | Thời gian |
| AI bám nguồn được giao (handoff), không tự đối chiếu baseline LAB-1 (B2b) | Đưa bước "đối chiếu phạm vi với SP4" và "bảng quy đổi pha" vào prompt ngay từ đầu | Đã rút bài học, áp từ B3 |

## Nhận xét của PL

- AI tách 95 đơn vị bàn giao thành 389 item rất nhanh và giữ được truy vết, nhưng bản đầu bỏ sót các màn ngoài 16 màn cốt lõi
  và so với LAB-1 theo hai phạm vi khác nhau. Hai lỗi này chỉ lộ ra khi tôi đối chiếu tổng giờ với estimate cũ.
- Skill SWP tạm chấm theo từ khóa nên phụ thuộc chất lượng mô tả ticket. Kiểm 14 mẫu giúp tôi thấy lỗi lặp theo kiểu,
  và sửa bằng quy tắc (R1–R3) hiệu quả hơn sửa từng issue. Ticket ghi thiếu thông tin (như #241) thì không skill nào chấm đúng.
- Báo cáo tiến độ do AI tổng hợp có số liệu khớp hoàn toàn với Project nhưng vẫn có câu làm nhẹ rủi ro và một câu tiếng Nhật
  hứa sai với khách. Số đúng chưa đủ để gửi khách; người phải đọc lại giọng văn và cam kết trước khi gửi.
- Cho AI Agent ghi thẳng lên Project hiệu quả khi có chạy thử (dry-run), xác nhận và đọc lại để đối chiếu. Khi làm thật, tôi sẽ
  tách tài khoản hoặc quyền, vì cùng một tài khoản có quyền project cũng ghi được vào Project của dự án thật.
- Sprint 1 là giả lập nên chưa có velocity thật. Ước tính và quy tắc SWP cần được kiểm lại bằng dữ liệu thực tế (KPI Insight)
  trước khi dùng để cam kết tiến độ với khách.
