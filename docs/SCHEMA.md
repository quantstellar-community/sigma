# Sigma --- Schema Document

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Logical Domain & Data Schema\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`SCHEMA.md` định nghĩa **logical data model** của Sigma: các thực thể
chính, thuộc tính cốt lõi, mối quan hệ giữa chúng và các data contract
quan trọng xuyên suốt hệ thống.

Tài liệu này trả lời:

-   Sigma hiểu những đối tượng tài chính nào?
-   Portfolio được biểu diễn thế nào?
-   Market Data và Return Data khác nhau ra sao?
-   Scenario và Loss Distribution được biểu diễn thế nào?
-   Risk Estimate chứa những thông tin gì?
-   Quantum Benchmark Result liên kết với financial quantity như thế
    nào?
-   Dataset provenance được lưu ở mức nào?
-   Những invariant nào phải được giữ giữa các module?

`SCHEMA.md` **không phải database schema**. Nó không quyết định
PostgreSQL, SQLite, ORM, table/index implementation hay storage engine.

Logical schema là source of truth cho **ý nghĩa dữ liệu**;
implementation schema có thể thay đổi theo deployment.

------------------------------------------------------------------------

# 2. Schema Principles

## 2.1. Financial Meaning First

Mỗi object phải có financial meaning rõ ràng.

Không tạo entity chỉ vì implementation cần một class.

------------------------------------------------------------------------

## 2.2. Source Data ≠ Derived Data

Sigma phải phân biệt:

``` text
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

-   Historical Price là observed/source data.
-   Return là derived data.
-   Volatility/Regime là model output.
-   Scenario là simulated/derived data.
-   VaR/CVaR là risk result.
-   Classical--Quantum comparison là benchmark result.

------------------------------------------------------------------------

## 2.3. Portfolio ≠ Market Data

Portfolio mô tả **ý định/exposure của người dùng**.

Market Data mô tả **quan sát thị trường**.

Hai khái niệm phải độc lập.

------------------------------------------------------------------------

## 2.4. Scenario ≠ Historical Observation

Một historical return không phải scenario.

Scenario là một outcome được sinh ra hoặc xác định trong một risk
analysis context.

------------------------------------------------------------------------

## 2.5. Risk Estimate Must Carry Context

Một con số như:

``` text
VaR = 42,000
```

không đủ ý nghĩa nếu thiếu:

-   portfolio;
-   horizon;
-   confidence level;
-   dataset;
-   methodology/model;
-   analysis context.

Vì vậy `RiskEstimate` phải mang đủ context để có thể diễn giải và tái
lập ở mức phù hợp.

------------------------------------------------------------------------

## 2.6. Benchmark Must Be Comparable

Classical và Quantum result phải liên kết với **cùng một financial
quantity và benchmark context**.

Không so sánh hai estimate được tạo từ hai problem khác nhau.

------------------------------------------------------------------------

# 3. Conceptual Model

Logical model của Sigma:

``` mermaid
flowchart TD
    DATASET["Dataset"]
    MARKET["Market Observation"]
    PORTFOLIO["Portfolio"]
    POSITION["Position"]
    ANALYSIS["Risk Analysis"]
    MODEL["Model Specification"]
    SCENARIO["Scenario"]
    LOSS["Portfolio Loss Distribution"]
    RISK["Risk Estimate"]
    BENCH["Benchmark"]
    CLASSICAL["Classical Result"]
    QUANTUM["Quantum Result"]

    DATASET --> MARKET

    PORTFOLIO --> POSITION
    ANALYSIS --> PORTFOLIO
    ANALYSIS --> DATASET
    ANALYSIS --> MODEL

    ANALYSIS --> SCENARIO
    SCENARIO --> LOSS
    LOSS --> RISK

    BENCH --> ANALYSIS
    BENCH --> CLASSICAL
    BENCH --> QUANTUM

    CLASSICAL --> BENCH
    QUANTUM --> BENCH
```

Đây là logical relationship, không phải physical database relationship.

------------------------------------------------------------------------

# 4. Core Entity Map

Sigma V1 có các nhóm entity chính:

``` text
Portfolio Domain
├── Portfolio
└── Position

Market Data Domain
├── Dataset
├── MarketObservation
└── ReturnObservation

Modeling Domain
├── ModelSpecification
├── VolatilityState
├── MarketRegime
└── DistributionSpecification

Scenario Domain
├── ScenarioSet
└── Scenario

Risk Domain
├── LossDistribution
├── RiskAnalysis
├── RiskEstimate
└── RiskContribution

Quantum / Evaluation Domain
├── BenchmarkRun
├── EstimationResult
├── ResourceMetrics
└── BenchmarkConclusion
```

Không phải mọi entity nhất thiết phải trở thành database table hoặc
Python class độc lập.

------------------------------------------------------------------------

# 5. Portfolio Schema

## 5.1. Portfolio

`Portfolio` biểu diễn một danh mục được phân tích.

### Core fields

  Field               Kiểu logic   Ý nghĩa
  ------------------- ------------ --------------------
  `portfolio_id`      Identifier   ID duy nhất
  `name`              String       Tên danh mục
  `base_currency`     Currency     Đồng tiền cơ sở
  `portfolio_value`   Decimal      Giá trị danh mục
  `positions`         Collection   Các vị thế
  `created_at`        Timestamp    Thời điểm tạo
  `updated_at`        Timestamp    Thời điểm cập nhật

### Invariants

-   `portfolio_id` phải duy nhất trong context.
-   `portfolio_value` phải không âm.
-   `base_currency` phải được xác định.
-   Portfolio phải có ít nhất một position khi chạy risk analysis.

------------------------------------------------------------------------

# 6. Position Schema

`Position` biểu diễn exposure của portfolio đối với một asset.

### Core fields

  Field            Kiểu logic   Ý nghĩa
  ---------------- ------------ ---------------------------
  `position_id`    Identifier   ID position
  `portfolio_id`   Identifier   Portfolio sở hữu position
  `asset_id`       Identifier   Asset
  `quantity`       Decimal      Số lượng
  `weight`         Decimal      Tỷ trọng
  `market_value`   Decimal      Market value
  `currency`       Currency     Currency của position

### Invariants

-   Mỗi position thuộc đúng một portfolio.
-   `asset_id` phải xác định được asset.
-   `weight` phải nằm trong miền hợp lệ theo portfolio policy.
-   Tổng weights phải được kiểm tra trước khi analysis.
-   Không tự động normalize weight mà không ghi nhận hành vi đó.

------------------------------------------------------------------------

# 7. Asset Identity

Sigma V1 cần một identity ổn định cho asset.

Logical representation:

  Field          Kiểu logic   Ý nghĩa
  -------------- ------------ ------------------
  `asset_id`     Identifier   Identity nội bộ
  `symbol`       String       Ticker/symbol
  `name`         String       Tên asset nếu có
  `asset_type`   Enum         Loại asset
  `currency`     Currency     Currency

`asset_id` không nên phụ thuộc tuyệt đối vào ticker nếu data provider có
khả năng thay đổi symbol.

Ticker là market identifier; `asset_id` là logical identity.

------------------------------------------------------------------------

# 8. Dataset Schema

`Dataset` mô tả một tập dữ liệu được Sigma sử dụng.

Dataset phải có provenance để hỗ trợ reproducibility.

### Core fields

  Field                 Kiểu logic    Ý nghĩa
  --------------------- ------------- -----------------------------
  `dataset_id`          Identifier    Dataset identity
  `name`                String        Tên dataset
  `source`              String        Nguồn dữ liệu
  `version`             String        Version
  `frequency`           Enum          Daily, weekly...
  `start_date`          Date          Ngày bắt đầu
  `end_date`            Date          Ngày kết thúc
  `assets`              Collection    Assets
  `price_field`         Enum/String   Price field được sử dụng
  `adjustment_method`   String        Adjustment policy
  `timezone`            Timezone      Timezone
  `license`             String        License / usage information
  `downloaded_at`       Timestamp     Thời điểm thu thập
  `checksum`            String        Integrity identifier

### Provenance

Sigma cần có khả năng trả lời:

> Dataset nào đã tạo ra kết quả này?

và:

> Nếu kết quả thay đổi, data version nào đã thay đổi?

------------------------------------------------------------------------

# 9. MarketObservation Schema

`MarketObservation` là một quan sát thị trường tại một timestamp.

### Core fields

  Field              Kiểu logic   Ý nghĩa
  ------------------ ------------ -------------------------------------
  `asset_id`         Identifier   Asset
  `timestamp`        Timestamp    Thời điểm
  `open`             Decimal      Open
  `high`             Decimal      High
  `low`              Decimal      Low
  `close`            Decimal      Close
  `adjusted_close`   Decimal      Adjusted close nếu dataset cung cấp
  `volume`           Decimal      Volume nếu có
  `dataset_id`       Identifier   Dataset source

Không phải mọi provider đều cung cấp toàn bộ field. Schema phải phân
biệt:

``` text
Required
Optional
Unavailable
```

thay vì tự tạo dữ liệu thiếu.

------------------------------------------------------------------------

# 10. ReturnObservation Schema

Return là derived data.

### Core fields

  Field                  Kiểu logic   Ý nghĩa
  ---------------------- ------------ ---------------------
  `asset_id`             Identifier   Asset
  `timestamp`            Timestamp    Thời điểm return
  `value`                Decimal      Return
  `method`               Enum         Simple / Log
  `source_observation`   Reference    Market observations
  `dataset_id`           Identifier   Dataset

Ví dụ:

``` text
Price_t
   ↓
Price_{t-1}
   ↓
Return_t
```

Schema phải ghi rõ return convention.

Không được để một module sử dụng log return trong khi module khác ngầm
hiểu simple return.

------------------------------------------------------------------------

# 11. Modeling Schema

## 11.1. ModelSpecification

`ModelSpecification` mô tả cách một risk analysis mô hình hóa dữ liệu.

### Fields

  Field                  Kiểu logic   Ý nghĩa
  ---------------------- ------------ ------------------
  `model_id`             Identifier   Model identity
  `name`                 String       Tên model
  `version`              String       Model version
  `return_model`         String       Return modeling
  `volatility_model`     String       Volatility model
  `regime_model`         String       Regime model
  `distribution_model`   String       Distribution
  `parameters`           Mapping      Model parameters
  `assumptions`          Collection   Assumptions

Ví dụ conceptual:

``` text
Return Model:
Historical / Parametric

Volatility:
GARCH

Regime:
HMM

Distribution:
Student-t / Regime-conditioned
```

Không hard-code một model duy nhất vào schema.

------------------------------------------------------------------------

# 12. VolatilityState

`VolatilityState` là derived/model state dùng trong risk modeling.

### Fields

  Field         Kiểu logic   Ý nghĩa
  ------------- ------------ ----------------------
  `asset_id`    Identifier   Asset
  `timestamp`   Timestamp    Thời điểm
  `value`       Decimal      Estimated volatility
  `model_id`    Identifier   Model sử dụng

Volatility phải luôn gắn với methodology/model context.

------------------------------------------------------------------------

# 13. MarketRegime

`MarketRegime` biểu diễn trạng thái thị trường được model xác định.

### Fields

  Field           Kiểu logic    Ý nghĩa
  --------------- ------------- ---------------------------
  `regime_id`     Identifier    Regime
  `timestamp`     Timestamp     Thời điểm
  `label`         String/Enum   Regime label
  `probability`   Decimal       Regime probability nếu có
  `model_id`      Identifier    Regime model

Ví dụ label:

``` text
Low Volatility
High Volatility
Stress
Normal
```

Các label thực tế phải do methodology định nghĩa, không mặc định cứng
trong schema.

------------------------------------------------------------------------

# 14. DistributionSpecification

`DistributionSpecification` mô tả distribution được dùng để sinh
scenario.

### Fields

  Field                Kiểu logic   Ý nghĩa
  -------------------- ------------ ---------------------
  `distribution_id`    Identifier   Identity
  `model_id`           Identifier   Model source
  `family`             String       Distribution family
  `parameters`         Mapping      Parameters
  `regime_condition`   Reference    Regime context
  `fit_window`         TimeRange    Training/fit window

Ví dụ:

``` text
Student-t
+
Regime-conditioned parameters
```

Distribution là model artifact, không phải scenario.

------------------------------------------------------------------------

# 15. ScenarioSet Schema

`ScenarioSet` là collection các scenario được tạo trong một analysis.

### Fields

  Field               Kiểu logic       Ý nghĩa
  ------------------- ---------------- ----------------------------
  `scenario_set_id`   Identifier       Identity
  `analysis_id`       Identifier       Risk analysis
  `method`            String           Scenario generation method
  `count`             Integer          Số scenario
  `seed`              Integer/String   Random seed nếu có
  `distribution_id`   Identifier       Distribution source
  `created_at`        Timestamp        Creation time

### Invariants

-   `count` phải bằng số scenario thực tế hoặc có thể truy vết.
-   Nếu stochastic simulation dùng seed, seed phải được ghi nhận khi
    reproducibility yêu cầu.
-   Scenario set phải gắn với một analysis context.

------------------------------------------------------------------------

# 16. Scenario Schema

`Scenario` biểu diễn một market/portfolio outcome.

### Fields

  Field                Kiểu logic   Ý nghĩa
  -------------------- ------------ ---------------------------------
  `scenario_id`        Identifier   Scenario identity
  `scenario_set_id`    Identifier   Scenario set
  `regime_id`          Identifier   Market regime nếu có
  `asset_returns`      Mapping      Return theo asset
  `portfolio_return`   Decimal      Portfolio return
  `portfolio_pnl`      Decimal      Portfolio P&L
  `portfolio_loss`     Decimal      Portfolio loss
  `scenario_type`      Enum         Simulated / Stress / Historical

### Distinction

``` text
Historical Scenario
→ dựa trên observed event

Simulated Scenario
→ do model sinh

Stress Scenario
→ được thiết kế để kiểm tra adverse condition
```

Không trộn ba loại này mà không lưu `scenario_type`.

------------------------------------------------------------------------

# 17. LossDistribution Schema

`LossDistribution` biểu diễn tập hợp hoặc representation của portfolio
losses.

### Fields

  Field                    Kiểu logic             Ý nghĩa
  ------------------------ ---------------------- -------------------
  `loss_distribution_id`   Identifier             Identity
  `analysis_id`            Identifier             Analysis
  `scenario_set_id`        Identifier             Scenario source
  `loss_values`            Collection/Reference   Loss observations
  `sample_count`           Integer                Số mẫu
  `loss_convention`        String                 Quy ước loss
  `currency`               Currency               Currency
  `summary_statistics`     Mapping                Statistics

### Loss convention

Sigma phải định nghĩa rõ:

``` text
Loss > 0
```

là tổn thất hay:

``` text
P&L < 0
```

là tổn thất.

Không để các module tự chọn convention.

------------------------------------------------------------------------

# 18. RiskAnalysis Schema

`RiskAnalysis` là một execution context cho một lần phân tích.

Đây là entity trung tâm kết nối:

``` text
Portfolio
Dataset
Model
Scenario Set
Risk Results
```

### Fields

  Field                 Kiểu logic   Ý nghĩa
  --------------------- ------------ ----------------------------------------
  `analysis_id`         Identifier   Analysis identity
  `portfolio_id`        Identifier   Portfolio
  `dataset_id`          Identifier   Dataset
  `model_id`            Identifier   Model specification
  `risk_horizon`        Duration     Horizon
  `confidence_levels`   Collection   Confidence levels
  `scenario_count`      Integer      Scenario count
  `scenario_set_id`     Identifier   Scenario set
  `status`              Enum         Pending / Running / Completed / Failed
  `created_at`          Timestamp    Start
  `completed_at`        Timestamp    Completion
  `configuration`       Mapping      Analysis configuration

### Analysis lifecycle

``` text
Created
   ↓
Running
   ↓
Completed
```

hoặc:

``` text
Running
   ↓
Failed
```

------------------------------------------------------------------------

# 19. RiskEstimate Schema

`RiskEstimate` biểu diễn một estimated risk quantity.

### Fields

  Field                Kiểu logic   Ý nghĩa
  -------------------- ------------ ----------------------------------
  `risk_estimate_id`   Identifier   Identity
  `analysis_id`        Identifier   Analysis
  `metric`             Enum         VaR / CVaR / Expected Loss / ...
  `confidence_level`   Decimal      Confidence
  `horizon`            Duration     Risk horizon
  `value`              Decimal      Estimated value
  `currency`           Currency     Currency
  `method`             String       Estimation method
  `error_estimate`     Decimal      Error nếu available
  `created_at`         Timestamp    Timestamp

Ví dụ:

``` text
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

Một `RiskEstimate` không được tồn tại mà không có analysis context.

------------------------------------------------------------------------

# 20. RiskContribution Schema

`RiskContribution` mô tả đóng góp của asset vào portfolio risk.

### Fields

  Field                  Kiểu logic   Ý nghĩa
  ---------------------- ------------ -----------------------
  `analysis_id`          Identifier   Analysis
  `asset_id`             Identifier   Asset
  `metric`               String       Risk metric
  `contribution_value`   Decimal      Contribution
  `contribution_ratio`   Decimal      Relative contribution

Contribution phải ghi rõ đang đóng góp vào metric nào.

Ví dụ:

``` text
CVaR contribution
≠
Volatility contribution
```

Không được dùng chung semantics.

------------------------------------------------------------------------

# 21. Benchmark Schema

Classical--Quantum benchmark là first-class evaluation object.

## 21.1. BenchmarkRun

`BenchmarkRun` mô tả một lần benchmark.

### Fields

  Field                Kiểu logic   Ý nghĩa
  -------------------- ------------ -------------------------
  `benchmark_id`       Identifier   Identity
  `analysis_id`        Identifier   Financial context
  `target_quantity`    String       Quantity được ước lượng
  `classical_method`   String       Classical estimator
  `quantum_method`     String       Quantum estimator
  `backend`            String       Quantum backend
  `noise_model`        String       Noise configuration
  `configuration`      Mapping      Benchmark settings
  `created_at`         Timestamp    Timestamp

Benchmark phải tham chiếu đến financial analysis thay vì tồn tại như một
quantum experiment không có context.

------------------------------------------------------------------------

# 22. EstimationResult

`EstimationResult` là kết quả của một estimator.

### Fields

  Field                     Kiểu logic   Ý nghĩa
  ------------------------- ------------ ---------------------
  `estimator_type`          Enum         Classical / Quantum
  `estimate`                Decimal      Estimate
  `absolute_error`          Decimal      Absolute error
  `relative_error`          Decimal      Relative error
  `runtime`                 Duration     Runtime
  `sample_or_query_count`   Integer      Samples / queries

Một benchmark có thể có:

``` text
Classical Result
+
Quantum Result
```

nhưng hai result phải cùng `target_quantity`.

------------------------------------------------------------------------

# 23. ResourceMetrics

Dùng cho quantum/resource-aware evaluation.

### Fields

  Field                      Kiểu logic         Ý nghĩa
  -------------------------- ------------------ --------------------------
  `qubit_count`              Integer            Qubit count
  `circuit_depth`            Integer            Circuit depth
  `gate_count`               Integer            Gate count nếu available
  `shots`                    Integer            Shots
  `oracle_queries`           Integer            Oracle/query count
  `state_preparation_cost`   Numeric/Metadata   State preparation
  `oracle_cost`              Numeric/Metadata   Oracle cost
  `noise_model`              String             Noise context

Không phải mọi field đều bắt buộc trong mọi experiment.

------------------------------------------------------------------------

# 24. BenchmarkConclusion

`BenchmarkConclusion` là interpretation của benchmark evidence.

### Fields

  Field                Kiểu logic   Ý nghĩa
  -------------------- ------------ ----------------------------------------
  `benchmark_id`       Identifier   Benchmark
  `summary`            String       Kết luận
  `evidence`           Collection   Metrics supporting conclusion
  `advantage_status`   Enum         Observed / Not Observed / Inconclusive
  `scope`              String       Điều kiện áp dụng

### Important rule

Không được lưu:

``` text
Quantum Advantage = True
```

chỉ vì Quantum có theoretical speedup.

Kết luận phải phản ánh benchmark evidence.

Ví dụ hợp lệ:

``` text
Theoretical query advantage observed,
but no end-to-end runtime advantage under
the evaluated simulator configuration.
```

------------------------------------------------------------------------

# 25. Data Provenance

Mọi kết quả quan trọng phải có khả năng truy nguyên:

``` text
Risk Result
    ↓
Analysis
    ↓
Dataset
    ↓
Market Observations
```

và:

``` text
Risk Result
    ↓
Analysis
    ↓
Model Specification
    ↓
Scenario Set
```

và với Quantum:

``` text
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

------------------------------------------------------------------------

# 26. Analysis Context

`RiskAnalysis` là context chính để nối các object:

``` mermaid
flowchart LR
    P["Portfolio"]
    D["Dataset"]
    M["Model"]
    A["RiskAnalysis"]
    S["ScenarioSet"]
    L["LossDistribution"]
    R["RiskEstimate"]
    B["BenchmarkRun"]

    P --> A
    D --> A
    M --> A
    A --> S
    S --> L
    L --> R
    A --> B
```

Một analysis phải đủ context để người khác có thể hiểu:

> "Kết quả này được tạo ra bằng dữ liệu nào, portfolio nào, model nào và
> scenario nào?"

------------------------------------------------------------------------

# 27. Entity Relationships

Logical relationships:

``` text
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

Cardinality có thể thay đổi theo implementation, nhưng logical ownership
phải giữ được.

------------------------------------------------------------------------

# 28. ER Diagram

``` mermaid
erDiagram
    PORTFOLIO ||--|{ POSITION : contains
    DATASET ||--|{ MARKET_OBSERVATION : provides
    DATASET ||--o{ RETURN_OBSERVATION : derives

    PORTFOLIO ||--o{ RISK_ANALYSIS : analyzed_by
    DATASET ||--o{ RISK_ANALYSIS : used_by
    MODEL_SPECIFICATION ||--o{ RISK_ANALYSIS : configured_by

    RISK_ANALYSIS ||--o{ SCENARIO_SET : produces
    SCENARIO_SET ||--|{ SCENARIO : contains
    SCENARIO_SET ||--|| LOSS_DISTRIBUTION : forms

    RISK_ANALYSIS ||--o{ RISK_ESTIMATE : produces
    RISK_ANALYSIS ||--o{ RISK_CONTRIBUTION : produces

    RISK_ANALYSIS ||--o{ BENCHMARK_RUN : evaluates
    BENCHMARK_RUN ||--|{ ESTIMATION_RESULT : contains
```

Đây là **logical ER model**, không phải database migration
specification.

------------------------------------------------------------------------

# 29. Scenario and Quantum Boundary

Một điểm đặc biệt quan trọng:

``` text
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

Quantum không nhận trực tiếp:

``` text
MarketObservation[]
```

làm input chính cho estimation.

Quantum nhận một representation của financial quantity đã được
formulation.

Điều này giúp giữ ranh giới:

``` text
Financial Modeling
        ≠
Quantum Estimation
```

------------------------------------------------------------------------

# 30. Classical--Quantum Comparable Schema

Benchmark phải có cấu trúc:

``` text
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

Điều này bảo đảm comparison không bị tách khỏi financial problem.

------------------------------------------------------------------------

# 31. Required vs Optional Data

Schema của Sigma phải phân biệt:

### Required

Dữ liệu cần để computation có ý nghĩa.

Ví dụ:

``` text
portfolio_id
asset_id
timestamp
return
risk_horizon
confidence_level
```

### Optional

Dữ liệu hữu ích nhưng không phải analysis nào cũng cần.

Ví dụ:

``` text
volume
high
low
noise_model
gate_count
```

### Derived

Dữ liệu Sigma tính ra:

``` text
return
volatility
regime
scenario
portfolio_loss
VaR
CVaR
```

### Metadata

Dùng cho reproducibility:

``` text
source
version
checksum
seed
model_version
```

------------------------------------------------------------------------

# 32. Units and Conventions

Sigma phải explicit về:

## Currency

Mọi monetary value phải có currency.

## Return

Phải chỉ rõ:

``` text
simple return
```

hoặc:

``` text
log return
```

## Loss

Phải có loss convention nhất quán.

## Time

Timestamp phải có timezone hoặc convention rõ ràng.

## Probability

Confidence level được biểu diễn thống nhất, ví dụ:

``` text
0.95
0.99
```

thay vì trộn:

``` text
95
99
0.95
0.99
```

trong các module.

------------------------------------------------------------------------

# 33. Schema Validation

Các validation chính:

### Portfolio

``` text
weights valid
portfolio value valid
assets valid
```

### Market Data

``` text
timestamp valid
asset identity valid
no unexpected duplicates
```

### Returns

``` text
method explicit
ordering correct
```

### Scenario

``` text
scenario_set reference valid
asset return dimensions consistent
```

### Risk

``` text
analysis reference valid
confidence level valid
horizon valid
metric explicit
```

### Benchmark

``` text
target quantity identical
financial context identical
method explicit
resource metadata consistent
```

------------------------------------------------------------------------

# 34. Versioning

Các artifact quan trọng nên có version:

``` text
dataset_version
model_version
analysis_configuration_version
benchmark_configuration_version
```

Không cần version mọi object một cách máy móc.

Versioning tập trung vào những thứ có thể làm thay đổi scientific
result.

------------------------------------------------------------------------

# 35. Reproducibility Contract

Một risk analysis có khả năng tái lập ở mức phù hợp khi có:

``` text
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

Một quantum benchmark có thêm:

``` text
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

------------------------------------------------------------------------

# 36. Demo vs Research Data

Sigma có thể có:

``` text
Demo Dataset
```

và:

``` text
Research Dataset
```

nhưng cả hai phải tuân theo cùng logical schema.

``` text
Demo Dataset
      ↓
Same Data Contract
      ↓
Same Risk Engine
```

Không tạo một schema riêng chỉ cho demo.

------------------------------------------------------------------------

# 37. Schema Boundary

`SCHEMA.md` định nghĩa:

``` text
Meaning
Structure
Relationships
Invariants
Provenance
Units
Contracts
```

Nó không định nghĩa:

``` text
PostgreSQL tables
SQLite tables
ORM models
Indexes
Partitions
Redis
Parquet implementation details
```

Các physical representation có thể được quyết định ở
implementation/architecture level.

------------------------------------------------------------------------

# 38. Future Extensibility

Schema phải có khả năng mở rộng từ Market/Portfolio Risk sang các risk
domain khác.

Hiện tại:

``` text
Market Risk
    ↓
Portfolio Risk
```

Tương lai:

``` text
RiskAnalysis
├── Market Risk
├── Portfolio Risk
├── Credit Risk
├── Liquidity Risk
└── Other Risk Domains
```

Không nên hard-code schema theo một metric duy nhất như VaR.

------------------------------------------------------------------------

# 39. Schema Success Criteria

Schema V1 được xem là đạt yêu cầu khi:

-   mọi core financial concept có representation rõ;
-   Portfolio và Market Data được tách biệt;
-   source và derived data được phân biệt;
-   Scenario và historical observation được phân biệt;
-   Risk result luôn có analysis context;
-   Classical và Quantum benchmark có cùng target quantity;
-   provenance đủ để hỗ trợ reproducibility;
-   units/conventions nhất quán;
-   schema không phụ thuộc trực tiếp vào UI framework;
-   schema không khóa Sigma vào một database implementation.

------------------------------------------------------------------------

# 40. Schema North Star

``` text
                   DATA
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Dataset      Portfolio    Configuration
        │            │
        ▼            ▼
 Market Observation Position
        │            │
        └──────┬─────┘
               ▼
          Risk Analysis
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    Modeling Scenario  Benchmark
       │       │        │
       │       ▼        ├── Classical
       │     Loss       └── Quantum
       │       │
       └───────┴───────┐
                       ▼
                  Risk Estimate
                       │
                       ▼
                 Risk Intelligence
```

------------------------------------------------------------------------

# 41. Final Schema Principle

> **Schema của Sigma phải mô tả thế giới tài chính và computational
> evidence mà Sigma hiểu, không mô tả database mà Sigma đang dùng.**

Mục tiêu:

``` text
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
