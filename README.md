SKR-FMS Backlog · Mã học viên: [PL điền] · Đề: Product A (LAB-5)

# SKR-FMS Backlog

> Repo và GitHub Project này **công khai**. Chỉ chứa nội dung tự viết: không chép RFP, không dữ liệu thật, không dữ liệu cá nhân, không khóa bí mật.
> **Sprint và người phụ trách (担当(仮)) là GIẢ LẬP** cho bài tập — không phản ánh lịch hay nhân sự thật.

## 1. Giới thiệu

[PL điền — mục tiêu bài LAB-5, phạm vi Product A, kết quả mong đợi, ràng buộc 完納奨励金 phải là task riêng.]

## 2. Liên kết

| Mục | URL |
|-----|-----|
| Repo | https://github.com/uyenltt-3707/skr-fms-backlog |
| GitHub Project "SKR-FMS Backlog" | https://github.com/users/uyenltt-3707/projects/2 |

## 3. Cấu trúc repo

| File / thư mục | Nội dung |
|----------------|----------|
| `README.md` | Tổng quan, liên kết, cách đọc repo (file này) |
| `PREMISE.md` | Tiền đề và giả định |
| `task-breakdown.md` | Nguyên tắc chia task, cây epic → issue → sub-issue |
| `estimate.md` | Cách quy ra giờ, SWP đã review, tổng hợp |
| `progress-report.md` | Báo cáo tiến độ Sprint giả lập |
| `AI-report.md` | Báo cáo sử dụng AI (công cụ, prompt, quyết định) |
| `process_log.md` | Nhật ký thao tác theo thời gian |
| `tools/` | Script dựng GitHub Project (chạy lại được) |
| `[PL điền: thư mục báo cáo HTML của skill chấm SWP]` | Báo cáo HTML chấm SWP |
| `skills/` | Skill đã dùng (nếu có) |

## 4. Cách đọc GitHub Project

Hai view: **Board** (cột theo Status) và **Table** (lọc/sắp xếp theo mọi trường).

| Trường | Kiểu | Giá trị / ý nghĩa |
|--------|------|-------------------|
| Status | Single select | Todo · In Progress · In Review · Done |
| Iteration | Iteration | Sprint 1–3, 2 tuần/sprint; Sprint 1 bắt đầu 2026-11-02 (**ngày giả lập**) |
| SWP | Number | Chỉ ghi SWP **đã review**; để trống khi chưa review |
| 見積時間 / Estimate (hours) | Number | Giờ ước lượng của từng issue (quy tắc: `estimate.md`) |
| 担当(仮) | Single select | FE-A · FE-B · BE-A · BE-B · QA-A · PM — người phụ trách **giả định**, không gán tài khoản thật |
| Item Type | Single select | Epic · Issue · Sub-issue |
| Constraint | Single select | 完納奨励金 · なし — dùng để lọc hạng mục bắt buộc tách riêng |

> Tên trường loại item là **Item Type** thay vì "Type": GitHub giữ chỗ tên "Type" (reserved), không tạo được.

Dựng lại Project: `bash tools/setup-github-project.sh` (cần `gh` đã đăng nhập, scope `project` + `repo`; chạy nhiều lần không tạo trùng).

## 5. Trạng thái hiện tại

- [x] B1: repo, Project, trường, view, khung tài liệu
- [ ] Issue chi tiết — đợi file bàn giao từ LAB-4
- [ ] SWP đã review · giờ ước lượng · báo cáo Sprint
