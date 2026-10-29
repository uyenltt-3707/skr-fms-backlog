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
