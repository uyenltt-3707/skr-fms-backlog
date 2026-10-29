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

## 2026-10-29 — B2b: sửa 3 vấn đề PL phát hiện khi duyệt B2

| Giờ | Việc | Kết quả |
|-----|------|---------|
| 22:34 | Nhận yêu cầu B2b; kiểm git (commit B2 `b31976a` đã push, `.gitignore` có `__pycache__/`, `*.pyc`) | — |
| 22:35 | Đọc SP4 LAB-1 `04_screens.yaml` | 22 màn baseline ngoài 16 màn cốt lõi; SCR-20 / 26 / 28 đã có issue → 19 màn thiếu (17 issue, gộp 34〜36) |
| 22:36 | Rà 49 WU "sửa từ prototype" (80 item lá, 784h) | +25% hoàn thiện production = +166.5h; 3 lá vượt 15h → tách sub-issue |
| 22:37 | Chuyển sửa YAML sang dạng dữ liệu + ghi lại cùng định dạng (kiểm round-trip: giống hệt, dry-run 0 thay đổi) | — |
| 22:38 | Áp thay đổi: 17 issue màn ước thô, tách 12 báo cáo E07, hoàn thiện production, chuyển API đơn giản sang FE | 366 item, 2,909.5h |
| 22:39 | Xếp lại Iteration | Lần 1 FE-A Sprint 3 = 12h → chuyển I-054 (API soạn version) sang FE-A, I-078.1 sang FE-B → S3 FE-A 48h / FE-B 45h; check ĐẠT |
| 22:40 | `create-issues.py` đồng bộ (nền) | xem dòng sau |
| 22:41 | So LAB-1 cùng phạm vi: đọc 102 dòng I của WBS xlsx, gán epic, lập bảng quy đổi pha | 552.2 vs 387.9 MD (−29.8%) |
| 22:43 | Cập nhật PREMISE, task-breakdown, README, estimate, progress-report, AI-report | — |
| 23:00 | Đồng bộ GitHub xong; chạy lại | 103 issue mới, 127 cập nhật, 103 liên kết sub-issue, trường 228 item; lần 2: 0 thay đổi |
| 23:03 | Điền số issue vào tài liệu; `check-backlog.py --remote`; `scan-content.py` | ĐẠT (366 item khớp Project, ẩn danh HTTP 200); quét ĐẠT |
