# AI Report — DRAFT (B1)

> Bản nháp, sẽ bổ sung qua các bước sau. Chỉ ghi phần đã làm.

## 1. Công cụ AI đã dùng

| Công cụ | Dùng để |
|---------|---------|
| Claude Code (Claude Sonnet 5.5) trong VS Code | Dựng repo, viết script, viết khung tài liệu |
| GitHub CLI `gh` (GraphQL API) | Tạo repo, Project, trường, view |

## 2. Prompt và kết quả

### B1 — Dựng repo, Project, nguyên tắc break task (chưa tạo issue)

- **Prompt (tóm tắt):** khởi tạo repo public `skr-fms-backlog`; tạo GitHub Project user-level public với trường Status / Iteration / SWP / giờ ước lượng / 担当(仮) / Type / Constraint và hai view Board + Table; viết script idempotent vào `tools/`; tạo khung 6 file Markdown; viết sẵn nguyên tắc chia task và đề xuất quy tắc quy giờ; `.gitignore`.
- **Cách làm:**
  1. Kiểm tra `gh auth status` (đủ scope `project`, `repo`), kiểm tra repo/Project chưa tồn tại.
  2. `gh repo create --public`; cấu hình git local dùng địa chỉ `noreply` của GitHub để không lộ email.
  3. `gh project create/edit/link` cho Project và liên kết repo.
  4. `gh project field-create` cho trường Single select / Number; **GraphQL** (`createProjectV2Field`, `updateProjectV2Field`, `createProjectV2View`, `updateProjectV2View`) cho Iteration, Status "In Review" và view — `gh` CLI chưa hỗ trợ.
  5. Chạy script 2 lần để xác nhận idempotent; truy vấn lại API và gọi URL ẩn danh để xác nhận công khai.
- **Kết quả:** repo + Project public, đủ trường và hai view; script ở `tools/setup-github-project.sh`.
- **Sự cố gặp phải:** GitHub từ chối tên trường "Type" (reserved) → dùng "Item Type". `gh` CLI không tạo được trường Iteration → dùng GraphQL.

## 3. Quyết định và kiểm chứng của con người

| # | Quyết định | Lý do | Trạng thái |
|---|-----------|-------|-----------|
| 1 | Trường loại item tên "Item Type" thay "Type" | "Type" bị GitHub giữ chỗ | Đã áp dụng — cần PL xác nhận |
| 2 | Sprint 1 bắt đầu 2026-11-02 (thứ Hai), 3 Sprint x 14 ngày, tên có chữ "giả lập" | Ngày giả lập theo đề; tham số hóa trong script | Cần PL xác nhận ngày |
| 3 | Git commit dùng email `noreply` GitHub | Repo public, không lộ dữ liệu cá nhân | Đã áp dụng |
| 4 | Quy tắc quy giờ (mục 2 của `estimate.md`) | Đề xuất nhất quán, đối chiếu 1MD = 7.5h | **Chờ PL duyệt** |
| 5 | Tiêu đề các mục trong khung file là suy đoán từ tóm tắt đề | Chưa có danh sách mục gốc | **PL đối chiếu với đề** |

[PL điền — đánh giá chất lượng đầu ra AI, phần đã sửa tay, bài học.]
