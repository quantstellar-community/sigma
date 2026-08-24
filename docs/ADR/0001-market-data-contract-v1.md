# ADR-0001: Market Data Contract V1

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Data layer của Sigma — provider strategy, price semantics,
return convention, calendar/missing-data policy, snapshot format
**Liên quan:** RULES-006/007/071/077, SCHEMA.md §7, §18, TECH_STACK.md §20

---

## 1. Bối cảnh

Sigma đang bước vào giai đoạn xây dựng data layer — thành phần đầu tiên
của Risk Engine. Cần chốt các quyết định nền móng trước khi viết code:
dùng nguồn dữ liệu nào, schema nội bộ định nghĩa "giá" và "return" thế nào,
và dữ liệu thô được lưu ra sao để bảo đảm reproducibility.

Tại thời điểm quyết định, repo chưa có implementation nào; toàn bộ
`src/sigma/data/` là placeholder.

## 2. Các yếu tố thúc đẩy quyết định

- **Reproducibility là priority cao hơn convenience** trong thang ưu tiên
  của Sigma (RULES.md). Risk Engine không được phụ thuộc vào việc gọi API
  lúc runtime.
- **Financial Correctness đứng đầu**: return convention và adjusted-price
  semantics sai thì toàn bộ GARCH/Monte Carlo/VaR phía sau sai theo.
- **RULE-071**: cấm abstraction quá sớm (Factory/Manager/Adapter trên giấy).
- **RULE-077**: secrets chỉ nằm trong `.env`.
- Free tier của Alpha Vantage giới hạn ~25 requests/day.

## 3. Các phương án đã cân nhắc

### Provider

| Phương án | Kết luận |
|---|---|
| Một nguồn duy nhất (yfinance hoặc AV) | Bị loại — vendor lock, mất khả năng đối chiếu |
| Alpha Vantage primary + yfinance dev/fallback | **Chọn** |
| Nasdaq Data Link | Hoãn — là data marketplace, mỗi dataset có contract riêng; phù hợp mở rộng sau |
| Kaggle dataset | Chỉ dùng làm benchmark/reference, không bao giờ là market truth |

### Price semantics

| Phương án | Kết luận |
|---|---|
| Raw OHLC + `adjusted_close` tách riêng + corporate actions | **Chọn** — không mất thông tin, audit được |
| Fully-adjusted OHLC duy nhất | Bị loại — mất giá thị trường thật và lịch sử corporate actions |

### Return convention

| Phương án | Kết luận |
|---|---|
| Simple = canonical, Log = derived explicit | **Chọn** |
| Log = canonical toàn hệ thống | Bị loại — weighted-sum portfolio return chỉ chính xác trong không gian simple |
| Chỉ chọn một và dùng mọi nơi | Bị loại — mỗi layer có requirement toán học khác nhau |

## 4. Quyết định

### D1 — Provider strategy: đa nguồn, chuẩn hóa về một contract

> **Cập nhật 2026-08-24 (ADR-0004):** đánh giá thực nghiệm cho thấy free tier
> của Alpha Vantage/FMP không cung cấp adjusted close — yfinance trở thành
> provider giá duy nhất của V1. Bảng vai trò dưới đây được thay thế bởi
> bảng trong TECH_STACK.md §20.

```text
Alpha Vantage (free tier) → primary reference source
yfinance                  → development / fallback / bootstrap
FRED                      → future: macro/risk factors
```

Provider chỉ được gọi ở giai đoạn download. Risk Engine chạy trên local
snapshot, không gọi API lúc runtime. API key nằm trong `.env`.

### D2 — Canonical price semantics

Schema nội bộ lưu raw OHLC + `adjusted_close` riêng + `CorporateAction`
(dividend/split) tách biệt. Return luôn tính từ `adjusted_close`, không
tính từ giá thô. Lý do: adjusted close loại bỏ biến động nhân tạo do
split/dividend (ví dụ AAPL split 4:1/2020 tạo "lỗ giả" −74% nếu tính từ
giá raw), trong khi raw price giữ nguyên sự thật thị trường để audit.

### D3 — Return convention theo tầng

```text
Simple return (canonical): portfolio aggregation, historical simulation,
                           P&L/loss, VaR/CVaR
Log return (derived):      GARCH, HMM/regime, temporal aggregation
Conversion:                r_log = ln(1 + R_simple), luôn explicit
```

Lý do log return cho model lớp dưới là time-additivity khi mô phỏng
multi-step, không phải "làm mượt dữ liệu".

### D4 — Calendar & missing-data policy

- NYSE trading calendar, exchange tz `America/New_York`, timestamps lưu UTC timezone-aware.
- Cấm forward-fill giá trước khi tính return (ffill tạo return giả = 0).
- Ngày holiday xử lý bằng calendar alignment; missing bất thường và delisted assets phải được flag, không impute âm thầm.

### D5 — Snapshot format

Parquet + metadata sidecar: provider, symbol, frequency, price field,
retrieved_at, date range, row count, checksum, schema version.

### D6 — Không thiết kế provider abstraction trước

Không tạo `MarketDataProvider` ABC trước khi có code. Trình tự: viết
YFinance loader thật → viết loader thứ hai → mới extract interface chung
từ hai implementation thật (tuân thủ RULE-071). Canonical schema — chứ
không phải interface — là tài sản kiến trúc cho phép thay provider.

### D7 — Scope V1

- Universe research: 8–12 assets đa dạng sector (equities, ETF, gold, treasury).
- VaR V1: horizon 1 ngày, `Loss = −V₀·(wᵀR)` chính xác tuyệt đối;
  multi-horizon hoãn đến khi chốt rebalancing assumption (weights drift).

## 5. Hệ quả

**Thuận:**
- Đổi provider không đổi Risk Engine — modeling layer không biết data từ đâu ra.
- Kết quả reproducible: mọi analysis gắn với snapshot version + checksum.
- Tránh class lỗi nghiêm trọng: fake returns do ffill, split-induced losses, mixed conventions.

**Trái / rủi ro chấp nhận:**
- Alpha Vantage free tier 25 req/day → chỉ refresh định kỳ; dev hàng ngày dựa vào yfinance snapshot.
- yfinance là công cụ research/educational theo terms của Yahoo → không đóng vai trò production data contract.
- Lưu cả raw + adjusted làm snapshot nặng hơn — chấp nhận để không phải tải lại khi research mở rộng.

## 6. Điều kiện xem xét lại

- Khi cần multi-horizon VaR → mở ADR mới cho rebalancing assumption.
- Khi đưa FRED/macro factors vào core → mở ADR mới cho regime/stress extension.
- Khi chi phí/nhu cầu vượt free tier → đánh giá lại Alpha Vantage premium hoặc Nasdaq Data Link.
