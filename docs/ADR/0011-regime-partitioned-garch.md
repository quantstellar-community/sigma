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
synthetic + benchmark OOS vs baselines naive (constant/rolling/ewma).
Out: market-factor HMM (WP-5), regime-conditioned distribution (WP-5),
scenario engine tích hợp (WP-5).

## 4. Hệ quả

- GARCH per regime được benchmark công bằng với các baseline naive
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
3. Benchmark (WP-4b.5b) dùng k=2 làm mặc định — k=3 (vd XOM) là extension
   tiềm năng, KHÔNG phải case study của paper core (tập trung quantum
   experiment per regime với k=2).

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

---

## 6. Benchmark Outcome (WP-4b.5b — OOS, causal labels, 250 ngày × 3 assets)

Protocol: HMM refit expanding-window (63 ngày), nhãn regime **causal**
(predict từng ngày với model fit trên data ≤ t — không lookahead), cùng
ladder tiêu chí (VaR viol 95/99 + MAE) với các baseline naive
(constant/rolling/ewma).

| Asset | ewma viol95 | garch-regime viol95 | MAE thắng |
|---|---|---|---|
| SPY | 6.0% | 7.2% | regime (0.00444 vs 0.00453) |
| NVDA | 6.4% | 7.2% | regime (0.01351 vs 0.01278) |
| GLD | 4.0% | 6.4% | ewma (0.01143 vs 0.01017) |

> Ghi chú lịch sử: bảng đầu tiên (trước khi xóa `garch_sigma`) so với
> garch-full — GLD cải thiện viol95 8.8 → 6.4, MAE thắng 2/3 assets.
> Quyết định sau đó xóa `garch_sigma` standalone (xem §6.1), harness giờ
> so với baselines naive.

Kết luận trung thực:

- **GLD (bản garch-full cũ)**: regime cải thiện rõ (viol95 8.8 → 6.4,
  gần mục tiêu 5%) — ủng hộ.
- **SPY/NVDA**: MAE tốt hơn nhưng viol95 cao hơn mục tiêu — trung tính.
- Với 250 ngày, sai số ±3–4pp → khoảng cách nằm trong nhiễu cho phần lớn
  chỉ số → kết quả là **hòa/nhỉnh hơn, chưa đủ kết luận "thắng"** cũng
  không "thua".

**Quyết định theo ADR-0006 tiêu chí:** chưa đủ bằng chứng để tuyên bố
GARCH-per-regime vượt trội → giữ các baseline naive làm thước đo đối
chứng; GARCH-per-regime là phương án nghiên cứu tiếp tục đo (thêm asset,
thêm ngày test) — không phải negative result dứt khoát, cũng không phải
chiến thắng được công nhận. Regime layer (HMM) độc lập với kết luận này
(ADR-0012 D2 fallback chưa kích hoạt).

---

## 6.1. Xóa `garch_sigma` standalone (quyết định sau benchmark)

Sau khi hybrid regime-GARCH là ứng viên chính, `garch_sigma` (GARCH toàn
chuỗi) bị XÓA khỏi code (function + exports + các test tham chiếu) vì:

- Paper benchmark trung tâm là **quantum per regime** (ADR-0008), không
  phải GARCH-vs-GARCH;
- Hybrid là model chính của volatility layer — không giữ "GARCH lẻ" kề bên;
- Bằng chứng benchmark đã được ghi lại trong §6, không mất đi khi xóa code;
- Baselines naive (constant/rolling/ewma) giữ làm thước đo so sánh trong
  evaluation suite.

Hệ quả: `modeling/__init__.py` không còn expose `garch_sigma`;
`tests/evaluation/test_volatility_benchmark.py` và
`test_regime_garch_benchmark.py` dùng baselines naive + garch-regime.
Kết quả đo (GLD cải thiện viol95, MAE thắng 2/3) là tín hiệu nghiên cứu
được giữ trong ADR — không phải kết luận sản phẩm.