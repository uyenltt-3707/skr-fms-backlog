# Estimate — SWP và giờ

## 1. Báo cáo HTML của skill chấm SWP

Đường dẫn: **`swp-report/swp-report-261030.html`** (tự chứa, mở trực tiếp) · dữ liệu `swp-report/swp-scores.yaml` · skill
`skills/swp-provisional/` (`SKILL.md`). Trạng thái: **bản nháp** — 「SWP tạm — thang điểm do PL tự đặt, chờ skill chính thức của chương trình; khi có sẽ chạy lại và thay thế」.

- Chấm 286 item lá theo mô tả issue (không dựa vào giờ); cha / epic = tổng con. Tổng SWP tạm **2,546**; riêng 完納奨励金 320.
- Độ tin cậy: cao 44 · vừa 163 · thấp 79 (77 trong đó là màn 概算).
- Kiểm chéo giờ / SWP (quy tắc 6): theo epic, E05 (+60%) và E06 (+52%) lệch quá ±50% so với tỉ lệ chung 1.21 h / SWP; E07 +13%,
  E11 +12%, E12 −31% (trong ngưỡng). 105 item lá lệch quá ±50% so với epic của nó (44 là màn 概算) → danh sách trong báo cáo §4.
- **Chưa ghi SWP lên Project** — chờ PL quyết các mẫu ở §2.

## 2. Issue mẫu skill chọn để kiểm

Skill chọn 14 mẫu (quy tắc ở `skills/swp-provisional/SKILL.md`): 3 SWP cao nhất, 2 thấp nhất, 5 độ tin cậy thấp, 3 Constraint =
完納奨励金, 2 ngẫu nhiên (seed cố định); #307 trúng hai quy tắc.

| Issue | Skill chấm (Scope × Complexity → SWP, độ tin cậy) | Bạn chốt | Lý do | Lý do chọn mẫu |
|---|---|---|---|---|
| #271 [SCR-04] 画面設計 — screen spec + cấp API-ID | 3 × 4 → **12** (thấp) | | | độ tin cậy thấp (màn 概算) |
| #307 [SCR-17] 実装 1/3 — API đọc / ghi | 2 × 1 → **2** (thấp) | | | SWP thấp nhất; độ tin cậy thấp (màn 概算) |
| #308 [SCR-17] 実装 2/3 — màn chính | 2 × 1 → **2** (thấp) | | | SWP thấp nhất |
| #310 [WU-094] Truy vấn + bộ cột RPT-04 滞留引渡し・引渡し例外 | 3 × 2 → **6** (vừa) | | | ngẫu nhiên (seed 20261030) |
| #175 [WU-052] Hàm giá trị hiệu lực (gốc + DBT-21) | 4 × 2 → **8** (thấp) | | | độ tin cậy thấp (không có dấu hiệu Complexity) |
| #194 [WU-059] Lọc khoản trả theo hạn ở JST + test biên ngày | 2 × 4 → **8** (cao) | | | Constraint = 完納奨励金 |
| #207 [WU-067] UI SCR-26 form + tải CSV | 3 × 2 → **6** (vừa) | | | Constraint = 完納奨励金 |
| #335 [WU-065] Hoàn thiện production — xử lý lỗi, test bổ sung, kiểm quyền | 2 × 3 → **6** (cao) | | | Constraint = 完納奨励金 |
| #342 [SCR-31] 画面設計 — screen spec + cấp API-ID | 3 × 4 → **12** (thấp) | | | độ tin cậy thấp (màn 概算) |
| #234 [WU-076] Đo dump + sao chép trong lúc chạy tải cao điểm FIG-LOAD-01 (điều kiện ADR-010) | 5 × 5 → **25** (cao) | | | SWP cao nhất (hòa điểm → rải theo issue cha) |
| #241 [WU-079] Dựng thử Postgres + Auth / API ở Osaka | 5 × 5 → **25** (vừa) | | | SWP cao nhất |
| #243 [WU-081] Dữ liệu + kịch bản tải FIG-LOAD-01 | 5 × 5 → **25** (vừa) | | | SWP cao nhất |
| #359 [SCR-37] 実装 1/3 — API đọc / ghi | 2 × 3 → **6** (thấp) | | | độ tin cậy thấp (màn 概算) |
| #380 [結合テスト] Delta → giá trị hiệu lực ở màn đọc, CSV đối soát 「調整済み」, báo cáo ngày | 5 × 4 → **20** (vừa) | | | ngẫu nhiên (seed 20261030) |

Lý do từng trục của mỗi mẫu: báo cáo HTML §2 và `swp-report/swp-scores.yaml`. PL điền `pl_final` / `pl_reason` ở file YAML
(cột "Bạn chốt" / "Lý do" ở bảng này cập nhật theo).

## 3. Cách quy ra giờ

**Cách đã chọn:** ước giờ **trực tiếp, từ dưới lên, cho từng item lá**; cha và epic tự cộng. PL đã duyệt 8 quy tắc dưới đây
(đề xuất ở B1, quy tắc 4 sửa ở B2).

**Vì sao:** item lá đủ nhỏ (≤ 15h) để người làm hình dung được việc cụ thể; SWP (B3) là cỡ tương đối nên không dùng để suy giờ —
giữ hai trường độc lập thì mới kiểm chéo được nhau (quy tắc 6).

| # | Quy tắc |
|---|---|
| 1 | Ước giờ trực tiếp theo từng issue, không suy từ SWP. SWP và giờ là hai trường độc lập. |
| 2 | Giờ gồm code + test + review + cập nhật tài liệu (Định nghĩa xong, `task-breakdown.md` §1.2). Không cộng buffer vào từng issue. |
| 3 | Làm tròn 0.5h, tối thiểu 1h, tối đa 15h / item lá (2 ngày công). Vượt thì tách sub-issue. |
| 4 | Item lá ước giờ trực tiếp. Issue cha và epic **cũng điền** 見積時間 (và SWP ở B3) = tổng các con, `tools/create-issues.py` tự cộng. Tổng trong file này chỉ cộng từ item lá để tránh cộng đôi. |
| 5 | Quy đổi MD = giờ / 7.5 (tiền đề LAB-1); đối chiếu tổng MD với LAB-1, chênh quá ±15% phải giải thích (§5). |
| 6 | Giờ / SWP theo từng epic dùng để kiểm tra chéo (B3): lệch quá ±50% so với trung bình epic thì rà lại. Không dùng để tính giờ. |
| 7 | Buffer và rủi ro để ở cấp dự án (không phân bổ vào issue). |
| 8 | 完納奨励金 là các issue riêng, gắn Constraint = 完納奨励金, có tổng riêng (§4). |

**Cách áp dụng nhất quán cho từng item lá:**

1. Ghi ra kết quả cụ thể phải giao (bảng / RPC / route / màn / bộ test) và tiêu chí xong — có trong body issue.
2. Chọn khoảng tham chiếu theo loại và độ khó (bảng dưới), lệch lên khi làm mới, lệch xuống khi chỉ sửa code prototype đã có.
3. Ước con số trong khoảng, làm tròn 0.5h. Vượt 15h → tách sub-issue và ước lại từng phần.
4. Ghi vào `tools/backlog.yaml`; `tools/check-backlog.py` kiểm 1h ≤ giờ ≤ 15h, bội 0.5, mọi lá có giờ.
5. **WU "sửa từ prototype"** (49 WU theo cột prototype của handoff): cộng **+25%** (≥ 1h, làm tròn lên 0.5h) cho item lá DB / API / UI /
   batch / hạ tầng — phần hoàn thiện lên production mà prototype chưa có: xử lý lỗi theo danh mục mã lỗi, test bổ sung (prototype
   không có test ma trận), kiểm quyền / RLS / audit (prototype còn nhánh demo). Vượt 15h → tách sub-issue "Hoàn thiện production".
   Không áp cho test / tài liệu. Tổng +166.5h (B2b, PL phát hiện).
6. **Màn chưa có thiết kế** (19 màn baseline LAB-1 ngoài 16 màn cốt lõi): ước thô 「詳細設計未作成のため概算」 — 実装 = năng suất LAB-1
   S / M / L = 2.5 / 5 / 10 MD × 7.5h, chia phần ≤ 15h; 画面設計 = 0.2 × 実装 (hệ số 詳細設計 của LAB-1). Ước lại sau 画面設計.
7. **Báo cáo E07:** 12 báo cáo khác nguồn dữ liệu và bộ cột → mỗi báo cáo một sub-issue, 6–14h tùy độ phức tạp của truy vấn (§5).
8. **Test tích hợp theo luồng** (B3a, PREMISE P3-7): mỗi đoạn luồng một sub-issue 10–14h (khoảng 'test'), 担当 QA-A; luồng dùng
   màn ước thô ghi 「概算」, Iteration trống, ước lại sau 画面設計.

Ví dụ trong bảng là giờ cơ sở (bước 2–3); WU sửa từ prototype còn cộng bước 5.

| Loại item lá | Khoảng tham chiếu / item lá | Ví dụ |
|---|---|---|
| DB / API — thấp (thêm cột, CHECK, đổi tham số route) | 4–8h | #2 5h, #9 6h |
| DB / API — vừa (bảng mới + RPC, route có nhiều mã lỗi) | 8–12h | #42 12h, #153 8h |
| DB / API — cao (RPC nguyên tử, hàm lõi, logic tiền) | 10–14h mỗi phần, thường tách 2–3 phần | #79 12h + 12h, #160 10h + 14h + 12h |
| UI — sửa màn prototype | 8–12h | #26 10h, #121 10h |
| UI — màn mới hoặc nhiều biến thể | 10–14h mỗi phần, tách theo nhóm biến thể | #49 14h + 12h + 12h |
| test | 6–14h mỗi bộ | #203 10h, #249 14h |
| hạ tầng | 4–14h | #227 4h, #229 14h |
| thiết kế màn / thiết kế bổ sung | 6–10h | #142 6h, #166 10h |
| 要確認 (soạn câu hỏi, theo dõi, cập nhật issue) | 1–1.5h | #116 1.5h |

Tham khảo công cụ: đã xem skill `tkm:estimate` / sub-skill `task-breakdown`; ở chế độ trước-estimate skill này **không sinh số giờ**,
nên chỉ dùng cấu trúc epic → story → task làm tham khảo. Mọi con số là ước của nhóm theo quy tắc trên (nguồn: `tools/backlog.yaml`).

## 4. Tổng theo epic

Chỉ cộng item lá. MD = giờ / 7.5. Tổng SWP = **SWP tạm, bản nháp** (chưa review, chưa ghi Project).

| Epic | Số issue (issue / sub-issue / lá) | Tổng SWP | Tổng giờ | MD | Ghi chú (giờ Sprint 1 / 2 / 3 / backlog) |
|---|---|---|---|---|---|
| #1 E01 基盤・認証・権限 | 13 / 20 / 26 | 240 | 262.5 | 35.0 | 33.5 / 98 / 25 / 106 |
| #33 E02 参加者・参加根拠（許可／承認） | 11 / 17 / 21 | 137 | 227.5 | 30.3 | 20 / 12.5 / 67.5 / 127.5 |
| #57 E03 ロット・目利き／下見 | 8 / 18 / 19 | 136 | 225 | 30.0 | 12.5 / 18.5 / 9 / 185 |
| #77 E04 相対取引 | 6 / 12 / 14 | 106 | 183.5 | 24.5 | 0 / 0 / 0 / 183.5 |
| #89 E05 せり結果 | 4 / 12 / 12 | 76 | 148 | 19.7 | 0 / 0 / 22.5 / 125.5 |
| #101 E06 引渡し | 7 / 18 / 19 | 122 | 224.5 | 29.9 | 1.5 / 0 / 0 / 223 |
| #27 E07 業務日・締め・締め解除 | 13 / 30 / 36 | 263 | 362 | 48.3 | 23 / 12.5 / 37.5 / 289 |
| #102 E08 調整要求 | 8 / 20 / 20 | 154 | 209 | 27.9 | 18 / 0 / 0 / 191 |
| #151 E09 規則・料率版 | 6 / 14 / 14 | 112 | 148 | 19.7 | 25 / 20 / 22 / 81 |
| #150 E10 完納奨励金 | 14 / 21 / 27 | 268 | 259 | 34.5 | 11 / 0 / 0 / 248 · Constraint 完納奨励金 |
| #22 E11 監査・共通 | 9 / 19 / 22 | 184 | 249.5 | 33.3 | 62.5 / 22.5 / 0 / 164.5 |
| #13 E12 インフラ・NFR | 13 / 31 / 33 | 416 | 349 | 46.5 | 36 / 22 / 46 / 245 · B3a +security test #367, restore lần 2 #371 |
| #247 E13 テスト・移行・文書 | 12 / 20 / 23 | 332 | 244 | 32.5 | 0 / 26 / 20 / 198 · B3a +5 luồng test tích hợp |
| **Tổng** | **124 / 252 / 286** | **2,546** | **3091.5** | **412.2** | |
| **Riêng 完納奨励金** (Constraint) | 15 / 24 / 30 | **320** | **291** | **38.8** | 9.4% tổng giờ; gồm D33 46h, RPT-07 10h (sub-issue ở E07), câu hỏi #158 1h, luồng test tích hợp #381 22h (E13) |

**Tải theo 担当(仮) × Iteration** (giờ; trần 52.5h / người / sprint, PM 30h):

| 担当(仮) | Sprint 1 | Sprint 2 | Sprint 3 | Backlog | Tổng |
|---|---|---|---|---|---|
| FE-A (trần 52.5) | 43.5 | 45 | 48 | 566.5 | 703 |
| FE-B (trần 52.5) | 48 | 52 | 45 | 553.5 | 698.5 |
| BE-A (trần 52.5) | 52 | 50 | 50 | 391 | 543 |
| BE-B (trần 52.5) | 52.5 | 51 | 52.5 | 397 | 553 |
| QA-A (trần 52.5) | 18 | 18 | 50 | 290 | 376 |
| PM (trần 30) | 29 | 16 | 4 | 169 | 218 |
| **Tổng** (trần 292.5) | **243** | **232** | **249.5** | 2367 | 3091.5 |

## 5. So với estimate LAB-1

Nguồn LAB-1: `06_estimate_wbs_cost_internal.xlsx` (tổng 1,539.9 MD gồm mọi pha, gián tiếp, buffer) và `06_premises.yaml` (hệ số pha).
So **cùng phạm vi**: trước hết xác định giờ LAB-5 (code + test + review + tài liệu, Định nghĩa xong) ứng với pha nào của LAB-1,
rồi chỉ lấy đúng các pha đó của LAB-1 để so.

**Bảng quy đổi pha** (I = 製造・単体テスト của các dòng WBS có trong backlog = 377.5 MD):

| Pha LAB-1 | Hệ số | Có trong giờ LAB-5? | Item LAB-5 tương ứng |
|---|---|---|---|
| 要件定義・基本設計 | 0.40 × I | Không — đã làm ở LAB-2〜4 | — |
| 詳細設計 | 0.20 × I | Chỉ phần **chưa thiết kế ở LAB-4** (19 màn ngoài cốt lõi + SCR-20 / 28) | sub-issue 画面設計 / thiết kế |
| 製造・単体テスト | 1.00 × I | Có | item DB / API / UI / batch (gồm phần 実装 ước thô) |
| 結合テスト | 0.30 × I | Có — một phần trong Định nghĩa xong của từng item (test API / tích hợp của item) + issue test riêng | item test |
| システムテスト, UAT支援 | 0.25 + 0.10 × I | Không | — |
| Cố định 非機能 (bảo mật, backup / restore, giám sát, tải) | 40 MD | Có một phần | E12 hạ tầng / test (DR, giám sát, load test, security test, restore lần 2) |
| Cố định khác (移行, 教育, 切替, hypercare, 機器テスト) | 134 MD | Không | — |
| Gián tiếp (PM / comtor / QA) + buffer 15% | — | Không (quy tắc 7) | — |

LAB-1 cùng phạm vi của mỗi epic = 1.3 × I(epic) + 0.2 × I(màn chưa thiết kế của epic) (+ 40 MD 非機能 ở E12).
Dòng LAB-1 **không có** trong backlog, đã loại khỏi cả hai phía (29 MD): phiếu PDF hiện trường ×4 (D25 không cấp API),
FT-13-01 xuất đối soát và FT-13-03 thuế (chờ #125), FT-15-02 chuyển kho cold.

| Phần (epic) | LAB-1 cùng phạm vi (MD) | LAB-5 (MD) | Chênh | Vì sao |
|---|---|---|---|---|
| E01 基盤・認証・権限 | 24.2 (1.3 × 17.5 + 0.2 × 7.5) | 34.9 | +10.6 (+44%) | Thêm middleware AAL2 cho ~30 endpoint và khung màn chung (LAB-1 để trong 共通基盤 — dòng E11); thiết bị dùng chung tách thiết kế + 3 phần cài đặt (P1-5); +25% hoàn thiện production |
| E02 参加者・参加根拠（許可／承認） | 29.8 (1.3 × 22.5 + 0.2 × 2.5) | 30.3 | +0.6 (+2%) | Trong ngưỡng |
| E03 ロット・目利き／下見 | 34.5 (1.3 × 25 + 0.2 × 10) | 30.0 | -4.5 (-13%) | Trong ngưỡng; SCR-08 / 10 sửa từ prototype, SCR-09 ước thô |
| E04 相対取引 | 34.5 (1.3 × 25 + 0.2 × 10) | 24.5 | -10.0 (-29%) | Route và RPC 確定 đã có ở prototype; SCR-12 ước thô theo năng suất LAB-1 |
| E05 せり結果 | 20.5 (1.3 × 15 + 0.2 × 5) | 19.7 | -0.8 (-4%) | Trong ngưỡng |
| E06 引渡し | 48.5 (1.3 × 35 + 0.2 × 15) | 29.7 | -18.8 (-39%) | RPC giao hàng và SCR-15 đã có ở prototype; SCR-16 / 17 ước thô |
| E07 業務日・締め・締め解除 | 122.6 (1.3 × 92 + 0.2 × 15) | 48.1 | -74.5 (-61%) | Xem giải thích E07 bên dưới |
| E08 調整要求 | 33.5 (1.3 × 25 + 0.2 × 5) | 27.9 | -5.6 (-17%) | API 証憑 dùng chung, màn SCR-32 ước thô; RPC quyết định 調整要求 tách 3 phần |
| E09 規則・料率版 | 27.0 (1.3 × 20 + 0.2 × 5) | 19.7 | -7.3 (-27%) | API soạn version là CRUD bản nháp; chọn version theo 発効日 (FT-10-03) tính ở E10 |
| E10 完納奨励金 | 45.5 (1.3 × 35 + 0.2 × 0) | 34.4 | -11.1 (-24%) | LAB-1 ước 2 khối 10 MD (calc_logic_F11); LAB-5 tách 14 issue nhỏ có test vector riêng; đã gồm D33 6.1 MD (P1-3) |
| E11 監査・共通 | 58.8 (1.3 × 42.5 + 0.2 × 17.5) | 33.3 | -25.5 (-43%) | 共通基盤 20 MD của LAB-1 trải sang E01 / E12 ở LAB-5 và một phần đã có ở prototype |
| E12 インフラ・NFR | 72.9 (1.3 × 23 + 0.2 × 15 + 40) | 46.5 | -26.4 (-36%) | B3a đã thêm security test #367 và diễn tập restore lần 2 #371 (+6.9 MD, P3-8); còn thiếu chuyển kho cold FT-15-02 — không có WU trong handoff |
| E13 テスト・移行・文書 (test xuyên epic, migration schema) | — (đã nằm trong 1.3 × I của từng epic) | 30.7 | — | Test E2E / quyền / khóa ngày của LAB-5 gom ở E13; B3a thêm 5 luồng test tích hợp (+17.3 MD, P3-7) |
| Khác LAB-5 (tài liệu, 要確認) | — (LAB-1 tính trong gián tiếp PM) | 2.5 | — | — |
| **Tổng** | **552.2** | **412.2** | **-140.0 (-25.4%)** | Xem kết luận (B2b: 387.9, −29.8%) |

**E07 — 12 báo cáo:** đã kiểm catalog (RPT-01〜12): mỗi báo cáo lấy từ nguồn dữ liệu khác nhau (giao dịch, lô, người tham gia,
giao hàng, đối soát, kế toán, 完納奨励金, điều chỉnh, tranh chấp; 3 báo cáo tháng) và có bộ cột riêng → **khác định dạng**. Đã tách mỗi
báo cáo thành một sub-issue và ước lại: 9 báo cáo ngày trong #136 (6–14h / báo cáo, RPT-05 / 06 chờ #125),
3 báo cáo tháng trong #141 (8–10h). Phần báo cáo LAB-5 = 166h = 22.1 MD so với LAB-1 (12 × 3 MD + SCR-28 + batch FT-12-04)
× 1.3 ≈ 59.5 MD. Vẫn thấp vì LAB-5 dùng **một** màn SCR-28 và **một** API xuất CSV chung cho 12 báo cáo, còn LAB-1 tính màn + lọc + CSV
riêng cho từng báo cáo. Còn rủi ro ước thiếu → kiểm chéo bằng SWP: bản nháp B3a cho E07 1.38 h / SWP, +13% so với tỉ lệ chung
(trong ±50%) — chưa thấy dấu hiệu ước thiếu; chờ PL review SWP.

**WU sửa từ prototype:** đã rà 49 WU (80 item lá). Giờ B2 chỉ tính phần sửa, chưa tính hoàn thiện lên production → cộng +25% cho item
DB / API / UI / batch / hạ tầng (§3 bước 5): **+166.5h (+22.2 MD)**; 3 item vượt 15h tách thêm sub-issue "Hoàn thiện production".

**Kết luận:** chênh −25.4% (B2b −29.8%; vẫn vượt ±15%). Nguyên nhân chính, theo thứ tự lớn → nhỏ:
1. **結合テスト:** LAB-1 0.3 × I = 113.2 MD. LAB-5 item test riêng (ngoài test 非機能 E12): **trước B3a 21.1 MD (158h) → sau B3a
   38.4 MD (288h)** nhờ 5 luồng test tích hợp theo luồng nghiệp vụ (+130h, P3-7); chênh 結合テスト giảm từ −92.1 MD xuống **−74.8 MD**.
   Phần còn lại là test API / tích hợp trong Định nghĩa xong của từng item. Hai luồng dùng màn ước thô (#384, #387) là 概算,
   ước lại sau 画面設計.
2. **E07 báo cáo** dùng chung màn + API (−37 MD so với cách tính từng báo cáo của LAB-1).
3. **Tái dùng prototype** ở E04 / E06 / E11 (route, RPC, khung chung đã có) dù đã cộng 25% hoàn thiện.
4. **E12**: B3a đã thêm security test và diễn tập restore lần 2 (+52h, PL quyết); còn thiếu chuyển kho cold FT-15-02.
Thay đổi ở PREMISE.md làm tăng giờ (P1-1〜P1-5: 74h; P1-6: 879h), không làm giảm. E07, E11, E12 kiểm chéo bằng SWP ở B3 (quy tắc 6) — nháp B3a: E07 +13%, E11 +12%, E12 −31% so với tỉ lệ chung
1.21 h / SWP (trong ±50%); E05 +60%, E06 +52% vượt ngưỡng → rà lại sau khi PL chốt SWP.

