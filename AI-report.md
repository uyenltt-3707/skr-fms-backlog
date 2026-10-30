# AI Report — LAB-5 (nháp, cập nhật đến B3b)

Công cụ: Claude Code trong VS Code (B1: Claude Sonnet 5.5 · B2〜B3a: Claude Opus 5.5) · GitHub CLI `gh` (REST + GraphQL) · Python 3 (PyYAML).

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
| Báo cáo tiến độ | — | B4 | — |

Skill `task-breakdown` ở chế độ trước-estimate không sinh số giờ → chỉ dùng cấu trúc epic → story → task làm tham khảo; giờ do
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

## 3. Điểm đặc biệt

- **Hiệu quả:** một file YAML là nguồn duy nhất → issue, trường Project, mapping và bảng trong tài liệu sinh từ đó; chạy lại không
  tạo trùng. Script quét chép nguyên văn bắt được lỗi mà đọc bằng mắt khó thấy (câu quen dùng trùng repo nguồn).
- **Chưa tốt, cần cải thiện khi làm thật:** giờ do AI đề xuất cho 184 item lá, PL mới duyệt quy tắc chứ chưa duyệt từng con số —
  khi làm thật cần người làm từng phần ước lại (planning poker) và đối chiếu SWP. Lịch Sprint xếp bằng thuật toán nên bộc lộ nút cổ
  chai BE nhưng chưa tối ưu tải FE. So LAB-1 lệch −41.6% chủ yếu do phạm vi — cần PL xác nhận cách so.
- **Bài học B2b:** AI bám đúng nguồn được giao (handoff) nhưng không tự đối chiếu với baseline LAB-1, và so số liệu khi chưa định nghĩa
  phạm vi tương đương — cần đưa bước "đối chiếu phạm vi với SP4" và "bảng quy đổi pha" vào prompt ngay từ đầu.
- **Chưa có ý tưởng:** cách tự động kiểm "giờ hợp lý" ngoài khoảng tham chiếu — B3a dùng SWP kiểm chéo, nhưng 105 / 286 item lệch
  quá ±50% (44 là màn 概算): luật từ khóa không phân biệt được cỡ các phần 1/3, 2/3, 3/3 của cùng một màn → kiểm chéo mức item
  còn nhiễu; mức epic dùng được (E05, E06 vượt ngưỡng).
- **Giới hạn skill TẠM:** chấm bằng từ khóa — tái lập và giải thích được, nhưng không hiểu nghiệp vụ; độ tin cậy "thấp" là để PL
  kiểm, không phải để bỏ qua. Khi có skill chính thức thì chạy lại và thay toàn bộ.
