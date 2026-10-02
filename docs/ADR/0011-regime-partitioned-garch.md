# ADR-0011: Regime-Partitioned GARCH (WP-4b.5)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/modeling/regime_garch.py` — stage 2 của Hybrid:
fit GARCH riêng trong từng regime + forecast + simulate path
**Liên quan:** ADR-0007 D2, ADR-0010 D4, ADR-0006 (GARCH baseline),
SCHEMA.md §8.2, WORKFLOW.md §5.1

---

## 1. Bối cảnh

Hybrid (ADR-0007): stage 1 = HMM gán nhãn regime (WP-4b, đã xong), stage 2 =
fit GARCH riêng trong từng regime. Thiết kế **decoupled** (ADR-0010 D4):
chỉ nhận mảng nhãn regime làm input, không phụ thuộc nguồn nhãn (per-asset
HMM bây giờ, market-factor HMM sau này).

## 2. Quyết định

### D1 — Fit pooled theo nhãn regime

Gộp toàn bộ ngày mang nhãn regime k thành MỘT chuỗi → fit GARCH trên chuỗi
đó → bộ tham số (ω, α, β, ν) riêng cho regime k.

Lý do: từng episode regime thường ngắn hơn `_MIN_GARCH_OBS` (100 ngày) —
vd đợt crisis 2018 chỉ 74 ngày. Pooled đảm bảo đủ dữ liệu và mô tả "cấu
trúc vol dynamics của riêng regime này" (2020 ≈ 2022 chung một GARCH_crisis).

### D2 — Forecast carry-over (không reset khi đổi regime)

Duyệt chuỗi theo thời gian thực, mang σ² qua ngày:

```text
σ²ₜ = ω[regimeₜ] + α[regimeₜ]·ε²ₜ₋₁ + β[regimeₜ]·σ²ₜ₋₁
```

Khi regime đổi → đổi tham số nhưng GIỮ σ² (không reset về long-run variance).
Lý do: sau khủng hoảng, vol cao kéo dài nhiều tuần — reset sẽ bỏ qua thực tế đó.

### D3 — Tách bạch FIT và FORECAST

```text
Pooled     → dùng cho HỌC THAM SỐ (parameters) — gộp episode không liền nhau
Carry-over → dùng cho MÔ PHỎNG/FORECAST — phải nối tiếp thời gian thực
```

### D4 — `simulate_regime_paths` cho scenario generation

API sinh n_paths chuỗi return theo regime:

```text
Mỗi ngày: rút ε ~ Student-t(ν[regimeₜ]) → cập nhật σ² theo regimeₜ
          → regimeₜ₊₁ rút từ transition matrix → carry-over σ² nếu đổi regime
```

Đây là nền tảng scenario generation (WP-5) — WP-4b.5 chỉ cung cấp API,
chưa tích hợp vào scenario engine.

### D5 — Lỗi: `ModelingError`

- Regime gộp < `_MIN_GARCH_OBS` (100) → ModelingError (regime quá hiếm để fit tin cậy)
- labels không khớp độ dài returns → ModelingError
- Deterministic với seed cố định (RULES-001)

## 3. Phạm vi

In: fit_regime_garch, forecast_regime_vol, simulate_regime_paths, tests
synthetic + benchmark OOS vs GARCH toàn chuỗi.
Out: market-factor HMM (WP-5), regime-conditioned distribution (WP-5),
scenario engine tích hợp (WP-5).

## 4. Hệ quả

- GARCH per regime được benchmark công bằng với baseline GARCH toàn chuỗi
  (không tuyên bố tốt hơn nếu chưa đo — RULES-043).
- Decoupled: khi C triển khai (market factor), chỉ đổi nguồn nhãn, không
  đổi code fit/forecast.

---

## 5. Measurement Outcome (bổ sung sau khi chạy survey 12 assets, k=3)

### Kết quả đo

| Asset | Regime days (k=3) | GARCH fit |
|---|---|---|
| XOM | [1453, 129, 1343] | ✅ OK — 3 regime đủ dữ liệu (Calm 1.05% / Volatile 1.82% / Crisis 3.59%) |
| AAPL, AMZN, GOOGL, JPM, META, MSFT, NVDA, GLD, QQQ, SPY, TLT | state hiếm nhất 19–78 ngày | ❌ ModelingError (regime < 100 ngày gộp) |

### Hàm ý

1. **k=2 là cấu trúc được dữ liệu ủng hộ** cho đa số assets (11/12):
   state thứ 3 của HMM là artifact khi không đủ dữ liệu. Chọn k cho
   GARCH per regime phải theo data (XOM: k=3 chạy được).
2. **Insight phương pháp luận tiềm năng:** ngưỡng GARCH-fittability hoạt
   động như một **tiêu chí regime validity** — regime không fit được
   volatility model riêng thì nghi ngờ không phải regime thật. Đây là
   phát hiện từ thực nghiệm, CHƯA phải quyết định — sẽ được cân nhắc
   đưa vào select_k protocol (khi đó mở ADR riêng).
3. Benchmark (WP-4b.5b) dùng k=2 làm mặc định; XOM k=3 làm case study.

### Quan sát: nu ngược trực giác (SPY, k=2)

```text
Calm  : nu = 7.5   ← innovation đuôi béo
Crisis: nu = 20.4  ← innovation gần Gaussian
```

Điều này NGƯỢC trực giác (kỳ vọng Crisis đuôi béo hơn), nhưng có lời
giải thích nhất quán: fat tails của khủng hoảng đã được **variance cao
của regime** hấp thụ — innovation sau khi chia cho σ lớn trông gần
Gaussian. Trong Calm (σ nhỏ), một outlier nhỏ tuyệt đối vẫn là cực đoan
tương đối → đuôi innovation béo.

Hàm ý: bằng chứng ủng hộ luận điểm "tách regime đã bắt phần lớn fat
tails" — liên quan trực tiếp quyết định Gaussian-vs-Student-t ở WP-5.
Là quan sát cần kiểm chứng thêm, không phải kết luận cuối.