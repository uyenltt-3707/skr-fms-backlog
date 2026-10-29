# SKR-FMS Backlog

## 1. Dự án

**Dự án:** SKR-FMS — Sakura Fish Market Operations Support · **Mã học viên:** uyenltt3707 · **Đề:** Product A (LAB-5)

> Repo và GitHub Project này **công khai**: chỉ nội dung tự viết, chỉ ghi **mã** spec LAB-4 (SCR-/API-/DBT-/ADR-/DD-/FS-/WU-);
> không chép RFP hay văn bản spec, không dữ liệu thật, không dữ liệu cá nhân, không khóa bí mật.
> Sprint và người phụ trách (担当(仮)) là **giả lập**.

## 2. Tổng quan

- **Nguồn break:** bản LAB-4 = repo `product-a-fishmarket` commit **`576480b`** ("lab4: final decisions, PL remarks"),
  ngày commit **2026-10-29 20:58 (+07:00)**; nguồn break là `specs/_meta/lab5_handoff.yaml` — 95 đơn vị công việc WU-001〜095.
- **PREMISE.md: có thay đổi** so với LAB-4 — 6 dòng spec thêm / sửa (thiết kế màn SCR-20 và SCR-28, mở rộng 調整要求 sang
  支払実績 theo D33, nút 確定 ở SCR-26, bảng thiết bị dùng chung, 19 màn baseline LAB-1 ngoài 16 màn cốt lõi), 9 giả định bổ sung,
  6 hướng đã chốt.
- **Backlog (sau B2b):** 13 epic · 117 issue · 236 sub-issue (270 item lá) · **2,909.5h = 387.9 MD**; riêng 完納奨励金 269h (37 item).
  Trong đó 17 issue màn ước thô (879h, 「詳細設計未作成のため概算」). 4 issue `要確認`, 14 chỗ hở spec ở `task-breakdown.md` §4.
  So LAB-1 cùng phạm vi: 552.2 → 387.9 MD (−29.8%, giải thích ở `estimate.md` §5).
- **Sprint giả lập:** chưa chạy. Đã xếp kế hoạch Sprint 1 (2026-11-02〜11-15, 243h) · Sprint 2 (232h) · Sprint 3 (249.5h);
  195 item lá còn ở backlog. Lý do xếp: `task-breakdown.md` §1.3. Báo cáo tiến độ: `progress-report.md` (bước sau).

## 3. Liên kết

| Mục | Đường dẫn |
|---|---|
| Repo | https://github.com/uyenltt-3707/skr-fms-backlog |
| GitHub Project "SKR-FMS Backlog" (#2) | https://github.com/users/uyenltt-3707/projects/2 |
| Báo cáo HTML chấm SWP | `swp-report/` (B3 — chưa có) |
| Mapping id nội bộ ↔ issue | `tools/issue-map.json` |

Kiểm tra truy cập không đăng nhập: `tools/check-backlog.py --remote` gửi request không cookie / token tới Project và 3 issue mẫu,
nhận HTTP 200 (2026-10-29). Mở thử bằng cửa sổ ẩn danh của trình duyệt: [PL điền — ngày, kết quả].

**Cách đọc Project:** view **Board** (cột theo Status) và **Table** (lọc theo mọi trường). Trường:

| Trường | Giá trị |
|---|---|
| Status | Todo · In Progress · In Review · Done |
| Iteration | Sprint 1–3 (giả lập), 2 tuần / sprint, từ 2026-11-02; trống = backlog |
| SWP | trống ở B2; chỉ ghi SWP đã review (B3) |
| 見積時間 / Estimate (hours) | item lá: ước trực tiếp; issue cha / epic: tổng con |
| 担当(仮) | FE-A · FE-B · BE-A · BE-B · QA-A · PM (giả định, không gán tài khoản thật) |
| Item Type | Epic · Issue · Sub-issue (tên "Type" bị GitHub giữ chỗ) |
| Constraint | 完納奨励金 · なし |

## 4. Cấu trúc repo

| File / thư mục | Nội dung |
|---|---|
| `README.md` | Tổng quan, liên kết, cấu trúc, bảng spec → epic (file này) |
| `PREMISE.md` | Backlog khác bản LAB-4 ở đâu: spec thêm / sửa, giả định bổ sung, hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task, spec → issue, hạng mục 完納奨励金, chỗ hở spec LAB-4 |
| `estimate.md` | Báo cáo SWP (B3), cách quy ra giờ, tổng theo epic, so với LAB-1 |
| `progress-report.md` | Báo cáo tiến độ Sprint giả lập (bước sau) |
| `AI-report.md` | Skill / prompt đã dùng, review output AI, điểm cần cải thiện |
| `process_log.md` | Nhật ký thao tác theo thời gian |
| `tools/` | Dữ liệu backlog và script: `backlog.yaml` (dữ liệu tự viết), `create-issues.py` (tạo / đồng bộ issue + Project, idempotent), `check-backlog.py` (kiểm tra), `scan-content.py` (quét chép nguyên văn / email / khóa), `backlog_model.py`, `github_api.py`, `project_fields.py` (module dùng chung), `issue-map.json` (mapping sinh ra), `setup-github-project.sh` (dựng Project, B1) |
| `swp-report/` | Báo cáo HTML của skill chấm SWP (B3) — đang trống |
| `skills/` | Skill tự viết (B3) — đang trống |
| `.gitignore` | Loại file bí mật, file tạm, thư mục công cụ cục bộ (`.claude/`, `plans/`) |
| `.gitattributes` | Ép LF cho script shell |

Chạy lại: `python tools/create-issues.py` (cần `gh` đăng nhập scope `repo` + `project`, Python có PyYAML), rồi
`python tools/check-backlog.py --remote` và `python tools/scan-content.py`.

## 5. Spec → epic

| Spec (mã / file LAB-4, hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| SCR-01, 02, 03, 04; API-001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 013, 015, 020, 021, 023, 041, 043; DBT-01; CSP-01, 02, 03, 04, 19, 22; ADR-013 | #1 — E01 基盤・認証・権限 | PREMISE P1-5, P2-6; màn ước thô #265, #270 (P1-6) |
| SCR-05, 06, 07; API-011, 012, 013, 014, 015, 016, 017, 018, 019; DBT-03, 04, 17; FS-03; CSP-09; ADR-014 | #33 — E02 参加者・参加根拠（許可／承認） | màn ước thô #275 (P1-6) |
| SCR-08, 09, 10; API-022, 024, 025, 062; DBT-07, 18, 19; CSP-15, 20 | #57 — E03 ロット・目利き／下見 | màn ước thô #279 (P1-6) |
| SCR-11, 12; API-026, 027, 028, 029, 030, 031, 032; DBT-08; DD-01; FS-03 | #77 — E04 相対取引 | màn ước thô #286 (P1-6) |
| SCR-13, 14; API-034, 035, 036, 037, 038; DBT-09; DD-02; CSP-15 | #89 — E05 せり結果 | màn ước thô #293 (P1-6) |
| SCR-15, 16, 17; API-040, 041, 042; DBT-10, 16, 21, 22, 23; DD-03 | #101 — E06 引渡し | 1 issue 要確認 (G6); màn ước thô #298, #305 (P1-6) |
| SCR-18, 19, 20, 28, 29; API-004, 043, 044, 045, 046, 047, 048; DBT-05, 24, 25, 26, 28, 29, 30; DD-04; FS-02; CSP-01, 06; ADR-004, 007, 009 | #27 — E07 業務日・締め・締め解除 | PREMISE P1-1, P1-2, P2-4; 1 issue 要確認 (G7); 12 báo cáo tách riêng (B2b); màn ước thô #320 (P1-6) |
| SCR-06, 21, 22, 32; API-016, 026, 033, 039, 049, 050, 051, 066, 067, 069; DBT-20, 21, 27; DD-05; CSP-10 | #102 — E08 調整要求 | PREMISE P3-5, P3-6; màn ước thô #325 (P1-6) |
| SCR-23, 24, 25; API-052, 053, 054, 055, 056, 057, 058, 059; DBT-11, 12; DD-06; ADR-006 | #151 — E09 規則・料率版 | màn ước thô #330 (P1-6) |
| SCR-21, 26, 27; API-050, 060, 061, 063, 064, 065, 068, 069; DBT-11, 12, 13, 14, 20; DD-05, 07; FS-01; CSP-16, 17 | #150 — E10 完納奨励金 | **Constraint = 完納奨励金** cho mọi item; PREMISE P1-3, P1-4, P2-1〜P2-3, P2-5, P3-1〜P3-3 |
| SCR-30, 31, 34, 35, 36; DBT-11, 14, 15, 23, 24; CSP-05, 07, 11, 15, 18, 21, 22; ADR-004, 007, 012 | #22 — E11 監査・共通 | màn ước thô #336, #341, #346 (P1-6) |
| SCR-33, 37, 38; DBT-31, 32; DD-07; ADR-001, 010 | #13 — E12 インフラ・NFR | PREMISE P3-4 (DR B′ / B); màn ước thô #352, #357, #362 (P1-6) |
| SCR-10, 13; API-001, 069; DBT-04, 07, 09; DD-01, 02, 03, 04, 05, 06; FS-02; CSP-03, 04, 05, 13, 15; ADR-013, 014 | #247 — E13 テスト・移行・文書 | — |
| PREMISE P1-1 (thiết kế SCR-20) | #27 — E07 業務日・締め・締め解除 | #131 trước #134, #135 |
| PREMISE P1-2 (thiết kế SCR-28) | #27 — E07 業務日・締め・締め解除 | #142 trước #143, #144 |
| PREMISE P1-3 (調整要求 → 支払実績, D33) | #150 — E10 完納奨励金 | #165, Constraint = 完納奨励金 |
| PREMISE P1-4 (nút 確定 SCR-26) | #150 — E10 完納奨励金 | #213, Constraint = 完納奨励金 |
| PREMISE P1-5 (bảng thiết bị dùng chung) | #1 — E01 基盤・認証・権限 | #18 |
