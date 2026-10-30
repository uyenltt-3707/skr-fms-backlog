# Review độc lập — progress-report.md (Sprint 1 giả lập)

Ngày review: 2026-10-30. Người review không phải tác giả. Đọc Project #2 trực tiếp bằng GraphQL (389 item, 4 trang), tự tính lại; không dùng script của repo.
Số dòng = `progress-report.md`.

## A. Đối chiếu số liệu (tự đọc API) — KHỚP

| Hạng mục | Kết quả |
|---|---|
| Item lá Sprint 1 | 29 (34 item có Iteration = Sprint 1, trừ 5 cha #103 #152 #218 #223 #232) — khớp |
| Status | Done 20 / 182 SWP / 155.5h · In Review 3 / 28 / 40h · In Progress 5 / 46 / 39.5h · Todo 1 / 25 / 8h · tổng 29 / 281 / 243h — khớp từng ô (dòng 19–24) |
| Issue open/closed | 20 Done = 20 CLOSED; 9 chưa Done = 9 OPEN; `sprint1.yaml` ↔ Project không lệch |
| Per 担当 | BE-A 52/46, BE-B 52.5/27.5, FE-A 43.5/28.5, FE-B 48/35.5, PM 29/18, QA-A 18/0 — khớp (dòng 32–37) |
| Burndown | 281 → 281, 260, 243, 219, 194, 173, 143, 125, 105, 99 — khớp CSV, PNG và bảng; tự tính lại từ ngày Done trong yaml + SWP Project |
| Cha / epic | 5 cha trong Sprint 1 không bị cộng; Status cha = In Progress, không bất thường |
| Tính mô phỏng | Nói rõ ở tiêu đề, dòng 3–5, biểu đồ, JA dòng 91; "thực hiện 2026-10-30" có — ĐẠT (mục 6) |
| 5 rủi ro bắt buộc | Đều có mặt (dòng 82–86): BE quá tải + thêm BE từ Sprint 4, −25.4%, 要確認, ADR-010, 概算 — ĐẠT về hiện diện; vấn đề nằm ở độ sâu (mục B) |

## B. Phát hiện

| # | Mức | Vị trí | Phát hiện | Bằng chứng | Đề xuất sửa |
|---|---|---|---|---|---|
| 1 | High | §4 dòng 82 (hành động "lên đầu Sprint 2") + thiếu hẳn ở §2/§4 | Không nói Sprint 2 sẽ **vượt trần** khi cộng carry-over. Hành động "đưa #179 #180 #146 lên đầu" không nêu việc nào bị đẩy ra | Sprint 2 kế hoạch 232h (BE-A 50, BE-B 51, FE-A 45, FE-B 52, QA-A 18, PM 16). Carry-over 87.5h (BE-A 6, BE-B 25, FE-A 15, FE-B 12.5, QA-A 18, PM 11). Tổng 319.5h > trần 292.5h. BE-B 76h (145% trần 52.5); FE-B 64.5; FE-A 60; BE-A 56. Dù bỏ phần chỉ còn chờ review (#179, #220, #166): BE-B 61, FE-B 64.5, BE-A 56 vẫn > 52.5 | Thêm 1 đoạn "Tải Sprint 2 sau carry-over" (bảng 担当 × giờ); nêu rõ item nào lùi Sprint 3 hoặc ai gánh; FE-B cũng thành điểm nghẽn, không chỉ BE |
| 2 | High | JA dòng 96 | Viết "合意済みの前提で進めます" (tiến hành theo tiền đề **đã được thống nhất**). Khách chưa thống nhất gì: P2-3 là giả định nội bộ của team (PREMISE §2). Gửi khách sẽ thành cam kết sai sự thật / dễ bị phản bác | `PREMISE.md` P2-3 "Giả định bổ sung"; report dòng 84 tự ghi "chốt theo giả định PREMISE P2-3" | Đổi: 「ご回答がない場合は、当方の暫定前提（次期＝未確定の最も早い期）で進め、内容を改めてご報告します」 |
| 3 | High | §4 dòng 85 (ADR-010), dòng 82 | Chuỗi ADR-010 chỉ gắn #243/#244 → #234/#235. Bỏ sót nhánh FE-B: #234 phụ thuộc I-075 (dump + sao chép Osaka) mà I-075.2/.3 (22h) ở **Sprint 2 của FE-B**, FE-B đã 52/52.5h và còn mang carry-over #225. Không nói quyết định B′/B (12-11) có thể trượt, cũng không nói hệ quả với cam kết NFR-AVL-03 nếu trượt | `tools/backlog.yaml` I-076 `deps: [I-075, I-081]`; I-075.2 FE-B 12h S2, I-075.3 FE-B 10h S2, I-075.1 FE-A 14h S3; ước tính tải ở mục 1 | Thêm I-075 (#FE-B) vào cột Issue/Ảnh hưởng; nêu "nếu #243/#244 hoặc I-075 không xong hết Sprint 2 thì #234 trượt sang Sprint 4, B′/B không chốt được 12-11" |
| 4 | Medium | §4 dòng 82 | Nguyên nhân quá tải BE chỉ quy cho "review chậm / BE-A review DB duy nhất". Bỏ sót nguyên nhân gốc ở khâu xếp kế hoạch: BE-A 52h, BE-B 52.5h = 99–100% trần (trần đã trừ 15h buffer), không có dự phòng | `estimate.md` §4 bảng tải: BE-A 52, BE-B 52.5 (trần 52.5). Sprint 2: 50 / 51, Sprint 3: 50 / 52.5 → lặp lại | Ghi "Sprint 1–3 xếp BE ở ~100% trần" thành nguyên nhân; hành động: giảm tải BE Sprint 2–3, không chỉ "đổi người review" |
| 5 | Medium | dòng 82 "người review DB duy nhất" | "duy nhất" không có nguồn: yaml chỉ ghi BE-A review DB của BE-B (#146, #179) | `sprint1.yaml` note #146: "người review DB của BE-B"; note #179: "người review được là BE-A" | Bỏ "duy nhất" hoặc ghi "chủ yếu" + nguồn |
| 6 | Medium | §4 dòng 82 (cột Issue/Ảnh hưởng) | Tác động phụ thuộc của carry-over thiếu: #179/#180 → ngoài #182 #183 (S2) còn #188 #189 (S3, gián tiếp), #185 #186 #153 #157 (backlog). #146 chặn 12 item trực tiếp / 67 item gián tiếp (chuỗi 調整要求 #148 #149 #161–#163 #175 #176, upload 証憑 #177 #178, **#226 RLS/REVOKE cho mọi bảng mới ADR-004**) mà không dòng nào nhắc. #243/#244 → #234 #235 (S3) có | Dò phụ thuộc bắc cầu từ `backlog.yaml` (phụ thuộc cha kế thừa xuống lá) | Thêm cột "Item bị chặn (Sprint 2/3 / backlog)"; nêu riêng #226 (bảo mật) |
| 7 | Medium | dòng 75 | "không do một item lớn bất thường" mềm hơn dữ liệu. 99 SWP còn lại: #244 25 (25%), #166 16, #243 15 → ba item = 56 SWP (57%); hai trong ba là chuỗi QA load test | Project: #244 25 SWP Todo, #166 16 SWP In Review, #243 15 SWP In Progress; 25+16+15=56/99 | Viết "57% SWP còn lại nằm ở 3 item (#244, #166, #243), trong đó chuỗi load test 40 SWP" thay vì kết luận "không do item lớn" |
| 8 | Medium | dòng 83 (−25.4%) | "Sprint 1 giả lập không đo giờ thực tế → chưa kết luận" đúng, nhưng bỏ qua tín hiệu có sẵn: #14 (8h) và #243 có "việc thêm ngoài giờ ước" (yaml), mà ước lượng trên Project không đổi (#14 8h, #243 10h), không có issue/giờ bổ sung; #241 (14h, FE-B, chưa xếp Iteration) mô tả ghi "kết quả bất định" mà report chỉ nhắc "mô tả đã ghi giới hạn" (dòng 85). Chuỗi này giờ/SWP thấp: #244 0.32, #234 0.40, #241 0.56, #243 0.67 so trung bình 1.23 | `sprint1.yaml` note #14, #243; Project: #14 8h, #243 10h, #244 8h/25 SWP, #234 10h/25, #241 14h/25; `backlog.yaml` I-079.2 desc | Thêm: "2 item Sprint 1 phát sinh việc ngoài ước, chưa ghi giờ; chuỗi DR/load test có giờ/SWP thấp nhất → ứng viên ước thiếu"; nêu #241 là rủi ro kết quả bất định |
| 9 | Medium | JA dòng 93 | Nói "認証・権限の基盤 … 共通エラー処理 … 本番環境の構築 … 大半が完了" gần như hoàn tất nền tảng, quá lạc quan: OTP/MFA (#I-002.1, 15h) thuộc Sprint 2; #220 (130 MSG JA) còn In Review nên 共通エラー処理 mới xong phía API (#219). 31% item, 35% SWP chưa xong; JA không nhắc có ảnh hưởng tiến độ ngoài "tối thiểu hóa" | `backlog.yaml` I-002.1 sprint 2; Project #219 Done, #220 In Review | Viết cụ thể: 「認証の一部（ロック機構、権限絞り込み）、…」「エラーメッセージの画面反映はレビュー中」; thêm "計画比 約6割強の完了" nếu cần (không dùng SWP) |
| 10 | Medium | đầu file (thiếu) | Không có kết luận tổng quan ở đầu (sprint đạt/không đạt, mức trễ). Không tính velocity hay hệ quả với mốc hoàn tất: dòng 82 chỉ ghi "mốc hoàn tất backlog (BE-A 543h + BE-B 553h)" không số tác động. Backlog còn 2,367h chưa xếp sau Sprint 3 (`estimate.md` §4) | 182 SWP/sprint; 99 SWP + 87.5h carry-over; không dòng nào quy ra sprint trễ | Thêm đoạn 3 dòng đầu §2: "64.8% SWP / 69% item; carry-over 87.5h ≈ 0.3 sprint; nếu giữ velocity này, backlog thêm X sprint" (ghi rõ là ước giả lập) |
| 11 | Low | dòng 87 | "phần cài đặt D33 (#165, #167)" sai đối tượng: #165 là issue cha chứa #166; phần bị chặn là #214 #215 #216, #168 #169 #170 và test #383 | Project: #165 parent In Progress; `backlog.yaml` deps của X-D33.1 | Sửa danh sách |
| 12 | Low | dòng 87 "#131, #142 đã duyệt" | "duyệt" không có nguồn (yaml chỉ ghi Done sau In Review; không ghi PL duyệt) | `sprint1.yaml` #131, #142 | Ghi "Done (qua review)" |
| 13 | Low | dòng 83 "lệch > 25% thì ước lại" | Ngưỡng 25% không có nguồn (`estimate.md` dùng ±15% cho epic, ±50% cho giờ/SWP) | `estimate.md` §5 kết luận, §4 | Nêu căn cứ hoặc dùng ngưỡng đã có |
| 14 | Low | dòng 42 (#243, #244 "chờ môi trường") | #244 không chờ môi trường mà chờ dữ liệu + kịch bản #243 | `sprint1.yaml` note #244 | Sửa lý do |
| 15 | Low | dòng 70–72 vs bảng | "Ngày 6–10 khoảng cách mở rộng" không đúng cho ngày 11-10: lệch +60.6 → +58.7 (thu hẹp 1.9). Tự kiểm của repo chỉ kiểm ngày 2–5 | CSV dòng 11-09, 11-10 | Viết "mở rộng gần như liên tục, trừ 11-10" |
| 16 | Low | dòng 75 | "khoảng một phần ba SWP" thực tế 35.2% (99/281); mềm nhẹ | tính 99/281 | Ghi "35%" |
| 17 | Low | dòng 82–86 | Điểm quyết định "thêm BE" (11-27) không nói thời gian đưa người mới vào trước Sprint 4 (12-14), cũng không nói vì sao chỉ tính BE | Sprint 3 kết thúc ~12-11 (`sprint1.yaml` 14 ngày/sprint) | Thêm 1 dòng lead-time |
| 18 | Low | `progress-data/self-check-progress-report.txt` | Tự kiểm "truy vết số" chỉ khớp yếu với số ≤10 (vô nghĩa), nên chưa chứng minh được mọi số/câu có nguồn; chỉ kiểm khoảng 12 điều kiện | file self-check, các dòng "khớp yếu" | Không dùng nó làm bằng chứng đạt; giữ review này làm cổng |

## C. Câu không có nguồn (tổng hợp mục 3)

Không tìm số liệu nào không truy vết được về Project / `sprint1.yaml` / docs; vấn đề nằm ở **suy diễn**: "duy nhất" (#5), "đã duyệt" (#12), ngưỡng 25% (#13), hạn 2026-11-16/11-20, "hạn review 1 ngày" (là đề xuất hành động, chấp nhận được nhưng nên ghi "đề xuất"). Fact "không có region Osaka" có nguồn trong `backlog.yaml` I-079.2 và `sprint1.yaml` #14, nhưng là giả định kịch bản (PL bổ sung 2026-10-30), chưa kiểm với Supabase thật — report có ghi "giả lập".

## D. Phụ lục JA (mục 5)

| Tiêu chí | Kết quả |
|---|---|
| Không có số nội bộ (SWP, giờ, tải người, −25.4%, tên người) | ĐẠT — không có |
| Ghi rõ mô phỏng | ĐẠT — dòng 91 (模擬スプリント, 2026-10-30, 実際の進捗ではありません) |
| 5–8 dòng | ĐẠT — 1 dòng chú thích + 5 gạch đầu dòng = 6 dòng |
| Tiếng Nhật tự nhiên | Cơ bản tự nhiên, đúng kính ngữ; có 2 lỗi nội dung (#2 "合意済み", #9 quá lạc quan) |
| An toàn gửi khách | CHƯA — sửa #2 trước khi gửi. Ghi chú: dòng 95 nêu giới hạn Supabase (không có Osaka) ảnh hưởng quyết định DR, nên PL xác nhận muốn báo khách ở mức này trước khi gửi |

## E. Điểm tốt

- Mọi số bảng khớp API 100%; không double-count cha/epic; Status/closed nhất quán.
- Báo cáo thẳng về BE-B 52%, QA-A 0%, burndown lệch +99; ghi rõ ADR-010 "chưa đo"; không nói quá về −25.4%.
- Nêu đủ 5 rủi ro bắt buộc, có người làm + ngày.
- Biểu đồ khớp CSV; ghi giả lập ngay trên tiêu đề biểu đồ.

## Kết luận: CHƯA ĐẠT

Số liệu đạt. Chưa đạt vì 3 mục High: (1) bỏ sót Sprint 2 quá tải sau carry-over (319.5h > trần 292.5h; BE-B 145%), (2) JA khẳng định "合意済み" sai sự thật với khách, (3) chuỗi ADR-010 thiếu nhánh FE-B/I-075 và hệ quả với quyết định B′/B. Sửa #1–#3 và #9–#10 rồi review lại; các mục Low có thể sửa cùng lúc.

---

## Vòng 2 (sau sửa)

Ngày: 2026-10-30. Tự kiểm lại bằng Project #2 (dữ liệu API đã đọc ở vòng 1) + `tools/backlog.yaml` + `sprint1.yaml`; không chạy script của repo (tránh ghi đè file). Số dòng = `progress-report.md` bản mới.

### Kiểm lại số liệu
- Bảng status / owner / burndown không đổi, vẫn khớp API.
- Bảng mới "Tải Sprint 2" (dòng 54–62): FE-A 45+15=60, FE-B 52+12.5=64.5, BE-A 50+6=56, BE-B 51+25=76, QA-A 36, PM 27, tổng 232+87.5=319.5 — khớp số tự tính (vòng 1). Vượt 7.5 / 12 / 3.5 / 23.5, tổng vượt 27 (=7.5+12+3.5+23.5=46.5 là tổng vượt theo người; 27 là 319.5−292.5 theo tổng — cả hai đúng, nhưng ô "Vượt 27" ở hàng Tổng khác bản chất với tổng cột; xem N3).
- Các item đề xuất rút: FE-A #12 (10h) · FE-B #264 (3.5h) + #31 (12.5h) · BE-A #222 (10h) · BE-B #67 (6h) — đều ở Sprint 2, đúng chủ, và **không có item phụ thuộc trong Sprint 2** (dò `backlog.yaml`). BE-B #7, #8, #29, #60 đúng là đều có item phụ thuộc trong Sprint 2 (#7/#8 → #253, #254; #29 → #31, #32, #264; #60 → #67). #230, #231 đúng là I-075.2/.3, FE-B, 12h + 10h, Sprint 2.
- Chặn bởi carry-over (dòng 46–48): #146 → 12 trực tiếp, gồm #226 ✓; #179/#180 → #182, #183 (S2), #188, #189 (S3) ✓; #243/#244 → #234, #235 ✓; #166 → #214〜#216, #168〜#170 ✓; #158 → #195, #196 ✓; #220 → #261 ✓.

### Từng phát hiện

| # | Mức cũ | Kết quả | Ghi chú / bằng chứng |
|---|---|---|---|
| 1 | High | **Đã sửa (còn dư, xem N1)** | Có bảng tải Sprint 2 sinh từ Project, hàng rủi ro dòng 103 nêu item rút cụ thể; sau khi rút FE-A 50, FE-B 48.5, BE-A 46 ≤ 52.5; BE-B chỉ rút được 6h nên còn 70 > 52.5 và report nói thẳng "phải lùi một chuỗi" — đúng |
| 2 | High | **Đã sửa** | Dòng 119 viết lại: 弊社の想定案で作業を進め、その内容を改めてご確認いただきます — không còn khẳng định "đã thống nhất", tiếng Nhật tự nhiên. Có thêm ghi chú PL xác nhận việc công bố giới hạn region (xem N2 về vị trí ghi chú) |
| 3 | High | **Đã sửa** | Dòng 107: thêm I-075 (#230, #231 FE-B Sprint 2, FE-B đã vượt trần), B′/B có thể lùi Sprint 4, NFR-AVL-03 chưa chốt, hành động "giữ #230 #231 #243 #244" nhất quán với dòng 103 |
| 4 | Medium | Đã sửa | BE-A / BE-B 99–100% trần: dòng 43, 93, 104; note yaml #146 |
| 5 | Medium | Đã sửa | "duy nhất" đã bỏ (grep: không còn); yaml #146 nay ghi "kịch bản: review DB do BE-A làm" — nguồn rõ |
| 6 | Medium | Đã sửa | Dòng 46–48 đủ và khớp phụ thuộc (đã kiểm) |
| 7 | Medium | Đã sửa | Dòng 95: 56/99 SWP (57%) khớp |
| 8 | Medium | Đã sửa | Dòng 105: nêu #14/#243 phát sinh, giờ/SWP thấp (#244 8h/25 SWP), #241 bất định, ước lại ở Sprint 2 planning |
| 9 | Medium | Đã sửa | JA dòng 116–117: "約7割（件数ベース）" = 20/29 (69%) đúng; OTP ở Sprint 2; "共通エラー処理の一部" chính xác |
| 10 | Medium | **Sửa chưa đủ** | Đã có kết luận đầu mục (dòng 15) "KHÔNG đạt kế hoạch". Nhưng tác động mốc vẫn không quy ra con số: dòng 103 chỉ ghi "phần vượt dồn sang Sprint 3"; không nói 87.5h ≈ 0.3 sprint, không ước Sprint 3 / backlog trễ bao lâu (xem N1) |
| 11 | Low | Đã sửa | Dòng 109 dùng #214〜#216, #168〜#170, #383 (đúng phụ thuộc) |
| 12 | Low | Đã sửa (có lỗi mới, N4) | yaml #131, #142 có note PL duyệt |
| 13 | Low | Đã sửa | Dòng 105 gắn nhãn "ngưỡng PM đề xuất 25%, chờ PL duyệt" |
| 14 | Low | Đã sửa | Dòng 44: #244 chờ dữ liệu + kịch bản #243 |
| 15 | Low | Đã sửa | Dòng 93 nêu 11-10 thu hẹp; kiểm: 11-10 có 3 item Done (#15 15, #219 6, #131 9 = 30 SWP) đúng |
| 16 | Low | Đã sửa | 35.2% (dòng 96) |
| 17 | Low | Đã sửa | Dòng 104: Sprint 4 bắt đầu 2026-12-14 (Sprint 3 11-30 + 14 ngày), có lead-time 2 tuần |
| 18 | Low | **Sửa một phần** | Self-check: 18 ĐẠT, 0 LỆCH, đã thêm kiểm 56 SWP, 99–100% trần, 12 item chặn, 16 item bị chặn, bảng sprint2. Nhưng **không** kiểm đề xuất rút item (#12, #264, #31, #222, #67 không có phụ thuộc S2; #7/#8/#29/#60 có phụ thuộc) — tôi phải kiểm tay; phần "số khớp yếu ≤10" vẫn vô nghĩa |

### Vấn đề MỚI phát sinh

| # | Mức | Vị trí | Phát hiện | Bằng chứng | Đề xuất |
|---|---|---|---|---|---|
| N1 | Medium | Dòng 103 | Rút phần vượt sang Sprint 3 mà không kiểm trần Sprint 3. Sprint 3 đã xếp: FE-A 48, FE-B 45, BE-A 50, BE-B 52.5 (`estimate.md` §4). Cộng phần rút: FE-A 58, FE-B 61, BE-A 60 (đều > 52.5); BE-B còn thêm chuỗi lùi nữa. Tức quá tải chỉ dời, và chưa nói Sprint 3 / mốc trễ bao nhiêu | 10 / 16 / 10 / 6h rút; Sprint 3 tổng 249.5 / 292.5 nhưng dư không đều | Thêm bảng tải Sprint 3 sau khi nhận phần rút (có thể sinh từ Project); nêu rõ nếu vượt thì lùi Sprint 4 và ảnh hưởng mốc |
| N2 | Low | Dòng 114 | Ghi chú nội bộ tiếng Việt nằm **trong** khối phụ lục gửi khách (blockquote liền dưới câu chú thích JA), dễ bị gửi nhầm; "(dòng 3)" mơ hồ — giới hạn region nằm ở dòng 90–91 và JA dòng 118, không phải dòng 3 | đọc dòng 111–114 | Đưa ghi chú ra ngoài phụ lục (trước tiêu đề) hoặc ghi "XÓA DÒNG NÀY TRƯỚC KHI GỬI"; sửa tham chiếu |
| N3 | Low | Dòng 62 | Ô "Vượt (h)" hàng Tổng = 27 (tổng − trần tổng) trong khi các hàng trên cộng lại 46.5 (người nào vượt thì tính); dễ gây hiểu nhầm là thiếu 19.5h | 7.5+12+3.5+23.5 = 46.5 ≠ 27 | Ghi chú "27 = tổng − trần tổng; 46.5 = tổng phần vượt theo người (QA-A, PM còn dư không bù được)" |
| N4 | Low | `progress-data/sprint1.yaml` dòng 20 (#23) | Note "PL duyệt thiết kế SCR-28 ngày 11-09" gắn nhầm vào #23 (WU-069 bảng audit), không phải thiết kế SCR-28; trùng note đúng của #142. Không ảnh hưởng báo cáo nhưng làm nhiễu nguồn | `gh issue view 23`: "[WU-069] Bảng audit…" | Xóa note ở #23 |

### Kết luận vòng 2: CHƯA ĐẠT (gần đạt)

Cả 3 High đã đóng và đã kiểm tay với Project/backlog. Còn lại: Medium #10 + N1 (tác động mốc chưa định lượng, quá tải dời sang Sprint 3 chưa kiểm trần) — cùng một gốc, cần thêm bảng tải Sprint 3 và 1–2 dòng ước độ trễ; kèm N2 (ghi chú nội bộ trong phụ lục JA) và N4 (note yaml sai). Sửa N1+N2 (và N3, N4 nhanh) thì có thể ĐẠT ở vòng 3 mà không cần review lại toàn bộ.

---

## Vòng 3

Ngày: 2026-10-30. Kiểm lại bằng Project #2 (dữ liệu API), `tools/backlog.yaml`, `sprint1.yaml`; không chạy script repo.

| Mục | Kết quả | Bằng chứng |
|---|---|---|
| N1 bảng tải Sprint 3 | **Đã sửa** | Dòng 67–77: FE-A 48+10=58 (+5.5), FE-B 45+16=61 (+8.5), BE-A 50+10=60 (+7.5), BE-B 52.5+6=58.5 (+6), QA-A 50, PM 4; tổng 249.5+42=291.5, vượt 27.5, ròng −1 — khớp số tự tính. Đề xuất rút lưu thành dữ liệu (`replan_push_to_sprint3: [12,264,31,222,67]`, `replan_keep_in_sprint2: [230,231,243,244]`), khớp dòng 121; hành động "xếp lại Sprint 2–3 cùng lúc, phần không hấp thụ ra sau Sprint 3, báo PL" nói rõ quá tải chỉ dời |
| #10 tác động mốc | **Đã sửa** | Dòng 80–81: 87.5/292.5 = 0.299 ≈ 0.3 sprint, dồn vào BE; lặp lại ở cột "Ảnh hưởng mốc" dòng 121. Xem L1 |
| N2 ghi chú nội bộ | **Đã sửa** | Ghi chú (không gửi khách) nằm trên tiêu đề phụ lục; "gạch đầu dòng thứ 3" đúng là bullet giới hạn region (Osaka). Phụ lục JA 5 gạch + 1 dòng chú thích mô phỏng, không có số nội bộ |
| N3 ô Vượt | **Đã sửa** | Dòng "Tổng" Sprint 2: 46.5 (ròng 27) = 7.5+12+3.5+23.5 và 319.5−292.5; Sprint 3: 27.5 (ròng −1) = 5.5+8.5+7.5+6 và 291.5−292.5; có chú thích |
| N4 note #23 | **Đã sửa** | `sprint1.yaml` #23 không còn note; "SCR-28 ngày" còn đúng 1 lần (#142) |
| #18 self-check | **Đã sửa** | `self-check-progress-report.txt`: 22 ĐẠT, 0 LỆCH; có kiểm item rút (thuộc Sprint 2, không có phụ thuộc S2), BE-B #7/#8/#29/#60 có phụ thuộc, bảng sprint3, 0.30 sprint. Tôi kiểm tay độc lập cùng kết quả vòng 2. Phần "số khớp yếu ≤10" vẫn vô nghĩa nhưng không còn là cổng duy nhất |
| Số liệu cũ | Không đổi | Status / owner / burndown / Sprint 2 vẫn khớp API |

### Lưu ý còn lại (Low, không chặn)
- **L1:** "mốc hoàn tất lùi ít nhất ~0.3 sprint" đúng nếu hiểu là phần thiếu hụt 87.5h so với kế hoạch trong điều kiện các sprint sau chạy 100% trần; nhưng câu đệm "Sprint 2–3 gần trần → không hấp thụ được" không khớp số: gộp Sprint 2+3 chỉ vượt ròng khoảng 26h (phân theo người ~32h, BE-B 23.5h là lớn nhất). Nên ghi rõ cách suy ra (thiếu hụt so kế hoạch ở trần 100%, và "chủ yếu BE-B") hoặc dùng "tối đa ~0.3 sprint"; không ảnh hưởng quyết định thêm BE.
- **L2:** Tổng hợp tải Sprint 2 và 3 chưa chỉ ra người cụ thể chịu phần dư cuối (BE-B ~23.5h qua cả hai sprint) — đã được ngầm nêu ở "BE-B vẫn vượt… phải lùi một chuỗi, PM chọn và báo PL".

### Kết luận vòng 3: ĐẠT

Số liệu khớp API; 3 High + các Medium/Low và N1–N4 đã đóng và kiểm độc lập; báo cáo ghi rõ giả lập (thực hiện 2026-10-30), phụ lục JA an toàn gửi khách (không số nội bộ, đã đánh dấu mô phỏng, không còn khẳng định "đã thống nhất", ghi chú nội bộ tách khỏi phụ lục). Chỉ còn 2 ghi chú Low (L1, L2), sửa được cùng lần chỉnh tiếp theo.

## PL duyệt

**PL duyệt 2026-10-30 — 受入** (sau khi đọc `progress-report.md` và vòng 3 của review này).

Nhận xét của PL khi duyệt (nguyên văn):

- Báo cáo tiến độ do AI tổng hợp có số liệu khớp hoàn toàn với Project nhưng vẫn có câu làm nhẹ rủi ro và một câu tiếng Nhật
  hứa sai với khách. Số đúng chưa đủ để gửi khách; người phải đọc lại giọng văn và cam kết trước khi gửi.

Sửa kèm khi duyệt: câu backup ở phụ lục JA viết trung tính (B′ 15 phút chờ kết quả load test, không đạt thì báo khách kèm phương án đề
xuất); ngưỡng ước lại 25% theo epic được PL đồng ý (`estimate.md` §3 quy tắc 9, `progress-report.md` §4).
