# Sigma — Mô hình Dữ liệu

**Phiên bản:** 0.3  
**Trạng thái:** Draft / Internal Baseline  
**Phạm vi:** Logical Domain & Data Schema  
**Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

`SCHEMA.md` định nghĩa **logical data model** của Sigma: các thực thể chính, thuộc tính cốt lõi, mối quan hệ và các data contract dùng xuyên suốt hệ thống.

Tài liệu trả lời:

- Sigma hiểu những đối tượng tài chính nào?
- Portfolio, Market Data, Return Data và Scenario khác nhau thế nào?
- Risk Estimate cần mang context gì?
- Classical và Quantum Benchmark liên kết với cùng financial quantity ra sao?
- Dataset provenance được lưu ở đâu?
- Invariant nào phải được giữ giữa các module?

`SCHEMA.md` **không phải database schema**.

Nó không quyết định PostgreSQL, SQLite, ORM, table/index hay storage engine. Logical schema là source of truth cho **ý nghĩa dữ liệu**; physical implementation có thể thay đổi theo deployment.

---

# 2. Nguyên tắc Schema

## 2.1. Financial Meaning First

Mỗi object phải có financial meaning rõ ràng.

Không tạo entity chỉ vì implementation cần một class.

## 2.2. Source Data ≠ Derived Data

Sigma phải phân biệt:

```text
Source / Observed Data
        ↓
Derived Data
        ↓
Model Output
        ↓
Scenario
        ↓
Risk Result
        ↓
Benchmark Result
```

Ví dụ:

- Historical Price → observed/source data
- Return → derived data
- Volatility / Regime → model output
- Scenario → simulated/derived data
- VaR / CVaR → risk result
- Classical–Quantum comparison → benchmark result

## 2.3. Portfolio ≠ Market Data

Portfolio biểu diễn **exposure**.

Market Data biểu diễn **market observation**.

Hai khái niệm phải độc lập.

## 2.4. Scenario ≠ Historical Observation

Historical return là observed data.

Scenario là outcome được sinh ra hoặc xác định trong một risk analysis context.

## 2.5. Risk Estimate phải mang Context

Một giá trị như:

```text
VaR = 42,000
```

không đủ ý nghĩa nếu thiếu portfolio, horizon, confidence level, dataset, methodology và analysis context.

`RiskEstimate` phải truy nguyên được về analysis tạo ra nó.

## 2.6. Benchmark phải Comparable

Classical và Quantum result phải liên kết với **cùng financial quantity và cùng benchmark context**.

Không so sánh hai estimate được tạo từ hai problem khác nhau.

---

# 3. Conceptual Model

```text
Dataset
   └── Market Observation
          └── Return Observation

Portfolio
   └── Position

Risk Analysis
   ├── Portfolio
   ├── Dataset
   ├── Model Specification
   ├── Scenario Set
   │      └── Scenario
   │             └── Loss Distribution
   ├── Risk Estimate
   ├── Risk Contribution
   └── Benchmark Run
          ├── Classical Result
          └── Quantum Result
                 └── Resource Metrics
```

Đây là **logical relationship**, không phải physical database relationship.

---

# 4. Core Entity Map

Sigma V1 có các nhóm entity:

```text
Portfolio
├── Portfolio
└── Position

Market Data
├── Dataset
├── MarketObservation
└── ReturnObservation

Modeling
├── ModelSpecification
├── VolatilityState
├── MarketRegime
└── DistributionSpecification

Scenario
├── ScenarioSet
└── Scenario

Risk
├── RiskAnalysis
├── LossDistribution
├── RiskEstimate
└── RiskContribution

Quantum / Evaluation
├── BenchmarkRun
├── EstimationResult
├── ResourceMetrics
└── BenchmarkConclusion
```

Không phải entity nào cũng phải trở thành database table hoặc Python class độc lập.

---

# 5. Portfolio & Position

## 5.1. Portfolio

`Portfolio` biểu diễn một danh mục được phân tích.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `portfolio_id` | Identifier | ID duy nhất |
| `name` | String | Tên danh mục |
| `base_currency` | Currency | Đồng tiền cơ sở |
| `portfolio_value` | Decimal | Giá trị danh mục |
| `positions` | Collection | Các vị thế |
| `created_at` | Timestamp | Thời điểm tạo |
| `updated_at` | Timestamp | Thời điểm cập nhật |

**Invariant**

- `portfolio_id` phải duy nhất trong context.
- `portfolio_value` không âm.
- `base_currency` phải được xác định.
- Portfolio phải có ít nhất một position khi chạy risk analysis.

## 5.2. Position

`Position` biểu diễn exposure của portfolio đối với một asset.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `position_id` | Identifier | ID position |
| `portfolio_id` | Identifier | Portfolio sở hữu position |
| `asset_id` | Identifier | Asset |
| `quantity` | Decimal | Số lượng |
| `weight` | Decimal | Tỷ trọng |
| `market_value` | Decimal | Market value |
| `currency` | Currency | Currency của position |

**Invariant**

- Mỗi position thuộc đúng một portfolio.
- `asset_id` phải xác định được asset.
- `weight` phải hợp lệ theo portfolio policy.
- Tổng weight phải được kiểm tra trước analysis.
- Không tự động normalize weight mà không ghi nhận.

---

# 6. Asset Identity

Sigma V1 cần identity ổn định cho asset.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `asset_id` | Identifier | Identity nội bộ |
| `symbol` | String | Ticker / symbol |
| `name` | String | Tên asset nếu có |
| `asset_type` | Enum | Loại asset |
| `currency` | Currency | Currency |

`asset_id` không nên phụ thuộc tuyệt đối vào ticker nếu data provider có thể thay đổi symbol.

Ticker là market identifier; `asset_id` là logical identity.

---

# 7. Dataset & Market Data

## 7.1. Dataset

`Dataset` mô tả tập dữ liệu Sigma sử dụng và phải có provenance để hỗ trợ reproducibility.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `dataset_id` | Identifier | Dataset identity |
| `name` | String | Tên dataset |
| `source` | String | Nguồn dữ liệu |
| `version` | String | Version |
| `frequency` | Enum | Daily, weekly... |
| `start_date` | Date | Ngày bắt đầu |
| `end_date` | Date | Ngày kết thúc |
| `assets` | Collection | Assets |
| `price_field` | Enum/String | Price field sử dụng |
| `adjustment_method` | String | Adjustment policy |
| `timezone` | Timezone | Timezone |
| `license` | String | License / usage |
| `downloaded_at` | Timestamp | Thời điểm thu thập |
| `checksum` | String | Integrity identifier |

Dataset phải trả lời được:

> Dataset nào đã tạo ra kết quả này?

và:

> Nếu kết quả thay đổi, data version nào đã thay đổi?

## 7.2. MarketObservation

`MarketObservation` là quan sát thị trường tại một timestamp.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `asset_id` | Identifier | Asset |
| `timestamp` | Timestamp | Thời điểm |
| `open` | Decimal | Open |
| `high` | Decimal | High |
| `low` | Decimal | Low |
| `close` | Decimal | Close |
| `adjusted_close` | Decimal | Adjusted close nếu có |
| `volume` | Decimal | Volume nếu có |
| `dataset_id` | Identifier | Dataset source |

Semantic của price fields phải rõ ràng:

- `close` là giá giao dịch thô (raw) tại thời điểm quan sát;
- `adjusted_close` là giá đã điều chỉnh split/dividend.

Return luôn được tính từ `adjusted_close`, không tính từ `close` thô.

Provider không nhất thiết cung cấp toàn bộ field. Schema phải phân biệt:

```text
Required
Optional
Unavailable
```

Không tự tạo dữ liệu thiếu.

## 7.3. ReturnObservation

Return là **derived data**.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `asset_id` | Identifier | Asset |
| `timestamp` | Timestamp | Thời điểm |
| `value` | Decimal | Return |
| `method` | Enum | Simple / Log |
| `source_observation` | Reference | Market observations |
| `dataset_id` | Identifier | Dataset |

Concept:

```text
Price_t
   ↓
Price_(t-1)
   ↓
Return_t
```

Return convention phải explicit và nhất quán giữa các module.

## 7.4. CorporateAction

Sự kiện doanh nghiệp ảnh hưởng chuỗi giá phải được lưu tách biệt, không impute ngầm.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `asset_id` | Identifier | Asset |
| `timestamp` | Timestamp | Ngày hiệu lực (ex-date) |
| `action_type` | Enum | Dividend / Split |
| `amount` | Decimal | Số tiền cổ tức hoặc hệ số split |
| `dataset_id` | Identifier | Dataset source |

## 7.5. Calendar & Missing Data Policy

Quy ước bắt buộc cho market data:

```text
Trading calendar : NYSE (exchange calendar)
Exchange timezone: America/New_York
Stored timestamps: timezone-aware UTC
```

Chính sách dữ liệu thiếu:

- Cấm forward-fill giá trước khi tính return — ffill tạo return giả bằng 0 và làm nhiễu volatility model.
- Ngày thiếu do lịch giao dịch được xử lý bằng calendar alignment, không phải impute.
- Missing observation bất thường phải được validation flag, không được impute âm thầm.
- Asset bị delisted hoặc chuỗi bị cắt cụt phải được flag rõ ràng.

---

# 8. Modeling

## 8.1. ModelSpecification

`ModelSpecification` mô tả cách một risk analysis mô hình hóa dữ liệu.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `model_id` | Identifier | Model identity |
| `name` | String | Tên model |
| `version` | String | Model version |
| `return_model` | String | Return modeling |
| `volatility_model` | String | Volatility model |
| `regime_model` | String | Regime model |
| `distribution_model` | String | Distribution |
| `parameters` | Mapping | Model parameters |
| `assumptions` | Collection | Assumptions |

Ví dụ conceptual:

```text
Return Model:
Historical / Parametric

Volatility:
GARCH

Regime:
HMM

Distribution:
Student-t / Regime-conditioned
```

Schema không hard-code một model duy nhất.

## 8.2. VolatilityState

`VolatilityState` là derived/model state.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `asset_id` | Identifier | Asset |
| `timestamp` | Timestamp | Thời điểm |
| `value` | Decimal | Estimated volatility |
| `model_id` | Identifier | Model sử dụng |

Volatility phải gắn với methodology/model context.

## 8.3. MarketRegime

`MarketRegime` biểu diễn trạng thái thị trường do model xác định.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `regime_id` | Identifier | Regime |
| `timestamp` | Timestamp | Thời điểm |
| `label` | String/Enum | Regime label |
| `probability` | Decimal | Probability nếu có |
| `model_id` | Identifier | Regime model |

Ví dụ:

```text
Low Volatility
High Volatility
Stress
Normal
```

Label thực tế phải do methodology định nghĩa.

## 8.4. DistributionSpecification

`DistributionSpecification` mô tả distribution dùng để sinh scenario.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `distribution_id` | Identifier | Identity |
| `model_id` | Identifier | Model source |
| `family` | String | Distribution family |
| `parameters` | Mapping | Parameters |
| `regime_condition` | Reference | Regime context |
| `fit_window` | TimeRange | Fit window |

Distribution là **model artifact**, không phải scenario.

---

# 9. Scenario

## 9.1. ScenarioSet

`ScenarioSet` là tập scenario được tạo trong một analysis.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `scenario_set_id` | Identifier | Identity |
| `analysis_id` | Identifier | Risk analysis |
| `method` | String | Generation method |
| `count` | Integer | Số scenario |
| `seed` | Integer/String | Random seed nếu có |
| `distribution_id` | Identifier | Distribution source |
| `created_at` | Timestamp | Creation time |

**Invariant**

- `count` phải khớp số scenario thực tế hoặc có thể truy vết.
- Nếu stochastic simulation cần reproducibility, seed phải được ghi nhận.
- Scenario set phải gắn với analysis context.

## 9.2. Scenario

`Scenario` biểu diễn một market/portfolio outcome.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `scenario_id` | Identifier | Scenario identity |
| `scenario_set_id` | Identifier | Scenario set |
| `regime_id` | Identifier | Regime nếu có |
| `asset_returns` | Mapping | Return theo asset |
| `portfolio_return` | Decimal | Portfolio return |
| `portfolio_pnl` | Decimal | Portfolio P&L |
| `portfolio_loss` | Decimal | Portfolio loss |
| `scenario_type` | Enum | Simulated / Stress / Historical |

Phân biệt:

```text
Historical Scenario
→ Dựa trên observed event

Simulated Scenario
→ Do model sinh

Stress Scenario
→ Được thiết kế để kiểm tra adverse condition
```

Không trộn ba loại mà không lưu `scenario_type`.

---

# 10. Loss Distribution & Risk

## 10.1. LossDistribution

`LossDistribution` biểu diễn tập hợp hoặc representation của portfolio losses.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `loss_distribution_id` | Identifier | Identity |
| `analysis_id` | Identifier | Analysis |
| `scenario_set_id` | Identifier | Scenario source |
| `loss_values` | Collection/Reference | Loss observations |
| `sample_count` | Integer | Số mẫu |
| `loss_convention` | String | Quy ước loss |
| `currency` | Currency | Currency |
| `summary_statistics` | Mapping | Statistics |

Sigma phải định nghĩa rõ loss convention, ví dụ:

```text
Loss > 0
```

hoặc representation:

```text
P&L < 0
```

Các module không được tự chọn convention khác nhau.

## 10.2. RiskAnalysis

`RiskAnalysis` là execution context của một lần phân tích và là entity trung tâm kết nối:

```text
Portfolio
Dataset
Model
Scenario Set
Risk Results
```

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `analysis_id` | Identifier | Analysis identity |
| `portfolio_id` | Identifier | Portfolio |
| `dataset_id` | Identifier | Dataset |
| `model_id` | Identifier | Model specification |
| `risk_horizon` | Duration | Horizon |
| `confidence_levels` | Collection | Confidence levels |
| `scenario_count` | Integer | Scenario count |
| `scenario_set_id` | Identifier | Scenario set |
| `status` | Enum | Pending / Running / Completed / Failed |
| `created_at` | Timestamp | Start |
| `completed_at` | Timestamp | Completion |
| `configuration` | Mapping | Analysis configuration |

Lifecycle:

```text
Created
   ↓
Running
   ↓
Completed
```

hoặc:

```text
Running
   ↓
Failed
```

## 10.3. RiskEstimate

`RiskEstimate` biểu diễn một estimated risk quantity.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `risk_estimate_id` | Identifier | Identity |
| `analysis_id` | Identifier | Analysis |
| `metric` | Enum | VaR / CVaR / Expected Loss / ... |
| `confidence_level` | Decimal | Confidence |
| `horizon` | Duration | Risk horizon |
| `value` | Decimal | Estimated value |
| `currency` | Currency | Currency |
| `method` | String | Estimation method |
| `error_estimate` | Decimal | Error nếu có |
| `created_at` | Timestamp | Timestamp |

Ví dụ:

```text
metric:
    CVaR

confidence_level:
    0.99

horizon:
    1D

method:
    Classical Monte Carlo

value:
    ...
```

Một `RiskEstimate` không tồn tại mà không có analysis context.

## 10.4. RiskContribution

`RiskContribution` mô tả đóng góp của asset vào portfolio risk.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `analysis_id` | Identifier | Analysis |
| `asset_id` | Identifier | Asset |
| `metric` | String | Risk metric |
| `contribution_value` | Decimal | Contribution |
| `contribution_ratio` | Decimal | Relative contribution |

Phải ghi rõ contribution thuộc metric nào.

```text
CVaR contribution
≠
Volatility contribution
```

---

# 11. Classical–Quantum Benchmark

Benchmark là **first-class evaluation object**.

## 11.1. BenchmarkRun

`BenchmarkRun` mô tả một lần benchmark.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `benchmark_id` | Identifier | Identity |
| `analysis_id` | Identifier | Financial context |
| `target_quantity` | String | Quantity được ước lượng |
| `classical_method` | String | Classical estimator |
| `quantum_method` | String | Quantum estimator |
| `backend` | String | Quantum backend |
| `noise_model` | String | Noise configuration |
| `configuration` | Mapping | Benchmark settings |
| `created_at` | Timestamp | Timestamp |

Benchmark phải tham chiếu tới financial analysis, không tồn tại như quantum experiment tách khỏi financial context.

## 11.2. EstimationResult

`EstimationResult` là kết quả của một estimator.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `estimator_type` | Enum | Classical / Quantum |
| `estimate` | Decimal | Estimate |
| `absolute_error` | Decimal | Absolute error |
| `relative_error` | Decimal | Relative error |
| `runtime` | Duration | Runtime |
| `sample_or_query_count` | Integer | Samples / queries |

Một benchmark có thể có:

```text
Classical Result
+
Quantum Result
```

nhưng cả hai phải estimate cùng `target_quantity`.

## 11.3. ResourceMetrics

Dùng cho quantum/resource-aware evaluation.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `qubit_count` | Integer | Qubit count |
| `circuit_depth` | Integer | Circuit depth |
| `gate_count` | Integer | Gate count nếu có |
| `shots` | Integer | Shots |
| `oracle_queries` | Integer | Oracle/query count |
| `state_preparation_cost` | Numeric/Metadata | State preparation |
| `oracle_cost` | Numeric/Metadata | Oracle cost |
| `noise_model` | String | Noise context |

Không phải field nào cũng bắt buộc trong mọi experiment.

## 11.4. BenchmarkConclusion

`BenchmarkConclusion` là interpretation của benchmark evidence.

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `benchmark_id` | Identifier | Benchmark |
| `summary` | String | Kết luận |
| `evidence` | Collection | Metrics hỗ trợ |
| `advantage_status` | Enum | Observed / Not Observed / Inconclusive |
| `scope` | String | Điều kiện áp dụng |

Không lưu:

```text
Quantum Advantage = True
```

chỉ vì Quantum có theoretical speedup.

Kết luận phải phản ánh benchmark evidence.

Ví dụ:

```text
Theoretical query advantage observed,
but no end-to-end runtime advantage under
the evaluated simulator configuration.
```

---

# 12. Data Provenance

Kết quả quan trọng phải truy nguyên được.

### Risk result

```text
Risk Result
    ↓
Analysis
    ↓
Dataset
    ↓
Market Observations
```

và:

```text
Risk Result
    ↓
Analysis
    ↓
Model Specification
    ↓
Scenario Set
```

### Quantum benchmark

```text
Benchmark
    ↓
Analysis
    ↓
Target Quantity
    ↓
Quantum Configuration
    ↓
Resource Metrics
```

---

# 13. Analysis Context

`RiskAnalysis` là context chính nối các object:

```text
Portfolio
Dataset
Model
     ↓
RiskAnalysis
     ↓
ScenarioSet
     ↓
LossDistribution
     ↓
RiskEstimate
```

Một analysis phải đủ context để trả lời:

> Kết quả này được tạo ra bằng dữ liệu nào, portfolio nào, model nào và scenario nào?

---

# 14. Entity Relationships

Logical relationships:

```text
Portfolio
  1 ──── N Position

Dataset
  1 ──── N MarketObservation

Dataset
  1 ──── N ReturnObservation

RiskAnalysis
  N ──── 1 Portfolio

RiskAnalysis
  N ──── 1 Dataset

RiskAnalysis
  N ──── 1 ModelSpecification

RiskAnalysis
  1 ──── 1..N ScenarioSet

ScenarioSet
  1 ──── N Scenario

ScenarioSet
  1 ──── 1 LossDistribution

RiskAnalysis
  1 ──── N RiskEstimate

RiskAnalysis
  1 ──── N RiskContribution

RiskAnalysis
  1 ──── N BenchmarkRun

BenchmarkRun
  1 ──── N EstimationResult
```

Cardinality có thể thay đổi theo implementation, nhưng logical ownership phải được giữ.

---

# 15. Scenario và Quantum Boundary

Pipeline:

```text
Market Data
    ↓
Model
    ↓
Distribution
    ↓
Scenario / Loss Distribution
    ↓
Financial Quantity
    ↓
Quantum Estimator
```

Quantum không mặc định nhận trực tiếp:

```text
MarketObservation[]
```

làm input chính cho estimation.

Quantum nhận representation của financial quantity đã được formulation.

Ranh giới:

```text
Financial Modeling
        ≠
Quantum Estimation
```

---

# 16. Classical–Quantum Comparable Schema

Benchmark nên có cấu trúc:

```text
BenchmarkRun
│
├── Target Quantity
│
├── Financial Context
│   ├── Portfolio
│   ├── Dataset
│   ├── Model
│   └── Scenario Set
│
├── Classical Result
│   ├── Estimate
│   ├── Error
│   ├── Samples
│   └── Runtime
│
└── Quantum Result
    ├── Estimate
    ├── Error
    ├── Queries
    ├── Runtime
    └── Resource Metrics
```

Mục tiêu là giữ comparison trong cùng financial context.

---

# 17. Required, Optional, Derived & Metadata

## Required

Dữ liệu cần để computation có ý nghĩa.

Ví dụ:

```text
portfolio_id
asset_id
timestamp
return
risk_horizon
confidence_level
```

## Optional

Dữ liệu hữu ích nhưng không phải analysis nào cũng cần:

```text
volume
high
low
noise_model
gate_count
```

## Derived

Dữ liệu Sigma tính ra:

```text
return
volatility
regime
scenario
portfolio_loss
VaR
CVaR
```

## Metadata

Dùng cho reproducibility:

```text
source
version
checksum
seed
model_version
```

---

# 18. Units & Conventions

Sigma phải explicit về:

**Currency**

Mọi monetary value phải có currency.

**Return**

Simple return là **canonical representation** cho portfolio aggregation,
historical simulation, P&L/loss và VaR/CVaR.

Log return là **derived representation** (`r = ln(1 + R)`), dùng cho các
model cần temporal aggregation (GARCH, HMM/regime). Mọi conversion giữa
hai representation phải explicit và được ghi nhận.

**Loss**

Loss convention: `Loss > 0` nghĩa là tổn thất. Nếu representation nội bộ
dùng `P&L < 0`, conversion sang loss phải explicit.

**Time**

Timestamp phải có timezone hoặc convention rõ ràng.

**Probability**

Confidence level phải dùng một representation thống nhất, ví dụ:

```text
0.95
0.99
```

Không trộn `95`, `99`, `0.95`, `0.99` giữa các module.

---

# 19. Schema Validation

### Portfolio

```text
weights valid
portfolio value valid
assets valid
```

### Market Data

```text
timestamp valid
asset identity valid
no unexpected duplicates
```

### Returns

```text
method explicit
ordering correct
```

### Scenario

```text
scenario_set reference valid
asset return dimensions consistent
```

### Risk

```text
analysis reference valid
confidence level valid
horizon valid
metric explicit
```

### Benchmark

```text
target quantity identical
financial context identical
method explicit
resource metadata consistent
```

---

# 20. Versioning

Các artifact quan trọng nên có version:

```text
dataset_version
model_version
analysis_configuration_version
benchmark_configuration_version
```

Không cần version mọi object máy móc.

Versioning tập trung vào những thứ có thể làm thay đổi scientific result.

---

# 21. Reproducibility Contract

Một risk analysis có khả năng tái lập ở mức phù hợp khi có:

```text
Portfolio
+
Dataset Version
+
Model Specification
+
Risk Configuration
+
Scenario Configuration
+
Random Seed (if applicable)
```

Quantum benchmark có thêm:

```text
Quantum Method
+
Backend
+
Noise Model
+
Shots
+
Circuit / Resource Configuration
```

---

# 22. Demo và Research Data

Sigma có thể có:

```text
Demo Dataset
```

và:

```text
Research Dataset
```

nhưng cả hai phải tuân theo cùng logical schema.

```text
Demo Dataset
     ↓
Same Data Contract
     ↓
Same Risk Engine
```

Không tạo schema riêng chỉ cho demo.

---

# 23. Schema Boundary

`SCHEMA.md` định nghĩa:

```text
Meaning
Structure
Relationships
Invariants
Provenance
Units
Contracts
```

Nó không định nghĩa:

```text
PostgreSQL tables
SQLite tables
ORM models
Indexes
Partitions
Redis
Parquet implementation details
```

Physical representation thuộc implementation/architecture level.

---

# 24. Future Extensibility

Schema phải có khả năng mở rộng sang các risk domain khác.

Hiện tại:

```text
Market Risk
    ↓
Portfolio Risk
```

Tương lai có thể mở rộng:

```text
RiskAnalysis
├── Market Risk
├── Portfolio Risk
├── Credit Risk
├── Liquidity Risk
└── Other Risk Domains
```

Không hard-code schema theo một metric duy nhất như VaR.

---

# 25. Schema Success Criteria

Schema V1 đạt yêu cầu khi:

- mọi core financial concept có representation rõ;
- Portfolio và Market Data được tách biệt;
- source và derived data được phân biệt;
- Scenario và historical observation được phân biệt;
- Risk result luôn có analysis context;
- Classical và Quantum benchmark có cùng target quantity;
- provenance đủ để hỗ trợ reproducibility;
- units/conventions nhất quán;
- schema không phụ thuộc trực tiếp vào UI framework;
- schema không khóa Sigma vào một database implementation.

---

# 26. Schema North Star

```text
Data
 │
 ├── Dataset
 │      └── Market Observation
 │
 ├── Portfolio
 │      └── Position
 │
 └── Configuration
          │
          ▼
      Risk Analysis
          │
    ┌─────┼──────┐
    ▼     ▼      ▼
 Modeling Scenario Benchmark
    │       │       │
    │       ▼       ├── Classical
    │     Loss      └── Quantum
    │       │
    └───────┴───────┐
                    ▼
               Risk Estimate
                    │
                    ▼
              Risk Intelligence
```

---

# 27. Final Schema Principle

> **Schema của Sigma phải mô tả thế giới tài chính và computational evidence mà Sigma hiểu, không mô tả database mà Sigma đang dùng.**

Mục tiêu:

```text
Clear Financial Semantics
        +
Explicit Data Contracts
        +
Traceable Provenance
        +
Reproducible Analysis
        +
Comparable Classical / Quantum Results
        ↓
Reliable Sigma Risk Intelligence Data Model
```
