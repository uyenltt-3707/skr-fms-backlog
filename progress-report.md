# Progress Report — Sprint giả lập

> Sprint và người phụ trách là **giả lập**. Sprint chưa chạy: file đang ở trạng thái kế hoạch (sau B2); số liệu thực tế điền ở bước báo cáo tiến độ.

## 1. Iteration

- Iteration trên Project: **Sprint 1 (giả lập)** — 2026-11-02 〜 2026-11-15 (giả lập, 10 ngày làm việc).
- Kế hoạch Sprint 1: 29 item lá, 243h (trần 292.5h). Sprint 2 (2026-11-16〜11-29) 232h · Sprint 3 (2026-11-30〜12-13) 249.5h (sau B2b).

## 2. Trạng thái

Ảnh chụp 2026-10-29, sau B2b.

| Trạng thái | Số issue | Tổng SWP | Ghi chú |
|---|---|---|---|
| Todo | 366 (270 item lá) | — | SWP chấm ở B3 |
| In Progress | 0 | — | |
| In Review | 0 | — | |
| Done | 0 | — | |

## 3. Burndown

Chưa có — Sprint 1 chưa chạy. Đường kế hoạch: 243h giảm đều trong 10 ngày (24.3h / ngày).

## 4. Rủi ro trễ

Nhận diện khi lập kế hoạch; cập nhật khi chạy Sprint.

| Rủi ro | Issue | Ảnh hưởng tới mốc nào | Hành động | Ai làm, khi nào |
|---|---|---|---|---|
| BE là nút cổ chai: bản B2 BE 977h / FE 538h, Sprint 3 FE-A chỉ có 4h việc vì màn chờ API | toàn backlog; đã chuyển #82, #120, #168, #181, #219, #134, #143, #317〜#319 sang FE | Mốc hoàn tất backlog | **Đã làm (B2b):** FE nhận API đơn giản (CRUD, đọc danh sách, không RPC / tiền / bảo mật — Next.js fullstack) + phần API của màn ước thô; RPC, logic nguyên tử, 完納奨励金, bảo mật giữ ở BE. Sau cân: Sprint 3 FE-A 48h / FE-B 45h / BE-A 50h / BE-B 52.5h, không ai vượt 52.5h. Còn lại: BE 1,096h vẫn ≈ 10 sprint cho 2 người → theo dõi từ Sprint 2, cân nhắc thêm 1 BE | PM — đã làm 2026-10-29; xem lại ở Sprint 2 planning (2026-11-13) |
| 4 câu hỏi 要確認 chưa có trả lời | #17, #116, #125, #158 | Chặn thiết kế #18, phạm vi #126, màn SCR-16, chốt #196 | Gửi câu hỏi tuần 1 Sprint 1; quá hạn thì chốt theo giả định PREMISE.md §2 | PM — 2026-11-06 |
| Thiết kế bổ sung chưa được PL duyệt | #166, #131, #142 | Phần cài đặt D33, SCR-20, SCR-28 không vào được Sprint 2–3 | Review thiết kế ở giữa Sprint 1 | PM — 2026-11-09 |
| B′ không đạt khi đo dump + sao chép | #228, #233 | Cam kết NFR-AVL-03 với khách | Đo ở Sprint 2; không đạt thì lùi B và gửi câu hỏi khách đã duyệt | QA-A đo, PM quyết — Sprint 2 |
| E07 có thể ước thiếu (báo cáo dùng chung) | #136, #141 | Mốc báo cáo ngày FR-RPT-01 (P0) | Kiểm chéo bằng SWP ở B3; nếu lệch thì ước lại | PM — B3 |
