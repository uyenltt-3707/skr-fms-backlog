# Task Breakdown — Product A (LAB-5)

Nguồn: `specs/_meta/lab5_handoff.yaml` của LAB-4 @ `576480b` — 95 WU, 13 epic. Dữ liệu backlog tự viết ở
`tools/backlog.yaml`; số `#n` là issue của repo này (mapping đầy đủ: `tools/issue-map.json`).

## 1. Nguyên tắc chia task

### 1.1 Độ hạt — chia tới đâu thì dừng

- **1 WU = 1 issue** (giữ truy vết 1–1 với handoff, tiêu đề mở đầu `[WU-NNN]`). Issue thêm khi break có tiền tố `[D33]` hoặc `[要確認]`.
- **Tách sub-issue** khi có một trong ba điều kiện:
  1. ước giờ > **15h** (2 ngày công × 7.5h) — mỗi sub-issue cũng ≤ 15h;
  2. issue cần **hai loại người làm** (vd. API cho BE + màn cho FE, hoặc phần test tích hợp cho QA) — mỗi sub-issue một 担当(仮);
  3. issue cần **bước thiết kế trước** (SCR-20, SCR-28, D33, thiết bị dùng chung) — sub-issue thiết kế đứng đầu, sub-issue cài đặt phụ thuộc nó.
- **Dừng chia** khi item lá: một người làm, một kết quả kiểm chứng được, ≤ 15h. Không chia theo từng file hay từng tầng code nhỏ hơn thế.
- Kết quả: 13 epic · 100 issue · 150 sub-issue · 184 item lá (lá = issue không có sub-issue, hoặc sub-issue).

### 1.2 Định nghĩa xong (Definition of Done)

Item lá chỉ chuyển `Done` khi đủ cả bốn: (1) **code** đạt tiêu chí xong ghi trong issue; (2) **test** tương ứng có và đạt;
(3) **review** xong (`In Review` → `Done`); (4) **tài liệu** liên quan đã cập nhật. Giờ ước lượng đã gồm đủ bốn việc.
Issue cha / epic `Done` khi mọi con `Done`.

### 1.3 Dùng epic → issue → sub-issue trên Project

| Cấp | Item Type | Cách liên kết | 見積時間 | 担当(仮) | Iteration |
|---|---|---|---|---|---|
| Epic | `Epic` | — | tổng item lá (script cộng) | PM | để trống (trải nhiều sprint) |
| Issue | `Issue` | sub-issue thật của epic | lá: ước trực tiếp · cha: tổng con | lá: theo loại · cha: người nhiều giờ nhất | lá: theo kế hoạch · cha: sprint chung của con, khác nhau thì trống |
| Sub-issue | `Sub-issue` | sub-issue thật của issue | ước trực tiếp (≤ 15h) | theo loại | theo kế hoạch |

- Mọi item: `Status = Todo` khi tạo (script không ghi đè tiến độ khi chạy lại), `Constraint = 完納奨励金` cho E10 và issue D33, còn lại `なし`.
- `SWP` để trống ở B2 (chấm ở B3).
- Nhãn `要確認`: issue cần hỏi lại PL / khách; lọc trên Project bằng `label:要確認`.
- 担当(仮) theo loại: DB / API / batch → BE-A, BE-B · UI → FE-A, FE-B · test → QA-A · tài liệu / thiết kế / 要確認 → PM.
  **Hạ tầng** (đề không gán) → FE-A, FE-B vì FE dư sức còn BE là nút cổ chai. Cân tải trong từng cặp: BE-A 487h / BE-B 490h, FE-A 254h / FE-B 284h.
- **Iteration** (6 người × 52.5h = 315h trần lý thuyết; PM chỉ 30h → 292.5h / sprint): xếp theo phụ thuộc (item phụ thuộc phải cùng hoặc sớm hơn) và ưu tiên —
  Sprint 1 = nền tảng: E01 (đăng nhập, quyền), E11 (audit, mã lỗi, component), E12 (môi trường, khung job, DR sớm vì quyết định B′ / B
  ảnh hưởng cam kết NFR), bảng lõi của E02 / E03 / E07 / E08 / E09, các bước thiết kế (D33, SCR-20, SCR-28) và 4 issue 要確認 để có
  câu trả lời sớm. Sprint 2–3 = phần phụ thuộc kế tiếp (MFA, FS-03, căn cứ tham gia, 締め). Diễn tập DR, E2E, tài liệu API để cuối.
  Còn lại để trống Iteration (backlog). Tải: Sprint 1 240h · Sprint 2 222h · Sprint 3 165h — chi tiết `estimate.md` §4.

## 2. Spec → issue

| Spec (mã LAB-4) | Epic | Issue (số sub-issue) | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| SCR-01, 03; API-001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 013, 015, 020, 021, 023, 041, 043; DBT-01; CSP-01, 02, 03, 04, 19, 22; ADR-013 | #1 E01 基盤・認証・権限 | #2, #3 (2), #6 (2), #9, #10 (2), #15, #16 (4), #17, #25, #26, #30 (2) | SCR-02 (đăng nhập người tham gia bên ngoài) — ngoài 16 màn cốt lõi; LAB-4 chỉ thiết kế phần thiết bị dùng chung (WU-007) |
| SCR-05, 06; API-011, 012, 013, 014, 015, 016, 017, 018, 019; DBT-03, 04, 17; FS-03; CSP-09; ADR-014 | #33 E02 参加者・参加根拠（許可／承認） | #34, #35 (2), #38, #39 (2), #42, #43 (2), #46 (2), #49 (3), #53, #54 (2) | SCR-07 (cảnh báo sắp hết hiệu lực) — ngoài phạm vi thiết kế LAB-4 |
| SCR-08, 09, 10; API-022, 024, 025, 062; DBT-07, 18, 19; CSP-15, 20 | #57 E03 ロット・目利き／下見 | #58 (2), #61 (2), #64 (2), #67, #68 (2), #71 (2), #74 (2) | SCR-09 ngoài nút 公開 — LAB-4 chỉ cấp API-062 cho phần màn cốt lõi cần (D25) |
| SCR-11; API-026, 027, 028, 029, 030, 031, 032; DBT-08; DD-01; FS-03 | #77 E04 相対取引 | #78, #79 (2), #82, #83 (2), #86 (2) | SCR-12 (danh sách / tra giao dịch) — ngoài phạm vi thiết kế LAB-4 |
| SCR-13; API-034, 035, 036, 037, 038; DBT-09; DD-02; CSP-15 | #89 E05 せり結果 | #90 (2), #93 (4), #98 (2) | SCR-14 (lịch sử sửa せり) — ngoài phạm vi thiết kế LAB-4 |
| SCR-15, 16; API-040, 041, 042; DBT-10, 16, 21, 22, 23; DD-03 | #101 E06 引渡し | #104 (2), #107 (2), #110 (2), #113 (2), #116 | SCR-16 例外登録 — chưa có WU, hỏi ở #116; SCR-17 (tra cứu liên quan) — ngoài phạm vi LAB-4 |
| SCR-18, 19, 20, 28; API-004, 043, 044, 045, 046, 047, 048; DBT-05, 24, 25, 26, 28, 29, 30; DD-04; FS-02; CSP-01, 06; ADR-004, 007, 009 | #27 E07 業務日・締め・締め解除 | #28, #29, #117, #118 (2), #121, #122 (2), #126 (2), #125, #129, #130 (3), #136 (4), #141 (3) | Xuất đối soát lần đầu IF-ACC-01 / SCR-29 — chưa có WU, hỏi ở #125; SCR-35 (bảo trì lịch 休市) — ngoài phạm vi LAB-4 |
| SCR-06, 21, 22; API-016, 026, 033, 039, 049, 050, 051, 066, 067, 069; DBT-20, 21, 27; DD-05; CSP-10 | #102 E08 調整要求 | #103 (2), #147 (2), #160 (3), #167 (3), #171 (2), #174 (2), #164 (2) | SCR-32 (màn chung 証憑) — chỉ có API (D25), không có màn riêng |
| SCR-23, 24; API-052, 053, 054, 055, 056, 057, 058, 059; DBT-11, 12; DD-06; ADR-006 | #151 E09 規則・料率版 | #152 (2), #181 (2), #184 (2), #187 (2), #190 (2) | SCR-25 (lịch sử version) — ngoài phạm vi thiết kế LAB-4 |
| SCR-21, 26, 27; API-050, 060, 061, 063, 064, 065, 068, 069; DBT-11, 12, 13, 14, 20; DD-05, 07; FS-01; CSP-16, 17 | #150 E10 完納奨励金 | #153, #154 (2), #155, #156, #159 (2), #197 (2), #157, #200 (2), #203, #204 (3), #208 (2), #211 (2), #165 (5), #158 | — (đủ 12 WU; thêm D33 và 1 câu hỏi 要確認) |
| DBT-15; CSP-05, 07, 11, 15, 18, 21, 22; ADR-004, 007, 012 | #22 E11 監査・共通 | #23, #218 (2), #24 (2), #223 (2), #226, #227 | SCR-30 (tìm audit), SCR-31 (tra version áp dụng) — ngoài phạm vi thiết kế LAB-4 |
| DBT-31, 32; DD-07; ADR-001, 010 | #13 E12 インフラ・NFR | #228 (3), #233 (2), #14, #236 (2), #239 (3), #132, #232 (2), #133 (2) | Security test, lưu trữ cold FT-15-02, SCR-33 / 37 / 38 — không có WU trong handoff (LAB-1 tính ở hạng mục cố định / màn ngoài cốt lõi) |
| SCR-10, 13; API-001, 069; DBT-04, 07, 09; DD-01, 02, 03, 04, 05, 06; FS-02; CSP-03, 04, 05, 13, 15; ADR-013, 014 | #247 E13 テスト・移行・文書 | #248 (3), #252 (2), #255 (2), #258 (2), #261, #262, #263 | Migration dữ liệu khách, đào tạo, cutover, hypercare — hạng mục cố định LAB-1, ngoài thiết kế LAB-4 |
| 95 WU của handoff · 52 dòng `design_vs_prototype.md` (qua bảng dvp_map) | mọi epic | mỗi WU = 1 issue, tiêu đề `[WU-NNN]` | — (kiểm bằng `tools/check-backlog.py`) |
| FORM-LOT / TRADE / SERI / DEL-01 (phiếu PDF hiện trường) | — | — | LAB-4 không cấp API cho 受領票 PDF (D25) — ngoài phạm vi; làm khi có thiết kế |

## 3. Hạng mục chịu ràng buộc đặc thù — 完納奨励金

Lý do chung: 完納奨励金 là logic tiền có nhiều biến cùng lúc — version tỷ lệ / ngưỡng theo 発効日, ranh giới ngày trả (JST, gồm ngày hạn),
bảng tier, làm tròn xuống JPY một lần, delta cho kỳ đã 確定, trạng thái 暫定 / 確定 và người 確定. Gộp lại thì không ước, không test và
không theo dõi riêng được từng biến; sai một biến là sai tiền cả kỳ. Vì vậy mỗi biến là một issue riêng, cùng gắn `Constraint = 完納奨励金`
(lọc được trên Project), tổng giờ tính riêng ở `estimate.md` §4.

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Version tỷ lệ / ngưỡng áp dụng theo 業務日 | #153 | Sai version là sai tiền toàn kỳ; có ca biên 発効日 riêng |
| Khoản trả đủ hạn 以内 | #154 | Biến ngày + múi giờ JST + dạng 支払期日 chưa chốt (P2-1) |
| Tier và 交付率 | #155 | Ca biên đúng ngưỡng cần test độc lập |
| Làm tròn xuống JPY một lần, cấm float | #156 | Tiêu chí chấp nhận riêng của BR-INC-01 |
| Delta kỳ sau cho kỳ đã 確定 | #159 | Phụ thuộc version kỳ gốc và định nghĩa 「次期」 (P2-3, #158) |
| Batch tháng chỉ tạo 暫定 | #197 | Idempotent theo kỳ, chạy lại không nhân đôi (P3-1) |
| Cột DB cho thanh toán / kết quả | #157 | Nền dữ liệu của mọi bước tính; trigger bất biến khi 確定 |
| Màn 照会 SCR-27 | #200 | Hiển thị version, delta, phép tính — chỉ xem |
| Test vector INC-EDGE + ca biên | #203 | Bộ kiểm chứng chung cho #153〜#156 |
| Nhập 支払実績 (SCR-26) | #204 | Đầu vào quyết định 以内; CSV chưa chốt cột (P2-2) |
| Test tích hợp delta + batch chạy lại | #208 | Xuyên 3 thành phần (調整要求, delta, batch) |
| 確定 kỳ bởi ROLE-SETTLEMENT + nút SCR-26 | #211 | Chuyển trạng thái bất biến, dùng chung khóa với batch (P3-2, P1-4) |
| 調整要求 cho 支払実績 (D33) | #165 | Thiết kế mới, ảnh hưởng 4 tài liệu và số tiền kỳ sau (P1-3) |
| Định nghĩa 「次期」 | #158 | Câu hỏi làm rõ, chặn chốt #196 |

## 4. Chỗ hở / mâu thuẫn của spec LAB-4 phát hiện khi break

| # | Spec | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|---|
| G1 | SCR-20 (WU-093) | Màn có trong backlog nhưng không có screen spec, API chưa có ID | đã sửa thiết kế — PREMISE.md P1-1 |
| G2 | SCR-28 (WU-095) | Như G1 | đã sửa thiết kế — PREMISE.md P1-2 |
| G3 | DD-05 / SCR-21 / API-050 / API-069 / DBT-20 (WU-050, D33) | Quyết định sửa 支払完了日 qua 調整要求 đã có, nhưng 調整要求 chưa nhận đối tượng 支払実績 | đã sửa thiết kế — PREMISE.md P1-3 |
| G4 | SCR-26 / API-068 (WU-067, WU-091, D30) | Nút 確定 kỳ được đặt ở SCR-26 nhưng không WU nào nhận phần UI | đã sửa thiết kế — PREMISE.md P1-4 |
| G5 | ADR-013 未決 #4 / Database Design (WU-007) | Chưa có bảng thiết bị dùng chung và PIN; cấp / thu hồi thiết bị chưa rõ | tạo issue làm rõ #17 |
| G6 | SCR-15 ⑭ → SCR-16 (WU-039, WU-038) | SCR-15 có nút sang 例外登録 (SCR-16) nhưng SCR-16 không có WU; chỉ API-042 có | tạo issue làm rõ #116 |
| G7 | DBT-28 / DBT-29 (WU-046) | WU-046 xuất **lại** dữ liệu đối soát nhưng bản xuất lần đầu IF-ACC-01 (gắn SCR-29) không có WU; thuế và cột trạng thái DBT-29 vẫn 未決 | tạo issue làm rõ #125 |
| G8 | FS-01 / DD-05 (WU-062) | 「次期」 chưa định nghĩa khi nhiều kỳ chưa 確定 | tạo issue làm rõ #158 |
| G9 | ADR-006 未決 #7 (WU-059) | Dạng quy tắc 支払期日 chưa chốt | giả định — PREMISE.md P2-1 |
| G10 | SCR-26 / API-065 (WU-067) | Bộ cột CSV 支払実績 chưa chốt | giả định — PREMISE.md P2-2 |
| G11 | DBT-30 / SCR-28 (WU-094, WU-095) | Catalog có 3 báo cáo tháng RPT-10〜12 nhưng không WU nào sinh chúng | giả định — PREMISE.md P2-4 |
| G12 | ADR-010 (WU-076) | B′ hay B chỉ chốt được sau khi đo; câu hỏi khách `open_questions` #1 chỉ gửi khi lùi về B | để mở — có nhánh xử lý sẵn ở #235, chưa có số đo thì không quyết được |
| G13 | SCR-22 / FORM-CORR-01 (WU-051) | 「追加情報の要求」 là kết quả riêng trong form nhưng baseline gộp vào 却下 | để mở — câu hỏi khách non-blocking (`open_questions` #2) đã duyệt lời văn; baseline giữ P3-5 |
