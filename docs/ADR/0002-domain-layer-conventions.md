# ADR-0002: Domain Layer Conventions

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/domain/` — công cụ mô hình hóa, quy ước bất biến,
định danh tài sản, tổ chức module
**Liên quan:** ADR-0001, RULES-006/007, SCHEMA.md §5–§7, §18,
ARCHITECTURE.md §3.3, §6.1

---

## 1. Bối cảnh

WP-1 bắt đầu xây domain layer — tầng định nghĩa các khái niệm tài chính
dùng chung toàn hệ thống. Domain phải độc lập với FastAPI, Taipy, Qiskit,
database (ARCHITECTURE §3.3), và là nền cho data pipeline (ADR-0001).

## 2. Quyết định

### D1 — Pydantic v2 làm công cụ mô hình hóa domain

Domain entities là `pydantic.BaseModel`, không phải dataclass thuần.

Lý do:
- Validation tài chính (giá ≥ 0, OHLC consistency, timezone-aware) là nơi
  Financial Correctness sinh ra; pydantic cho phép khai báo tập trung,
  kiểm thử được.
- pydantic đã có trong runtime dependencies (qua pydantic-settings) —
  không thêm dependency mới.
- Rule 3.3 cấm FastAPI/Taipy/Qiskit/DB trong domain; pydantic là thư viện
  validation dữ liệu, không phải framework nào trong số đó.

### D2 — Frozen (bất biến) toàn bộ domain entities

Mọi entity dùng `ConfigDict(frozen=True)`.

Lý do: observation lịch sử là sự thật đã xảy ra; mutation ngầm là kẻ thù
của reproducibility (priority #4). "Thay đổi" = tạo instance mới
(`model_copy`). Hệ thống chảy một chiều Data → Modeling → Scenario →
Risk nên kiến trúc bất biến khớp tự nhiên.

### D3 — Decimal cho tiền tệ, float chỉ ở lớp tính toán

```text
DOMAIN   (Decimal): giá, amount, volume, portfolio value, P&L, VaR/CVaR
   │  explicit conversion — một hàm duy nhất, có test riêng
   ▼
COMPUTE  (float): returns, volatility, covariance, Monte Carlo, GARCH
```

Lý do: loại bỏ sai số làm tròn nhị phân ở mọi biên tiền tệ; khớp SCHEMA.md
(khai báo Decimal). Provider trả float → adapter parse sang Decimal ngay
tại boundary theo quy ước rõ ràng. Khối lượng (volume) cũng là Decimal
vì là quantity đo đếm được, không phải kết quả tính toán liên tục.

### D4 — AssetId là string ổn định do Sigma quản lý

```python
type AssetId = str  # quy ước: "<asset_type>-<symbol>-<market>", vd equity-aapl-us
```

- `Asset` giữ cả `asset_id` (định danh vĩnh viễn) và `symbol` (ticker
  provider-specific). Mapping nằm trong universe config.
- Không dùng UUID (khó đọc, cần registry trung tâm) hay ticker trực tiếp
  (vi phạm SCHEMA §6).

### D5 — Tổ chức module theo trách nhiệm, không theo class

```text
domain/
├── __init__.py   # re-export public API
├── errors.py     # DomainValidationError base (rule phi-khởi-tạo, sinh dần theo nhu cầu)
└── market.py     # AssetId, AssetType, Asset, MarketObservation,
                  # CorporateAction (nhóm "Dataset & Market Data" của SCHEMA §7)
```

Validation lúc khởi tạo entity hiển thị thống nhất dưới dạng
`pydantic.ValidationError` (pydantic wrap mọi exception từ validator).
Custom error classes chỉ thêm vào khi xuất hiện rule domain ngoài khởi tạo
(YAGNI).

`portfolio.py`, `risk.py`, `scenario.py` để trống cho WP sau. Tách file
chỉ khi một module phình thực sự (>~300 dòng).

## 3. Phạm vi WP-1

In: AssetId, AssetType, Asset, MarketObservation, CorporateAction,
validation errors + tests (~15-20 cases).
Out: Portfolio/Position/Scenario/RiskEstimate, loader/pandas/parquet,
Dataset chi tiết đầy đủ (thêm field khi loader thật cần — YAGNI).

## 4. Hệ quả

- Mọi module phía sau import domain qua `sigma.domain` (public API ổn định).
- Loader (WP-2) có đích chuẩn hóa: provider payload → MarketObservation
  frozen với Decimal — ADR-0001 thành hiện thực.
- Validation gate (WORKFLOW §4.2) có contract để validate against.
- Nếu sau này cần domain thuần stdlib sẽ phải refactor pydantic ra khỏi
  domain — rủi ro được chấp nhận có chủ đích.
