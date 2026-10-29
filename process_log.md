# Process Log

Nhật ký thao tác theo thời gian. Cột Giờ là **xấp xỉ** (UTC+7), không phải mốc đo chính xác.

## 2026-10-29 — B1: dựng repo, Project, khung tài liệu

| Giờ | Việc | Kết quả |
|-----|------|---------|
| 19:07 | Nhận yêu cầu B1 | — |
| 19:08 | Kiểm tra `gh auth status`, repo và Project hiện có | Đã đăng nhập, scope `gist, project, read:org, repo, workflow`; chưa có repo `skr-fms-backlog` |
| 19:10 | `git init -b main`; cấu hình git local (email noreply) | OK |
| 19:11 | `gh repo create skr-fms-backlog --public` | https://github.com/uyenltt-3707/skr-fms-backlog |
| 19:15 | Khảo sát GraphQL schema: Iteration, view | `gh` CLI không tạo được Iteration → dùng GraphQL |
| 19:20 | Viết `tools/setup-github-project.sh`, chạy lần 1 | Lỗi: tên trường "Type" bị reserved |
| 19:22 | Đổi thành "Item Type", chạy lại | Tạo Project #2 + trường + view |
| 19:24 | Chạy lần 3 kiểm tra idempotent | Tất cả báo "exists", không tạo trùng |
| 19:25 | Xác minh: field/option/iteration/view qua API; URL ẩn danh | Project `public=true`, HTTP 200 |
| 19:30 | Viết `.gitignore`, khung 6 file Markdown, `AI-report.md`, `process_log.md` | OK |

Chưa làm (đợi LAB-4): issue chi tiết, SWP, giờ, báo cáo Sprint.

## 2026-10-29 — B2: sửa khung file, tạo epic / issue / sub-issue, ước giờ

| Giờ | Việc | Kết quả |
|-----|------|---------|
| 21:18 | Nhận yêu cầu B2 | — |
| 21:19 | Đọc handoff LAB-4 (`lab5_handoff.yaml/.md`), `decisions.md`, `design_risks.md`, `open_questions.md`; `git log` commit `576480b` | 95 WU, 13 epic; nguồn 2026-10-29 20:58 +07:00 |
| 21:20 | Đọc estimate LAB-1 (`06_estimate_wbs_cost_internal.xlsx`) | I = 406.5 MD, tổng 1,539.9 MD |
| 21:21 | Rà spec nghi có chỗ hở: ADR README 未決, DBT-28/29, SCR-16 | Xác nhận G5–G7 (`task-breakdown.md` §4) |
| 21:22 | Xem sub-skill `tkm:estimate/task-breakdown` | Chế độ trước-estimate không sinh giờ → chỉ tham khảo cấu trúc |
| 21:24 | Viết `tools/backlog.yaml` (263 item, giờ từng lá) | 1,780h |
| 21:27 | Xếp Iteration bằng script tạm (greedy) | Lần 1 sai ưu tiên, BE-A quá tải → thêm tầng ưu tiên, chuyển 5 item sang BE-B; phát hiện bước thiết kế kế thừa phụ thuộc cha → sửa |
| 21:30 | Viết `backlog_model.py`, `github_api.py`, `project_fields.py`, `create-issues.py`, `check-backlog.py`, `scan-content.py` | check cục bộ ĐẠT |
| 21:32 | `scan-content.py` lần 1 | 277 phát hiện (7 mô tả + câu chân body trùng nguồn) → viết lại → ĐẠT |
| 21:33 | `create-issues.py --dry-run` | Lộ lỗi YAML cắt chuỗi có dấu phẩy (10 dòng) → quote 150 dòng, thêm kiểm khóa lạ |
| 21:34 | `create-issues.py` chạy thật (nền) | xem dòng kế tiếp |
| 21:36 | Viết PREMISE.md, task-breakdown.md, estimate.md, README.md, progress-report.md, AI-report.md theo khung đề | — |
| 21:45 | Agent `reviewer` rà độc lập 6 script (chỉ đọc) | 3 High (POST retry 5xx có thể tạo trùng, lỗi mã hóa stdout Windows, option Iteration đã xong) + 5 Medium → sửa 7 điểm |
| 22:20 | `create-issues.py` chạy thật xong | 263 issue, 250 liên kết sub-issue, 263 item Project; không bị rate limit |
| 22:26 | Chạy lại `create-issues.py` | 0 thay đổi → idempotent |
| 22:27 | Điền số issue vào tài liệu; `check-backlog.py --remote`; `scan-content.py` | ĐẠT; Project + 3 issue mẫu HTTP 200 khi không đăng nhập; quét bắt 2 câu trích đường dẫn → viết lại → ĐẠT |
