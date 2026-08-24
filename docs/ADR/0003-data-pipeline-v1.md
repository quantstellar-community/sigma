# ADR-0003: Data Pipeline V1 (Universe → Loader → Snapshot)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/data/` — universe config, YFinance adapter, snapshot
persistence, download entry point
**Liên quan:** ADR-0001, ADR-0002, SCHEMA.md §7, §19,
ARCHITECTURE.md §6.2/§14, WORKFLOW.md §4

---

## 1. Bối cảnh

WP-2 biến Data Contract (ADR-0001) thành code. Đây là work package đầu tiên
có I/O với thế giới ngoài (network API, filesystem), tách thành WP-2a
(pure logic) và WP-2b (I/O).

## 2. Quyết định

### D1 — Universe khai báo trong `configs/universe.yaml`

Universe là cấu hình, không phải logic (ARCHITECTURE §14). Thêm asset =
thêm entry YAML, zero code change. `asset_type: MACRO` có sẵn để nhận
FRED series sau này mà không đổi schema.

```yaml
universe:
  name: research-universe-v1
  frequency: 1d
  calendar: NYSE
  timezone: America/New_York
  period: { start: 2015-01-01 }
assets:
  - { asset_id: equity-aapl-us, symbol: AAPL, asset_type: EQUITY, currency: USD }
```

### D2 — Lưu raw verbatim trước khi chuẩn hóa

`data/raw/yfinance/{symbol}__{retrieved_at}.parquet` giữ payload gốc.
Schema thay đổi sau này → re-process từ raw, không gọi lại API. Raw layer
không validate; phán xét dữ liệu là việc của validation gate.

### D3 — Snapshot: một Parquet/batch, long format + YAML sidecar

```text
data/processed/prices/research-universe-v1__{ts}.parquet
data/processed/prices/research-universe-v1__{ts}.meta.yaml
```

- Long format 1 dòng = 1 `MarketObservation`; giá lưu dạng string để
  round-trip Decimal tuyệt đối chính xác.
- Sidecar ghi đủ provenance SCHEMA §7.1: provider, symbols, frequency,
  price semantics, calendar/timezone, retrieved_at, period, rows,
  `checksum_sha256` (trên bytes parquet).
- Cặp file+sidecar là đơn vị bất biến — mọi analysis tham chiếu về đúng
  bản dữ liệu đã chạy.

### D4 — Entry point: `python -m sigma.data.download`

Đường ống thẳng config → fetch → raw → validation → canonical → snapshot.
Thuộc Data layer (ARCHITECTURE §6.2); không dựng orchestration trong
application layer cho workflow mỏng như vậy. Makefile target `download`.

### D5 — Chỉ `yfinance_loader.py` được import yfinance

Adapter duy nhất biết Yahoo. pandas chỉ sống trong data layer. Test unit
không bao giờ chạm network: monkeypatch fetch function với fixture
deterministic dựng bằng tay (DataFrame MultiIndex mô phỏng output thật của
`yf.download(auto_adjust=False)`).

### D6 — Validation gate (WORKFLOW §4.2, subset thực thi được ngay)

Bắt lỗi (raise `DataValidationError`, dừng pipeline):
duplicate `(asset_id, timestamp)` · timestamps không tăng ngặt theo asset ·
một symbol có 0 observation.

Xử lý im lặng bị cấm: hàng NaN price bị drop nhưng **số lượng phải được
báo cáo** trong kết quả chạy.

## 3. Phạm vi

In: universe parsing, yfinance loader, raw writer, validation gate,
snapshot store, CLI entry point, tests offline.
Out: AlphaVantageLoader (WP-2c — extract provider protocol lúc đó),
returns computation (WP-3), FRED/macro, network test trong gate mặc định.

## 4. Hệ quả

- Reproducibility: mọi analysis trỏ được về đúng snapshot qua
  `{universe}__{timestamp}` + checksum.
- Đổi provider = thêm adapter, không đổi gì phía sau (canonical schema).
- Chi phí disk gấp đôi cho raw — chấp nhận, quy mô hiện tại vài MB.
