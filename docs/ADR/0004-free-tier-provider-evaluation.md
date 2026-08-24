# ADR-0004: Đánh giá thực nghiệm Free-Tier Data Providers — yfinance giữ vai trò duy nhất cho giá V1

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Lựa chọn market-data provider cho `src/sigma/data/` (WP-2c)
**Liên quan:** ADR-0001 (provider strategy), SCHEMA.md §7.2,
TECH_STACK.md §20, RULES-043

---

## 1. Bối cảnh

ADR-0001 chỉ định Alpha Vantage làm *primary reference source* trên free tier
và dự kiến WP-2c viết `AlphaVantageLoader`. Trước khi thiết kế, ta kiểm chứng
bằng thực nghiệm khả năng đáp ứng của các free tier đối với **canonical data
contract**: mọi return phải tính từ `adjusted_close` đã điều chỉnh
split/dividend (SCHEMA.md §7.2).

## 2. Phương pháp

Đo trực tiếp API bằng key thật, không dựa vào tài liệu hay review:

```text
FMP  : 8 request thực (probe script, không in key)
AV   : đối chiếu tài liệu chính thức + nhiều nguồn độc lập 2026
EODHD: theo báo cáo cộng đồng (chưa đo key thật)
```

## 3. Kết quả đo được

### Financial Modeling Prep — free "Basic" (250 req/day)

| Thử nghiệm | Kết quả |
|---|---|
| `/stable/historical-price-eod/full?symbol=AAPL` | ✅ 1,253 rows |
| History depth | ❌ **đúng 5 năm** (2021-08-25 → 2026-08-21) |
| Field `adjClose` | ❌ **không có** — chỉ OHLCV + vwap |
| Endpoint adjusted (`histor-price-eod-adjusted*`) | ❌ HTTP 404 (nhiều biến thể) |
| Legacy `/api/v3/historical-price-full` | ❌ HTTP 403 (ngừng hỗ trợ từ 2025-08) |

### Alpha Vantage — free tier

| Hạng mục | Kết quả |
|---|---|
| `TIME_SERIES_DAILY_ADJUSTED` | ❌ premium ($49.99/mo trở lên) |
| `TIME_SERIES_DAILY` | ✅ nhưng **không có adjusted close**, và bị giới hạn `outputsize=compact` (~100 điểm/request) |

### EODHD — free tier (theo báo cáo, chưa đo)

20 requests/ngày, ticker bị giới hạn vài mã demo → không đủ điều kiện thử
nghiệm nghiêm túc.

## 4. Quyết định

### D1 — Không viết loader giá cho bất kỳ free tier nào ngoài yfinance

Không có free tier nào trong số các ứng viên cung cấp **adjusted daily prices
với đủ chiều sâu lịch sử** mà canonical schema yêu cầu. Viết loader trên raw
giá thô sẽ tạo ra cú lỗ giả khi split (ví dụ NVDA 10:1/2024 → −90% giả),
vi phạm Priority #1: Financial Correctness.

Đây là một **negative result có giá trị**: quyết định dựa trên phép đo trước
khi code, đúng tinh thần RULES-043.

### D2 — yfinance là provider giá duy nhất của Sigma V1

Vai trò nâng cấp từ "dev/fallback" thành **de-facto primary** cho V1, với
điều kiện vận hành không đổi: chỉ chạy ở giai đoạn download, snapshot-first,
không gọi lúc runtime.

### D3 — Vai trò khác của FMP key hiện có

FMP free vẫn hữu ích cho **fundamentals, company profile, corporate-action
calendars** — các endpoint tách biệt với price series. Giữ key trong `.env`,
chưa tích hợp; sẽ mở ADR riêng khi xuất hiện nhu cầu thật (RULE-087).

### D4 — Điều kiện revisit

Mở lại đánh giá provider khi có ít nhất một điều kiện:

- Budget premium sẵn sàng (FMP Premium $59/mo cho 30 năm adjusted, hoặc
  AV premium);
- Cần cross-validation độc lập giữa hai nguồn giá cho data-quality research;
- Cần dữ liệu ngoài phạm vi Yahoo (quốc tế, intraday).

## 5. Hệ quả

- WP-2c (AlphaVantageLoader) **hủy theo hình dạng ban đầu**; công sức chuyển
  sang WP-3 (Returns computation).
- Docs được cập nhật đồng bộ: ADR-0001 (D1) và TECH_STACK.md §20 phản ánh
  trạng thái mới.
- Nếu sau này cần thêm provider giá, điều kiện tiên quyết vẫn là
  adjusted close + đủ history — tiêu chí đã được chứng minh là rào cản thật.
