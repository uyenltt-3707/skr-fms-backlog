# Estimate — Ước lượng SWP và giờ

## 1. Phạm vi và phương pháp

[PL điền — phạm vi ước lượng, nguồn (task-breakdown.md), phương pháp chấm SWP.]

## 2. Cách quy ra giờ

> **Đề xuất — chờ duyệt.** Quy tắc nhất quán để mọi issue quy giờ cùng một cách.

1. **Ước giờ trực tiếp từ từng issue** (bottom-up), không suy giờ từ SWP.
   SWP là cỡ tương đối đã review; giờ là ước lượng công việc cụ thể. Hai trường độc lập.
2. **Phạm vi giờ** = code + test + review + cập nhật tài liệu (khớp Định nghĩa xong ở `task-breakdown.md` §1.2). Không cộng đệm (buffer) vào từng issue.
3. **Làm tròn** bội số 0.5h; tối thiểu 1h; **tối đa 15h/issue** (= 2 ngày công). Vượt 15h → tách sub-issue.
4. **Chỉ item lá mang giờ** (issue không có sub-issue, hoặc sub-issue). Issue cha có sub-issue và Epic **không** điền giờ trên Project (tránh cộng đôi khi cộng cột); giờ cha/Epic = tổng con, tính ở mục 4 của file này.
5. **Đối chiếu năng suất tiền đề LAB-1**: 1 MD = 7.5h.
   - Quy đổi: `MD = tổng giờ / 7.5`.
   - Đối chiếu tổng MD của backlog với tổng MD đã ước ở LAB-1; chênh lệch lớn hơn ±15% thì phải giải thích (phạm vi khác, giả định khác...) tại mục 5.
6. **Kiểm tra chéo SWP ↔ giờ** (không dùng để tính): tính giờ/SWP theo từng Epic; issue lệch quá ±50% so với trung bình Epic được rà lại.
7. **Buffer và rủi ro** để ở cấp dự án (mục 5), không phân bổ vào issue.
8. **Hạng mục 完納奨励金**: issue riêng, `Constraint = 完納奨励金`, ước giờ theo cùng quy tắc; tổng riêng nêu ở mục 4.

Điểm cần bạn duyệt: (a) trần 15h/issue, (b) ngưỡng ±15% so với LAB-1, (c) quy tắc "chỉ item lá mang giờ" (phương án khác: cha cũng điền giờ = tổng con).

## 3. SWP đã review theo issue

[PL điền — bảng: Issue · Epic · SWP đã review · Giờ · Ghi chú. Chỉ ghi SWP đã review.]

## 4. Tổng hợp

[PL điền — tổng theo Epic (SWP, giờ, MD); tổng riêng 完納奨励金; tổng toàn backlog.]

## 5. Giả định, rủi ro, buffer

[PL điền — đối chiếu LAB-1, giả định, rủi ro, buffer cấp dự án.]
