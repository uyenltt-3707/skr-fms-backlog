# Estimate — SWP và giờ

## 1. Báo cáo HTML của skill chấm SWP

Đường dẫn: `swp-report/` — **chưa có** (skill chấm SWP và báo cáo HTML làm ở B3).

## 2. Issue mẫu skill chọn để kiểm

Chưa làm — B3 (chấm SWP). Bảng sẽ có cột: Issue · Skill chấm (Scope × Complexity → SWP) · Bạn chốt · Lý do.

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

Chỉ cộng item lá. MD = giờ / 7.5. Tổng SWP để trống chờ B3.

| Epic | Số issue (issue / sub-issue / lá) | Tổng SWP | Tổng giờ | MD | Ghi chú (giờ Sprint 1 / 2 / 3 / backlog) |
|---|---|---|---|---|---|
| #1 E01 基盤・認証・権限 | 11 / 12 / 18 | | 170 | 22.7 | 30 / 82 / 20 / 38 |
| #33 E02 参加者・参加根拠（許可／承認） | 10 / 13 / 17 | | 178 | 23.7 | 16 / 18 / 52 / 92 |
| #57 E03 ロット・目利き／下見 | 7 / 12 / 13 | | 119 | 15.9 | 10 / 10 / 15 / 84 |
| #77 E04 相対取引 | 5 / 6 / 8 | | 78 | 10.4 | 0 / 0 / 16 / 62 |
| #89 E05 せり結果 | 3 / 8 / 8 | | 84 | 11.2 | 0 / 10 / 8 / 66 |
| #101 E06 引渡し | 5 / 8 / 9 | | 75.5 | 10.1 | 1.5 / 6 / 0 / 68 |
| #27 E07 業務日・締め・締め解除 | 12 / 16 / 22 | | 223.5 | 29.8 | 21.5 / 10 / 34 / 158 |
| #102 E08 調整要求 | 7 / 16 / 16 | | 164 | 21.9 | 18 / 0 / 0 / 146 |
| #151 E09 規則・料率版 | 5 / 10 / 10 | | 98 | 13.1 | 20 / 0 / 0 / 78 |
| #150 E10 完納奨励金 | 14 / 20 / 26 | | 241 | 32.1 | 11 / 0 / 0 / 230 · Constraint 完納奨励金 |
| #22 E11 監査・共通 | 6 / 6 / 9 | | 73 | 9.7 | 50 / 18 / 0 / 5 |
| #13 E12 インフラ・NFR | 8 / 14 / 16 | | 162 | 21.6 | 62 / 42 / 0 / 58 |
| #247 E13 テスト・移行・文書 | 7 / 9 / 12 | | 114 | 15.2 | 0 / 26 / 20 / 68 |
| **Tổng** | **100 / 150 / 184** | | **1780** | **237.3** | |
| **Riêng 完納奨励金** (Constraint) | 14 / 20 / 26 | | **241** | **32.1** | 13.5% tổng giờ; gồm D33 46h và câu hỏi #158 1h |

**Tải theo 担当(仮) × Iteration** (giờ; trần 52.5h / người / sprint, PM 30h):

| 担当(仮) | Sprint 1 | Sprint 2 | Sprint 3 | Backlog | Tổng |
|---|---|---|---|---|---|
| FE-A (trần 52.5) | 52 | 38 | 4 | 160 | 254 |
| FE-B (trần 52.5) | 44 | 34 | 20 | 186 | 284 |
| BE-A (trần 52.5) | 47 | 52 | 52 | 336 | 487 |
| BE-B (trần 52.5) | 50 | 50 | 49 | 341 | 490 |
| QA-A (trần 52.5) | 18 | 28 | 40 | 112 | 198 |
| PM (trần 30) | 29 | 20 | 0 | 18 | 67 |
| **Tổng** (trần 292.5) | **240** | **222** | **165** | 1153 | 1780 |

## 5. So với estimate LAB-1

LAB-1 (`06_estimate_wbs_cost_internal.xlsx`): tổng **1,539.9 MD** gồm mọi pha, gián tiếp và buffer; phần gần nghĩa nhất với giờ
LAB-5 (code + test đơn vị + review + tài liệu) là **I = 製造・単体テスト = 406.5 MD**. Bảng dưới so LAB-5 với các dòng I của LAB-1
ứng với từng epic (cột LAB-1 ghi dòng nguồn). Dòng I của LAB-1 không có trong backlog (màn ngoài phạm vi LAB-4) ghi riêng ở cuối.

| Phần (epic) | LAB-1 (MD) | LAB-5 (MD) | Chênh | Vì sao |
|---|---|---|---|---|
| E01 基盤・認証・権限 | 15 (SCR-01, 02, 03) | 22.7 | +7.7 (+51%) | Thêm middleware AAL2 cho ~30 endpoint và khung màn chung (LAB-1 để trong 共通基盤); thiết bị dùng chung tách thiết kế + 3 phần cài đặt (P1-5, P2-6) |
| E02 参加者・参加根拠 | 20 (SCR-05, 06, FT-02-03) | 23.7 | +3.7 (+19%) | Nhánh 解除 / 再審査 theo loại người (FIG-004) và ma trận test FS-03 nặng hơn ước theo cỡ màn |
| E03 ロット・目利き／下見 | 25 (SCR-08, 09, 10, FT-03-03) | 15.9 | −9.1 (−36%) | SCR-09 (L, 10 MD) chỉ còn nút 公開; SCR-08 / 10 sửa từ prototype |
| E04 相対取引 | 15 (SCR-11, FT-05-02) | 10.4 | −4.6 (−31%) | Route và RPC 確定 đã có ở prototype, chỉ sửa |
| E05 せり結果 | 10 (SCR-13) | 11.2 | +1.2 (+12%) | Trong ngưỡng |
| E06 引渡し | 30 (SCR-15, 16, FT-07-02, 07-04) | 10.1 | −19.9 (−66%) | SCR-16 (10 MD) không có trong backlog (G6, #116); RPC giao hàng đã có ở prototype |
| E07 業務日・締め・締め解除 | 87 (SCR-18, 19, 20, 28, RPT×12, FT-08-01, 08-03, 12-04, 13-02) | 29.8 | −57.2 (−66%) | LAB-1 ước 3 MD / báo cáo × 12; LAB-5 làm 1 batch chung + 1 màn chung cho 12 báo cáo. **Chênh lớn nhất — cần rà ở B3** (rủi ro ước thiếu) |
| E08 調整要求 | 25 (SCR-21, 22, 32, FT-09-03) | 21.9 | −3.1 (−12%) | Trong ngưỡng |
| E09 規則・料率版 | 20 (SCR-23, 24, FT-10-03) | 13.1 | −6.9 (−35%) | FT-10-03 (chọn version theo 発効日) nằm ở E10 #153 trong LAB-5 |
| E10 完納奨励金 | 30 (SCR-26, 27, FT-11-02, 11-03) | 32.1 | +2.1 (+7%) | Gồm D33 6.1 MD (P1-3); bỏ D33 thì 26.0 MD (−13%) |
| E11 監査・共通 | 25 (FT-14-01 + 共通基盤 20) | 9.7 | −15.3 (−61%) | 共通基盤 của LAB-1 trải ra E01 / E11 / E12 ở LAB-5 và một phần đã có ở prototype |
| E12 インフラ・NFR | 48 (FT-17-01, 17-02 + cố định 非機能 40) | 21.6 | −26.4 (−55%) | Có load test, DR, giám sát; **chưa có security test** (không có WU trong handoff) và chỉ 1 lần diễn tập restore |
| E13 テスト・移行・文書 | — | 15.2 | — | LAB-1 tính test bằng hệ số pha (結合 0.30 × I, システム 0.25 × I); migration cố định 50 MD của LAB-1 là dữ liệu khách, khác WU-086 (schema prototype) |
| Dòng I LAB-1 không có trong backlog | 96.5 (SCR-04, 07, 12, 14, 17, 25, 29–31, 33–38; FORM×4; FT-15-02; FT-13-01) | — | — | Ngoài phạm vi thiết kế LAB-4 (16 màn cốt lõi + phần hệ thống cần) — `task-breakdown.md` §2 |
| **Tổng** | **406.5** (I) | **237.3** (1,780h) | **−169.2 (−41.6%)** | Vượt ±15%: (1) 96.5 MD của LAB-1 thuộc màn ngoài phạm vi; (2) 49 / 95 WU là sửa prototype, LAB-1 giả định làm mới; (3) LAB-1 ước theo cỡ màn (gồm API, thiết kế chi tiết trong màn), LAB-5 ước theo việc cụ thể; (4) báo cáo dùng chung batch + màn (E07). So cùng phạm vi (E01–E12 với dòng LAB-1 tương ứng + 非機能 40 MD): 222.1 vs 350 MD = −36.5% |

Kết luận: chênh không do thay đổi ở PREMISE.md (P1-1〜P1-5 làm **tăng** 74h = 9.9 MD: #131 8h, #142 6h, #165 46h, #213 6h, #18 8h), mà do phạm vi và việc tái dùng prototype.
Ba epic chênh âm lớn (E07, E06, E11) sẽ được kiểm chéo bằng SWP ở B3 (quy tắc 6) trước khi chốt.
