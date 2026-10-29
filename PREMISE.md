# PREMISE — Backlog khác bản LAB-4 ở đâu

Bản LAB-4 làm nguồn: `product-a-fishmarket` commit `576480b` (2026-10-29). Chỉ ghi mã spec và nội dung tự viết.
Số `#n` là issue trên repo này. "Dòng" được trỏ từ `task-breakdown.md` §4 và `estimate.md` §5 theo mã P1-x / P2-x / P3-x.

## 1. Spec thêm / bỏ / sửa

| # | Spec (mã / file) | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| P1-1 | SCR-20 紛争管理 (screen spec + API-ID mới) | Thêm | Chỉ có bảng DBT-26 trong Database Design; màn chưa có screen spec, API chưa có ID → thêm bước "thiết kế màn + cấp API-ID", API và UI chờ bước này | Chỗ hở phát hiện khi break WU-093: không cài đặt được màn không có spec. Màn được đưa vào backlog theo quyết định PL L4-5 (`_meta/decisions.md` D27) vì thuộc baseline LAB-1, nhưng LAB-4 chưa thiết kế | #130 (#131 → #134, #135) |
| P1-2 | SCR-28 帳票出力・CSV (screen spec + API-ID mới) | Thêm | Như trên: chỉ có DBT-30 → thêm bước thiết kế màn + cấp API-ID trước API / UI | Chỗ hở khi break WU-095 (cùng nguồn D27); FR-RPT-01 là P0 nên không để ngoài backlog | #141 (#142 → #143, #144) |
| P1-3 | DD-05, SCR-21, API-050, API-069, DBT-20 (đối tượng của 調整要求) | Sửa | 調整要求 chỉ nhận giao dịch 相対 / せり → thêm đối tượng 支払実績 (DBT-13) để sửa 支払完了日 của kỳ 完納奨励金 đã 確定, sinh delta kỳ sau | PL đã quyết ở cuối LAB-4 (D33 — Q2) nhưng thiết kế chưa sửa; WU-050 chỉ ghi "thiết kế bổ sung trước khi làm". Khi break thấy 4 tài liệu phải sửa cùng lúc nên tách thành issue riêng có bước thiết kế đầu | #165 (5 sub-issue, đầu tiên là #166); #167 chờ #166 |
| P1-4 | SCR-26 + API-068 (nút 確定 kỳ 完納奨励金) | Sửa (phạm vi WU-091) | WU-091 chỉ có phần API; WU-067 (SCR-26) không có nút 確定 → thêm sub-issue UI cho nút | D30 đặt thao tác 確定 ở SCR-26 và ghi "nút thuộc phần UI LAB-5", nhưng không WU nào nhận phần UI — phát hiện khi chia owner của WU-091 | #211 → #213 |
| P1-5 | ADR-013 + Database Design (bảng thiết bị dùng chung, PIN băm) | Thêm | Database Design chưa có bảng thiết bị / PIN → thêm sub-issue thiết kế bổ sung trước phần cài đặt của WU-007 | ADR-013 未決 #4 và lý do Complexity của WU-007 trong handoff; break ra thấy 3 sub-issue cài đặt (API, UI, actor) đều phụ thuộc bảng này | #16 (#18 chờ #17) |

## 2. Giả định bổ sung

Chỉ lấp chỗ spec / RFP để ngỏ; không ghi đè điều RFP đã nêu rõ.

| # | Giả định | Chỗ spec / RFP để ngỏ | Ảnh hưởng tới issue / estimate |
|---|---|---|---|
| P2-1 | Quy tắc 支払期日 lưu dạng dữ liệu trong version, hỗ trợ cả "N ngày sau cuối kỳ" và "ngày cố định của tháng sau"; seed dùng giá trị mô phỏng | ADR-006 未決 #7, LAB-1 QA No.3 ② (dạng 支払期日 chưa có trả lời) | #193 10h đã gồm cả hai dạng; khách trả lời thì chỉ đổi seed, không đổi code |
| P2-2 | CSV 支払実績 tạm dùng bộ cột tối thiểu: mã người tham gia, kỳ, số tiền, 支払完了日 | Handoff WU-067: định dạng cột CSV còn 未決 (QA No.3) | #206 10h; đổi bộ cột ước thêm ~2h (rủi ro cấp dự án, không cộng vào issue) |
| P2-3 | 「次期」 khi ghi delta = kỳ chưa 確定 sớm nhất tại thời điểm 調整要求 được 承認 | Handoff WU-062: 「次期」 còn 未決 | #196; xác nhận ở #158, khác giả định thì sửa #196 |
| P2-4 | Báo cáo tháng RPT-10〜12 tạo khi người dùng mở ở SCR-28, không có batch tháng | Catalog báo cáo có 12 mục nhưng WU-094 chỉ sinh RPT-01〜09 (ngày); cách tạo báo cáo tháng không nêu | #143 14h đã gồm 3 báo cáo tháng; nếu cần batch tháng thì thêm issue |
| P2-5 | Nút 確定 trên SCR-26 ở mức tối thiểu: một nút, hộp xác nhận, hiện kết quả khi API trả 409 vì tính lại | D30 không nêu UI chi tiết của SCR-26 (màn ngoài cốt lõi, 非コア) | #213 6h |
| P2-6 | Thiết bị dùng chung làm theo giả định tạm của ADR-013 (danh sách thiết bị do ứng dụng quản lý, PIN băm, giới hạn số lần thử) cho tới khi có trả lời | ADR-013 未決 #4 (đăng ký thiết bị, độ dài PIN, cấp / thu hồi) | #16 46h; trả lời khác thì sửa #18 và ước lại |
| P2-7 | Đội giả định 6 người (FE-A, FE-B, BE-A, BE-B, QA-A, PM); sprint 10 ngày × 7.5h; giờ làm backlog 52.5h / người / sprint (trừ 7.5h họp, 15h buffer), PM 30h (còn lại là quản lý) | RFP / LAB-1 không định nghĩa đội cho LAB-5 (LAB-1 chỉ gợi ý cơ cấu đội) | Trần tải mỗi Iteration; Sprint 1 xếp 240h / 292.5h |

## 3. Hướng đã chốt

| # | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| P3-1 | Ai kích hoạt tính và 確定 完納奨励金 | (a) batch tháng tự 確定 · (b) Cron tạo 暫定, ROLE-SETTLEMENT bấm 確定 | (b) | D23 (L4-1): số tiền cần người kiểm (HITL). Backlog tách #197 (batch chỉ 暫定) và #211 (確定) |
| P3-2 | 確定 khi số 暫定 đã lệch dữ liệu mới | (a) chặn 確定 + thêm API "tính lại 暫定" · (b) tính lại trong cùng giao dịch, lệch thì cập nhật 暫定 + 409, không 確定 | (b) | D32: ít endpoint hơn, không có cửa sổ lệch giữa tính và 確定 → #212 |
| P3-3 | Sửa 支払完了日 sau khi kỳ đã 確定 | (a) qua 変更管理 · (b) qua 調整要求 → delta kỳ sau | (b) | D33: giữ nguyên tắc BR-INC-01 không sửa lặng lẽ kỳ đã 確定 → P1-3, #165 |
| P3-4 | DR khi mất cả region Tokyo | B dump 1 giờ · B′ dump 15 phút · C replication logic | B′ baseline có điều kiện; không đạt thì lùi B; C để tương lai | D20: chỉ chốt được khi có số đo → #228 dựng, #233 đo và ghi quyết định |
| P3-5 | 「追加情報の要求」 ở duyệt 調整要求 | (a) trạng thái riêng · (b) gộp vào 却下 | (b) cho baseline; câu hỏi khách non-blocking | D21 (d), D26 → #171 không có trạng thái riêng |
| P3-6 | ROLE-SETTLEMENT chọn giao dịch để 起票 調整要求 | (a) mở API đọc thô 026 / 033 · (b) endpoint đọc riêng API-069 | (b) | D24, D29: quyền tối thiểu → #168 |
