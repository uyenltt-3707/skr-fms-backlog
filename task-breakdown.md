# Task Breakdown — Product A

## 1. Nguyên tắc chia task

### 1.1 Độ hạt

- Một **issue ≤ 2 ngày công** (= 15 giờ theo 1 MD = 7.5h).
- Lớn hơn 2 ngày công → **tách thành sub-issue**; mỗi sub-issue cũng phải ≤ 2 ngày công.
- Một issue = một kết quả kiểm chứng được, một người phụ trách (担当(仮)).
- Hạng mục **完納奨励金** luôn là issue riêng (không gộp vào issue khác), gắn `Constraint = 完納奨励金`.

### 1.2 Định nghĩa xong (Definition of Done)

Một issue/sub-issue chỉ chuyển `Done` khi đủ cả bốn:

1. **Code** — hoàn thành theo tiêu chí chấp nhận.
2. **Test** — có test tương ứng và đạt.
3. **Review** — đã qua review (trạng thái `In Review` → `Done`).
4. **Tài liệu** — đã cập nhật tài liệu liên quan.

Giờ ước lượng của issue bao gồm đủ bốn việc trên.

### 1.3 Dùng epic → issue → sub-issue trên Project

| Cấp | Item Type | Ghi chú |
|-----|-----------|---------|
| Epic | `Epic` | Nhóm theo năng lực nghiệp vụ. Không tự mang giờ — tổng hợp từ con. |
| Issue | `Issue` | Đơn vị giao việc, ≤ 2 ngày công. Là con của một Epic (trường *Parent issue*). |
| Sub-issue | `Sub-issue` | Chỉ tạo khi issue vượt 2 ngày công. Là con của một Issue. |

Quy ước:

- Tạo mỗi item là một GitHub Issue trong repo này, thêm vào Project; liên kết cha–con bằng sub-issue gốc của GitHub (*Parent issue* / *Sub-issues progress*).
- Tiêu đề: Epic bắt đầu bằng `[Epic]`; Issue/Sub-issue bắt đầu bằng động từ hành động.
- Mọi item điền: `Item Type`, `Status` (mặc định `Todo`), `Iteration`, `担当(仮)`, `Constraint` (`なし` nếu không thuộc 完納奨励金).
- `SWP` để trống cho tới khi đã review; chỉ ghi SWP đã review.
- `見積時間 / Estimate (hours)` điền cho từng item theo `estimate.md` (mục "Cách quy ra giờ").
- Lọc 完納奨励金: view Table, lọc `Constraint:完納奨励金`.

## 2. Cây Epic

[PL điền — chờ file bàn giao từ LAB-4.]

## 3. Danh sách Issue / Sub-issue

[PL điền — chờ file bàn giao từ LAB-4.]

## 4. Ràng buộc 完納奨励金 và phụ thuộc

[PL điền — chờ file bàn giao từ LAB-4.]
