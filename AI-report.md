# AI Report — LAB-5 (nháp, cập nhật đến B2)

Công cụ: Claude Code trong VS Code (B1: Claude Sonnet 5.5 · B2: Claude Opus 5.5) · GitHub CLI `gh` (REST + GraphQL) · Python 3 (PyYAML).

## 1. Skill và prompt đã dùng

| Việc | Skill / công cụ | Prompt (tóm tắt) | Kết quả |
|---|---|---|---|
| Dựng repo + Project (B1) | Claude Code + `gh` GraphQL | Repo public, Project user-level với Status / Iteration / SWP / giờ / 担当(仮) / Item Type / Constraint, 2 view, script idempotent | `tools/setup-github-project.sh`, Project #2 |
| Break task (B2) | Claude Code; tham khảo `tkm:estimate` → sub-skill `task-breakdown` | "Sửa khung file theo đề; từ `lab5_handoff.yaml` tạo epic / issue / sub-issue tiếng Việt giữ thuật ngữ Nhật; 完納奨励金 tách issue riêng; WU-092〜095 và D33 có bước thiết kế đầu; 担当(仮) theo loại; Sprint 1 = nền tảng vừa sức đội; script idempotent dùng sub-issue thật; kiểm WU, ≤ 15h, cha = tổng con, Constraint, chép nguyên văn" | `tools/backlog.yaml` (263 item), `create-issues.py`, `check-backlog.py`, `scan-content.py` |
| Quy giờ (B2) | Claude Code | "Giữ 8 quy tắc B1, sửa quy tắc 4: cha / epic cũng điền giờ = tổng con, script tự cộng; tổng chỉ cộng lá" | `estimate.md` §3–§5; giờ từng lá ước theo bảng tham chiếu §3 |
| Xếp Iteration (B2) | Script tạm (greedy theo phụ thuộc + trần giờ từng người + tầng ưu tiên nghiệp vụ) | "Sprint 1 = E01, DB lõi, một phần E02 / E03, 6 người × 10 ngày × 7.5h trừ buffer và họp" | Sprint 1 240h / 2 222h / 3 165h; kết quả ghi cứng vào YAML |
| Sửa sau duyệt (B2b) | Claude Code + script tạm (sửa YAML theo cấu trúc dữ liệu, ghi lại cùng định dạng; so LAB-1 đọc thẳng xlsx WBS) | "Thêm màn baseline LAB-1 ngoài 16 màn cốt lõi (画面設計 + 実装, ước thô theo S/M/L LAB-1); so LAB-1 cùng phạm vi bằng bảng quy đổi pha; tách 12 báo cáo E07; +hoàn thiện production cho WU sửa từ prototype; chuyển API đơn giản sang FE, không sprint nào vượt sức, FE không rảnh ở Sprint 3" | 17 issue + 86 sub-issue mới; 2,909.5h; `estimate.md` §5 viết lại |
| Chấm SWP | — | B3 | — |
| Agent ghi SWP lên Project | — | B3 | — |
| Báo cáo tiến độ | — | B4 | — |

Skill `task-breakdown` ở chế độ trước-estimate không sinh số giờ → chỉ dùng cấu trúc epic → story → task làm tham khảo; giờ do
quy tắc `estimate.md` §3.

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
| Toàn bộ backlog, giờ, Iteration (sau B2b) | PL — **chưa** | — | Chờ PL review trước B3 |

## 3. Điểm đặc biệt

- **Hiệu quả:** một file YAML là nguồn duy nhất → issue, trường Project, mapping và bảng trong tài liệu sinh từ đó; chạy lại không
  tạo trùng. Script quét chép nguyên văn bắt được lỗi mà đọc bằng mắt khó thấy (câu quen dùng trùng repo nguồn).
- **Chưa tốt, cần cải thiện khi làm thật:** giờ do AI đề xuất cho 184 item lá, PL mới duyệt quy tắc chứ chưa duyệt từng con số —
  khi làm thật cần người làm từng phần ước lại (planning poker) và đối chiếu SWP. Lịch Sprint xếp bằng thuật toán nên bộc lộ nút cổ
  chai BE nhưng chưa tối ưu tải FE. So LAB-1 lệch −41.6% chủ yếu do phạm vi — cần PL xác nhận cách so.
- **Bài học B2b:** AI bám đúng nguồn được giao (handoff) nhưng không tự đối chiếu với baseline LAB-1, và so số liệu khi chưa định nghĩa
  phạm vi tương đương — cần đưa bước "đối chiếu phạm vi với SP4" và "bảng quy đổi pha" vào prompt ngay từ đầu.
- **Chưa có ý tưởng:** cách tự động kiểm "giờ hợp lý" ngoài khoảng tham chiếu — để B3 dùng SWP kiểm chéo.
