# Estimate — SWP và giờ

## 1. Báo cáo HTML của skill chấm SWP

Đường dẫn bản chốt: **`swp-report/swp-report-261030-final.html`** (tự chứa, mở trực tiếp) · bản nháp giữ lại để so trước / sau:
`swp-report/swp-report-261030.html` · dữ liệu `swp-report/swp-scores.yaml` · giải thích kiểm chéo `swp-report/cross-check-notes.yaml`
· skill `skills/swp-provisional/` (`SKILL.md`). Nhãn vẫn là 「SWP tạm — thang điểm do PL tự đặt, chờ skill chính thức của chương trình; khi có sẽ chạy lại và thay thế」.

- **Đã review:** PL quyết 14 mẫu (§2) và thêm 3 quy tắc sửa có hệ thống R1–R3, chấm lại toàn bộ 286 item lá. Tổng SWP
  **2,546 (nháp) → 2,516 (đã review)**, 68 item đổi; riêng 完納奨励金 320 → 320 (#158 −3 theo R3, #207 +3 theo PL).
- Độ tin cậy sau review: cao 41 · vừa 236 · thấp 9 (nháp: 44 / 163 / 79 — 73 item màn 概算 lên "vừa" nhờ R2).
- Kiểm chéo giờ / SWP (quy tắc 6): **không epic nào lệch quá ±50%** (tỉ lệ chung 1.23 h / SWP). Nháp có E05 +60%, E06 +52%; sau
  review E05 +47%, E06 +28%. Sát ngưỡng: E05 +47%, E13 −40% — giải thích ở §4. Item lá lệch quá ±50% so với epic: 105 → 79.
- **Đã ghi SWP lên Project #2** cho 389 item (lá = điểm đã review, cha / epic = tổng con), đọc lại bằng API khớp từng item (§4).

## 2. Issue mẫu skill chọn để kiểm — quyết định PL

Skill chọn 14 mẫu (quy tắc ở `skills/swp-provisional/SKILL.md`): 3 SWP cao nhất, 2 thấp nhất, 5 độ tin cậy thấp, 3 Constraint =
完納奨励金, 2 ngẫu nhiên (seed cố định); #307 trúng hai quy tắc. "Skill chấm" = bản nháp PL đã kiểm. Lý do ghi nguyên văn vào
`swp-scores.yaml` (`pl_final`, `pl_reason`; thêm `pl_scope` / `pl_complexity`).

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| #271 [SCR-04] 画面設計 — screen spec + cấp API-ID | 3 × 4 → 12 | 2 × 2 → **4** | Chấm lại theo quy tắc R2 — SCR-04 ở LAB-1 = S. |
| #307 [SCR-17] 実装 1/3 — API đọc / ghi | 2 × 1 → 2 | 2 × 3 → **6** | Chấm lại theo quy tắc R2 — SCR-17 ở LAB-1 = M. |
| #308 [SCR-17] 実装 2/3 — màn chính | 2 × 1 → 2 | 2 × 3 → **6** | Chấm lại theo quy tắc R2 — SCR-17 ở LAB-1 = M. |
| #310 [WU-094] Truy vấn + bộ cột RPT-04 滞留引渡し・引渡し例外 | 3 × 2 → 6 | 3 × 2 → **6** | Giữ 6. |
| #175 [WU-052] Hàm giá trị hiệu lực (gốc + DBT-21) | 4 × 2 → 8 | 2 × 4 → **8** | Sửa trục Scope 4 → 2, Complexity 2 → 4, SWP giữ 8 — một thành phần (hàm DB) nhưng logic nhiều biến (loại người tham gia → loại căn cứ, ngày nghiệp vụ 02:00, trạng thái đình chỉ). Tổng đúng nhưng lý do của skill sai. |
| #194 [WU-059] Lọc khoản trả theo hạn ở JST + test biên ngày | 2 × 4 → 8 | 2 × 4 → **8** | Giữ 8 — 以内 bao gồm ngày hạn, ngày JST, theo kỳ: logic nhiều biến. |
| #207 [WU-067] UI SCR-26 form + tải CSV | 3 × 2 → 6 | 3 × 3 → **9** | Sửa Complexity 2 → 3, SWP 6 → 9 — tải CSV phải kiểm từng dòng, báo lỗi từng dòng, chặn khi kỳ đã 確定, phân quyền. |
| #335 [WU-065] Hoàn thiện production — xử lý lỗi, test bổ sung, kiểm quyền | 2 × 3 → 6 | 2 × 3 → **6** | Giữ 6. |
| #342 [SCR-31] 画面設計 — screen spec + cấp API-ID | 3 × 4 → 12 | 2 × 3 → **6** | Chấm lại theo quy tắc R2 — SCR-31 ở LAB-1 = M. |
| #234 [WU-076] Đo dump + sao chép trong lúc chạy tải cao điểm FIG-LOAD-01 (điều kiện ADR-010) | 5 × 5 → 25 | 5 × 5 → **25** | Giữ 25 — hạ tầng toàn hệ thống, kết quả bất định, là điều kiện của ADR-010. |
| #241 [WU-079] Dựng thử Postgres + Auth / API ở Osaka | 5 × 5 → 25 | 5 × 5 → **25** | Giữ 25 — hạ tầng toàn hệ thống, phụ thuộc bên ngoài (giới hạn Supabase). |
| #243 [WU-081] Dữ liệu + kịch bản tải FIG-LOAD-01 | 5 × 5 → 25 | 5 × 3 → **15** | Sửa Complexity 5 → 3, SWP 25 → 15 — "NFR" không đồng nghĩa bất định; tạo dữ liệu và kịch bản tải là việc xác định, độ phức tạp nằm ở nhiều kịch bản (quy tắc R1). |
| #359 [SCR-37] 実装 1/3 — API đọc / ghi | 2 × 3 → 6 | 2 × 3 → **6** | Chấm lại theo quy tắc R2 — SCR-37 ở LAB-1 = M. |
| #380 [結合テスト] Delta → giá trị hiệu lực ở màn đọc, CSV đối soát 「調整済み」, báo cáo ngày | 5 × 4 → 20 | 5 × 4 → **20** | Giữ 20 — xuyên nhiều chức năng, logic tiền. |

Kết quả mẫu so với bản nháp: 6 giữ nguyên, 1 giữ tổng nhưng sửa lý do (#175), 7 đổi (5 theo R2, #243 theo R1, #207 riêng).

**Quy tắc sửa có hệ thống (PL quyết 2026-10-30, áp cho mọi item cùng loại, không chỉ mẫu)** — đã thêm vào thang điểm trong
`skills/swp-provisional/SKILL.md` và `swp_rubric.py`, chấm lại toàn bộ. Hai bước tách riêng: dòng R1–R3 = bản nháp → skill
chấm lại theo quy tắc; dòng PL = skill chấm lại → giá trị PL chốt cho 14 mẫu; dòng tổng = bản nháp → giá trị đã ghi lên Project.

| # | Quy tắc | Item áp | Item đổi SWP | SWP trước → sau |
|---|---|---|---|---|
| R1 | Complexity 5 chỉ khi kết quả bất định (đo đạc, phụ thuộc bên ngoài, yêu cầu chưa chốt). Việc chủ đề NFR nhưng làm theo quy trình xác định → chấm theo độ phức tạp thực tế. | 7 | 7 | 135 → 79 (−56) |
| R2 | Màn 概算 (画面設計 và 実装 k/n): Scope 2; Complexity theo độ phức tạp màn ở LAB-1 (`04_screens.yaml`): S → 2, M → 3, L → 4. | 73 | 57 | 427 → 452 (+25) |
| R3 | Issue 要確認 (đi hỏi làm rõ): Scope 1 × Complexity 2 = 2. | 4 | 4 | 20 → 8 (−12) |
| PL | PL chốt 14 mẫu (skill chấm lại → Bạn chốt): đổi #241 10 → 25, #243 20 → 15, #207 6 → 9; #175 đổi trục, giữ tổng | 14 | 3 | 137 → 150 (+13) |
| | **Tổng mọi item lá** | 286 | 68 | **2,546 → 2,516 (−30)** |

- **R1** đổi #240, #372 (viết / sửa thủ tục restore: 5 → 2), #368〜#370 (security test: Complexity 5 → 3, 25 → 15), #243 (luật
  cho 5 × 4 = 20 vì mô tả issue cha có «đồng thời»; PL chốt 5 × 3 = 15), #241 (luật hạ còn 5 × 2 = 10 vì bất định chỉ có ở issue
  cha; PL giữ 25 — phụ thuộc bên ngoài «giới hạn Supabase» không có trong mô tả nên luật không thấy được). Giữ 5 vì đo đạc / yêu cầu chưa chốt: #234, #242, #244, #316, #373 (đo
  RTO / p95 / thời gian), #235, #262 (câu hỏi khách, 未決).
- **R2** áp cho 73 sub-issue màn 概算 của 19 màn (mọi `実装 k/n`, không chỉ `/3`; SCR-34〜36 cùng S). 16 item không đổi vì luật cũ đã
  cho cùng điểm. Lên: màn L (SCR-09 / 12 / 16) và phần 3/3 "biến thể, xử lý lỗi, test"; xuống: 画面設計 Scope 3 → 2, màn S.
- **R3** áp cho #17, #116, #125, #158: 5 → 2.
- Cách áp khi cài luật — **PL đã xác nhận (2026-10-30)**: bất định phải là của **chính item** — mô tả issue cha chỉ cho Complexity
  tối đa 4 (nếu không, #240 / #372 viết thủ tục vẫn 5 vì issue cha có «RTO»); R2 áp mọi `実装 k/n`; SCR-34〜36 lấy mức cao nhất;
  `結合テスト・概算` không áp R2.
- #241, #243 giữ giá trị PL chốt (không đổi SWP đã ghi). Mô tả #241 đã bổ sung phụ thuộc giới hạn Supabase (không chọn được region
  backup, không có region Osaka) — bài học chất lượng ticket (`AI-report.md` §2).

## 3. Cách quy ra giờ

**Cách đã chọn:** ước giờ **trực tiếp, từ dưới lên, cho từng item lá**; cha và epic tự cộng. PL đã duyệt 9 quy tắc dưới đây
(đề xuất ở B1, quy tắc 4 sửa ở B2, quy tắc 9 thêm ở B5).

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
| 9 | Ước lại theo thực tế (PL duyệt 2026-10-30): từ Sprint 2 ghi giờ thực tế từng item; epic nào có thực tế lệch quá **25%** so với ước tính (tính trên các item đã xong của epic) thì ước lại phần còn lại của epic đó, báo PL. |

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

Chỉ cộng item lá. MD = giờ / 7.5. Tổng SWP = **SWP đã review** (PL quyết mẫu + R1–R3), đã ghi lên trường `SWP` của Project #2
(cha / epic trên Project = tổng con, đọc lại bằng API khớp). Giờ / SWP so với tỉ lệ chung 1.23 h / SWP (quy tắc 6, ngưỡng ±50%).

| Epic | Số issue (issue / sub-issue / lá) | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|
| #1 E01 基盤・認証・権限 | 13 / 20 / 26 | 224 | 262.5 | 35.0 MD · Sprint 33.5 / 98 / 25 / backlog 106 · SWP nháp 240 (R2 SCR-02 / 04; R3 #17) · giờ / SWP −5% |
| #33 E02 参加者・参加根拠（許可／承認） | 11 / 17 / 21 | 135 | 227.5 | 30.3 MD · 20 / 12.5 / 67.5 / 127.5 · nháp 137 (R2 SCR-07) · +37% |
| #57 E03 ロット・目利き／下見 | 8 / 18 / 19 | 147 | 225 | 30.0 MD · 12.5 / 18.5 / 9 / 185 · nháp 136 (R2 SCR-09 = L) · +25% |
| #77 E04 相対取引 | 6 / 12 / 14 | 117 | 183.5 | 24.5 MD · 0 / 0 / 0 / 183.5 · nháp 106 (R2 SCR-12 = L) · +28% |
| #89 E05 せり結果 | 4 / 12 / 12 | 82 | 148 | 19.7 MD · 0 / 0 / 22.5 / 125.5 · nháp 76 (R2 SCR-14) · **+47%** sát ngưỡng: WU-033〜035 sửa từ prototype, giờ gồm +25% hoàn thiện production, 4 / 12 lá chạm trần 15h — SWP không tính phần này; không sửa giờ |
| #101 E06 引渡し | 7 / 18 / 19 | 143 | 224.5 | 29.9 MD · 1.5 / 0 / 0 / 223 · nháp 122 (R2 SCR-16 = L, SCR-17; R3 #116) · +28% (nháp +52%) |
| #27 E07 業務日・締め・締め解除 | 13 / 30 / 36 | 252 | 362 | 48.3 MD · 23 / 12.5 / 37.5 / 289 · nháp 263 (R2 SCR-29; R3 #125) · +17% |
| #102 E08 調整要求 | 8 / 20 / 20 | 160 | 209 | 27.9 MD · 18 / 0 / 0 / 191 · nháp 154 (R2 SCR-32) · +6% |
| #151 E09 規則・料率版 | 6 / 14 / 14 | 104 | 148 | 19.7 MD · 25 / 20 / 22 / 81 · nháp 112 (R2 SCR-25) · +16% |
| #150 E10 完納奨励金 | 14 / 21 / 27 | 268 | 259 | 34.5 MD · 11 / 0 / 0 / 248 · Constraint 完納奨励金 · nháp 268 (#207 +3 theo PL, #158 −3 theo R3) · −21% |
| #22 E11 監査・共通 | 9 / 19 / 22 | 171 | 249.5 | 33.3 MD · 62.5 / 22.5 / 0 / 164.5 · nháp 184 (R2 SCR-30 / 31 / 34〜36) · +19% |
| #13 E12 インフラ・NFR | 13 / 31 / 33 | 381 | 349 | 46.5 MD · 36 / 22 / 46 / 245 · nháp 416 (R1 −46: security test, thủ tục restore, #243; R2 SCR-33 / 37 / 38 +11) · −25% |
| #247 E13 テスト・移行・文書 | 12 / 20 / 23 | 332 | 244 | 32.5 MD · 0 / 26 / 20 / 198 · nháp 332 · **−40%**: mỗi đoạn luồng 結合テスト là sub-issue 10–14h nhưng giữ Scope 5 (xuyên chức năng) → giờ / SWP thấp có tính cấu trúc; không sửa giờ |
| **Tổng** | **124 / 252 / 286** | **2,516** | **3091.5** | 412.2 MD · nháp 2,546 (−30) · không epic nào lệch quá ±50% |
| **Riêng 完納奨励金** (Constraint) | 15 / 24 / 30 | **320** | **291** | 38.8 MD · 9.4% tổng giờ, 12.7% tổng SWP · giờ / SWP 0.91 (−26%) · gồm D33 46h, RPT-07 10h (sub-issue ở E07), câu hỏi #158 (R3: 5 → 2), luồng test tích hợp #381 22h (E13); nháp 320 |

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

Sprint 1 **giả lập** (B4): giờ ước không đổi; Done 155.5h / 243h, 182 / 281 SWP; 9 item carry-over (`progress-report.md` §2). Chưa có giờ thực tế nên chưa so thực tế / ước.

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
riêng cho từng báo cáo. Còn rủi ro ước thiếu → kiểm chéo bằng SWP: SWP đã review (B3b) cho E07 1.44 h / SWP, +17% so với tỉ lệ chung
(trong ±50%) — chưa thấy dấu hiệu ước thiếu.

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
Thay đổi ở PREMISE.md làm tăng giờ (P1-1〜P1-5: 74h; P1-6: 879h), không làm giảm. E07, E11, E12 kiểm chéo bằng SWP đã review (B3b, quy tắc 6): E07 +17%, E11 +19%, E12 −25% so với tỉ lệ chung
1.23 h / SWP (trong ±50%); E05 / E06 nháp vượt ngưỡng (+60% / +52%) nay +47% / +28% — không epic nào vượt ±50% (§4).

