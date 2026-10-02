# ADR-0010: Portfolio Regime Semantic — Market State (Direction C)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Định nghĩa semantic của "regime" ở tầng portfolio — nền tảng
cho loss distribution và quantum risk estimation per regime
**Liên quan:** ADR-0007/0008/0009, PRD.md §26, WORKFLOW.md §12

---

## 1. Bối cảnh

WP-4b đã xây HMM regime layer **per-asset** (mỗi asset một regime profile).
Khi tiến tới portfolio loss distribution, xuất hiện câu hỏi semantic:

> Loss per regime — regime của PORTFOLIO là gì, khi mỗi asset có regime riêng?

Ba hướng khả dĩ (đã thảo luận):

- **A — Univariate per-asset kéo dài tới hết:** mỗi asset regime riêng, gộp
  thành portfolio loss. → Regime của portfolio mơ hồ (12 regime khác nhau mỗi
  ngày), "loss per regime" không định nghĩa được.
- **B — Portfolio-level HMM:** HMM trên chuỗi portfolio return (wᵀr). →
  Regime phụ thuộc weights: đổi weights là đổi regime structure; cùng một
  ngày thị trường có regime khác nhau tùy portfolio; không so sánh được
  giữa các portfolio → không phù hợp benchmark khoa học.
- **C — Market state:** HMM trên market factor (SPY hoặc equal-weighted),
  regime = thuộc tính THỊ TRƯỜNG; trong mỗi regime, mỗi asset có
  distribution/GARCH riêng.

## 2. Quyết định

### D1 — Regime = latent MARKET state (hướng C)

> Regime là thuộc tính của thị trường, không phải của portfolio.

```text
Market factor → HMM → Market Regime (Calm / Volatile / Crisis)
     ↓                    ↓
  (chọn factor            trong mỗi market regime:
   bằng benchmark         per-asset GARCH/distribution riêng
   ở WP-5)                → portfolio loss theo regime
```

Lý do:

- **Bất biến với portfolio weights** — đổi danh mục không làm đổi regime
  structure; so sánh được giữa mọi portfolio (benchmark khoa học hợp lệ).
- **Giải thích được**: "hôm đó thị trường ở regime Crisis" — khớp ngôn ngữ
  của Risk Analyst và research question trung tâm (ADR-0008) vốn hỏi
  *"under different market regimes"* — chữ "market" là chìa khóa.
- Khớp literature: market regimes tồn tại độc lập với portfolio.

### D2 — Per-asset layer giữ nguyên trong C

Trong mỗi market regime, mỗi asset vẫn có đặc tính riêng (emission,
GARCH, distribution) — phần dư riêng của từng asset (vd GLD không theo SPY
crisis) được mô hình hóa ở tầng asset, không làm sập tầng regime.

### D3 — Chọn market factor là phép đo, không phải giả định

SPY vs equal-weighted (bình quân 12 asset) — so sánh bằng benchmark
(stability, VaR coverage OOS) tại WP-5 khi triển khai. Không chọn bừa.

### D4 — Không triển khai C ngay trong WP-4b.5

GARCH per regime (WP-4b.5) được thiết kế **decoupled**: nhận mảng nhãn
regime làm input, không biết nhãn từ đâu (per-asset HMM bây giờ, market
factor HMM của C sau này). Việc xây market-factor HMM diễn ra ở WP-5 khi
portfolio loss thật sự cần một regime chung.

## 3. Mở cho tương lai

- **Multivariate HMM** (shared state, per-asset emissions, regime-dependent
  covariance) — khi cần mô hình hóa correlation thay đổi theo regime
  (Crisis: mọi asset rơi cùng nhau → đa dạng hóa kém tác dụng).
- **B vs C so sánh thực nghiệm** — research question riêng nếu muốn; nhưng
  vấn đề semantic của B (regime phụ thuộc weights) không phải vấn đề hiệu
  năng, nên khả năng B được chọn lại là thấp.

## 4. Hệ quả

- Kiến trúc ổn định từ bây giờ: regime = market state; per-asset là tầng
  phụ thuộc trong regime.
- WP-4b.5 (GARCH per regime) thiết kế decoupled — không lệch hướng, không
  phải làm lại khi C triển khai.
- WP-5 triển khai market-factor HMM + benchmark chọn factor.