# Sigma

## Hybrid Quantum-Classical Risk Intelligence

Sigma là một dự án nghiên cứu và engineering nhằm xây dựng **Financial
Risk Intelligence Engine** kết hợp Classical Computing, Statistical
Modeling và Quantum Computing.

Mục tiêu của Sigma không phải xây Quantum vì Quantum, mà là xây dựng một
hệ thống risk intelligence có khả năng:

``` text
Financial Data
    ↓
Financial Modeling
    ↓
Scenario Generation
    ↓
Portfolio Loss Distribution
    ↓
VaR / CVaR / Stress / Risk Analytics
    ↓
Classical–Quantum Benchmark
    ↓
Risk Intelligence
    ↓
Decision Support
```

> **Triết lý:** Classical First → Quantum Where Justified → Fair
> Benchmark → Measure Real Value.

> **Trạng thái:** Early-stage development. Sigma đang ở giai đoạn xây
> dựng foundation, architecture và research workflow; production
> implementation sẽ được phát triển từng bước.

------------------------------------------------------------------------

## 1. Vision

Tài chính là bài toán ra quyết định dưới uncertainty.

Sigma tập trung vào việc giúp người dùng hiểu:

-   portfolio đang chịu rủi ro gì;
-   những scenario nào có thể tạo ra tổn thất lớn;
-   tail risk lớn đến đâu;
-   yếu tố nào đang đóng góp nhiều nhất vào risk;
-   các phương pháp Classical và Quantum khác nhau như thế nào về
    accuracy, resource và practical utility.

Sigma hướng tới một hệ thống **modular, auditable và benchmarkable**,
trong đó Quantum là một computational enhancement layer thay vì product
identity.

------------------------------------------------------------------------

## 2. Core Principles

### Classical First

Mọi Quantum approach phải có Classical baseline tương ứng.

### Quantum Where Justified

Quantum chỉ được đưa vào khi có financial problem và computational
contribution rõ ràng.

### Fair Benchmark

Classical và Quantum phải được đánh giá trên cùng financial quantity,
context và experimental conditions phù hợp.

### No Unsupported Quantum Advantage

Không tuyên bố quantum speedup hoặc quantum advantage chỉ dựa trên
theoretical complexity hoặc circuit-level result.

### End-to-End Measurement

Benchmark phải xem xét khi phù hợp:

``` text
Accuracy
Runtime
Sampling / Query Cost
State Preparation
Oracle Cost
Qubits
Circuit Depth
Shots
Noise
Scalability
```

### Reproducibility

Risk result và research result phải có đủ context để truy nguyên tới:

``` text
Dataset
Model
Configuration
Code Version
Experiment
```

### Product Utility

Một phương pháp chỉ có giá trị product khi nó tạo ra utility thực tế,
không chỉ tạo ra một technical demonstration.

------------------------------------------------------------------------

## 3. V1 --- Regime-Aware Portfolio Risk Intelligence

Scope chính của Sigma V1 là:

> **REGIME-AWARE PORTFOLIO RISK INTELLIGENCE ENGINE**

Workflow:

``` text
Market Data
    ↓
Data Validation
    ↓
Returns / Features
    ↓
Volatility & Regime Modeling
    ↓
Regime-Aware Distribution
    ↓
Scenario Generation
    ↓
Portfolio Loss Distribution
    ↓
┌───────────────────────┐
│                       │
▼                       ▼
Classical Risk      Quantum Risk
│                       │
└───────────┬───────────┘
            ▼
Classical–Quantum Benchmark
            ↓
VaR / CVaR / Stress / Risk Intelligence
            ↓
API
            ↓
Taipy / Client
```

### V1 Inputs

-   historical market prices / returns;
-   asset identifiers và timestamps;
-   portfolio positions hoặc weights;
-   valuation date;
-   risk horizon;
-   confidence level;
-   scenario configuration;
-   model configuration.

### V1 Outputs

-   portfolio loss distribution;
-   VaR;
-   CVaR / Expected Shortfall;
-   expected loss;
-   stress-test results;
-   risk contribution;
-   scenario analysis;
-   model/configuration metadata;
-   Classical--Quantum benchmark results khi áp dụng.

------------------------------------------------------------------------

## 4. Architecture

``` mermaid
flowchart LR
    A[Market Data + Portfolio] --> B[Data Validation]
    B --> C[Financial Modeling]
    C --> D[Regime-Aware Distribution]
    D --> E[Scenario Generation]
    E --> F[Classical Risk Engine]
    E --> G[Quantum Risk Module]
    F --> H[Risk Intelligence]
    G --> H
    H --> I[FastAPI]
    I --> J[Taipy / Client]
```

### Core boundaries

``` text
Taipy
  ↓
FastAPI
  ↓
Application
  ↓
Sigma Core
  ├── Data
  ├── Modeling
  ├── Scenarios
  ├── Risk
  └── Quantum
```

UI không chứa financial business logic.

API là integration boundary.

Classical Risk Engine không phụ thuộc Quantum.

Quantum layer không định nghĩa financial semantics.

------------------------------------------------------------------------

## 5. Risk Workflow

Sigma chuyển financial data thành risk intelligence theo:

``` text
Market Data
    ↓
Validated Data
    ↓
Returns
    ↓
Volatility
    ↓
Market Regime
    ↓
Distribution
    ↓
Scenarios
    ↓
Portfolio P&L / Loss
    ↓
Loss Distribution
    ↓
Risk Estimation
```

Các risk quantities trọng tâm:

``` text
VaR
CVaR / Expected Shortfall
Expected Loss
Stress Loss
Risk Contribution
```

Loss convention và risk context phải được định nghĩa rõ trong từng
analysis.

------------------------------------------------------------------------

## 6. Classical Risk Engine

Classical Risk Engine là **baseline bắt buộc** và là computational
foundation của V1.

Nó chịu trách nhiệm:

-   scenario processing;
-   portfolio P&L / loss;
-   Monte Carlo;
-   loss distribution;
-   VaR;
-   CVaR;
-   stress testing;
-   risk contribution.

Classical engine phải có thể chạy độc lập:

``` text
Quantum unavailable
        ↓
Classical Risk Analysis
        ↓
Still Functional
```

------------------------------------------------------------------------

## 7. Quantum Research Layer

Quantum là computational enhancement layer.

Các hướng nghiên cứu ưu tiên:

``` text
Quantum Monte Carlo
        +
Quantum Amplitude Estimation
```

Potential workflow:

``` text
Financial Quantity
    ↓
Quantum Formulation
    ↓
State Preparation
    ↓
Oracle
    ↓
Amplitude Estimation
    ↓
Risk Estimate
```

Quantum không nhận raw financial data rồi tự thực hiện toàn bộ financial
modeling.

Ví dụ target quantity có thể là một xác suất/tail quantity như:

``` text
P(Loss > Threshold)
```

hoặc một expectation được formulation rõ ràng.

### Quantum architecture cần phân biệt

#### Pure Classical

``` text
Data
→ Classical Modeling
→ Classical Scenarios
→ Classical Risk
```

#### Naive Hybrid

``` text
Data
→ Classical Modeling
→ Classical Scenarios
→ Quantum State Preparation
→ QAE
→ Risk Estimate
```

#### Quantum / Co-designed Architecture

``` text
Data
→ Classical Parameter Estimation
→ Quantum Distribution / Scenario Representation
→ Quantum Estimation
→ Risk Estimate
```

Không architecture nào được mặc định là tốt nhất.

------------------------------------------------------------------------

## 8. Classical--Quantum Benchmark

Benchmark phải so sánh **cùng financial problem**:

``` text
Same Portfolio
Same Dataset
Same Risk Quantity
Same Horizon
Same Confidence Level
Same Relevant Model Context
```

Các metrics có thể gồm:

``` text
Accuracy
Absolute / Relative Error
Runtime
Sample / Query Complexity
Qubits
Circuit Depth
Shots
Oracle Cost
State Preparation Cost
Noise
Scalability
```

Một benchmark hợp lệ có thể kết luận:

``` text
Quantum Advantage
```

nhưng cũng có thể kết luận:

``` text
Quantum No Advantage
```

hoặc:

``` text
Inconclusive
```

Negative result là kết quả nghiên cứu hợp lệ.

------------------------------------------------------------------------

## 9. Research Workflow

Mọi research contribution quan trọng nên đi theo:

``` text
Problem
    ↓
Hypothesis
    ↓
Mathematical Formulation
    ↓
Classical Baseline
    ↓
Quantum Method
    ↓
Fair Benchmark
    ↓
Resource / Ablation Analysis
    ↓
Scientific Conclusion
    ↓
Product Evaluation
```

Không bắt đầu bằng:

``` text
“Có Quantum algorithm nào để dùng?”
```

mà bắt đầu bằng:

``` text
“Financial bottleneck nào đáng giải quyết,
và Quantum có thể đóng góp gì?”
```

------------------------------------------------------------------------

## 10. Technology Direction

Sigma V1 sử dụng Python làm computational ecosystem chính.

Core stack:

``` text
Python 3.12
uv
FastAPI
Taipy
NumPy
pandas
SciPy
statsmodels / scikit-learn khi phù hợp
Qiskit
Qiskit Aer
pytest
Ruff
Pyright
Git
```

Technology không phải product identity.

Việc bổ sung infrastructure hoặc dependency mới phải có requirement thực
tế.

------------------------------------------------------------------------

## 11. Documentation

Các tài liệu nền tảng của Sigma gồm:

``` text
PRD.md
DESIGN.md
ARCHITECTURE.md
SCHEMA.md
RULES.md
TECH_STACK.md
TEAM.md
ROLES.md
WORKFLOW.md
CONTRIBUTING.md
```

Mỗi document có một responsibility riêng:

``` text
PRD
→ Product requirements

DESIGN
→ User experience

ARCHITECTURE
→ System structure

SCHEMA
→ Data & domain semantics

RULES
→ Engineering / research constraints

TECH_STACK
→ Technology decisions

TEAM
→ Team ownership

ROLES
→ Role responsibilities

WORKFLOW
→ System & research workflows

CONTRIBUTING
→ Contribution process
```

------------------------------------------------------------------------

## 12. Repository

Sigma được phát triển theo hướng modular monolith trong V1.

Một structure khái quát:

``` text
sigma/
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
├── src/
│   └── sigma/
│       ├── data/
│       ├── modeling/
│       ├── scenarios/
│       ├── risk/
│       ├── quantum/
│       ├── application/
│       └── api/
├── tests/
├── research/
└── examples/
```

Structure có thể tiến hóa theo implementation thực tế nhưng các
architectural boundaries phải được giữ ổn định.

------------------------------------------------------------------------

## 13. Roadmap

### Phase 0 --- Foundation

-   hoàn thiện project structure;
-   Python/uv environment;
-   documentation;
-   schemas và conventions;
-   testing foundation.

### Phase 1 --- Classical Risk Core

-   market-data ingestion;
-   validation;
-   returns;
-   volatility/regime modeling;
-   distribution;
-   scenario generation;
-   Monte Carlo;
-   VaR/CVaR;
-   stress testing.

### Phase 2 --- API & UI

-   FastAPI;
-   application layer;
-   risk API;
-   Taipy reference client;
-   analytical visualization.

### Phase 3 --- Quantum Benchmark

-   financial quantity formulation;
-   quantum state preparation;
-   oracle;
-   QAE/QMC experiment;
-   Classical baseline;
-   fair benchmark;
-   resource analysis.

### Phase 4 --- Advanced Research

-   advanced distributions;
-   uncertainty modeling;
-   learned distributions;
-   advanced portfolio risk;
-   selected optimization problems;
-   further quantum methods.

### Phase 5 --- Productization

-   robust data connectors;
-   persistence;
-   authentication/authorization;
-   observability;
-   auditability;
-   deployment;
-   model governance.

------------------------------------------------------------------------

## 14. What Sigma Is

Sigma là:

-   Financial Risk Intelligence Engine;
-   hybrid Classical--Quantum research platform;
-   risk-first architecture;
-   scenario and tail-risk analysis system;
-   benchmarkable research environment;
-   API-first foundation cho decision support.

## What Sigma Is Not

Sigma hiện không phải:

-   autonomous trading system;
-   stock-price prediction product;
-   production banking platform;
-   replacement cho institutional risk systems;
-   proof of quantum advantage;
-   autonomous investment advisor.

------------------------------------------------------------------------

## 15. Responsible Use

Sigma là một project nghiên cứu và engineering.

Risk outputs phải được hiểu trong context của:

``` text
Data
Model
Assumptions
Scenario
Confidence Level
Method
Limitations
```

Các kết quả của Sigma không phải financial advice và không bảo đảm
investment performance.

Production use trong môi trường tài chính thực tế sẽ cần:

-   independent validation;
-   data governance;
-   security;
-   model governance;
-   domain expertise;
-   regulatory/compliance review.



> **Sigma không xây Quantum để chứng minh Quantum. Sigma xây Financial
> Risk Intelligence và sử dụng Quantum ở những nơi Quantum thực sự tạo
> ra giá trị có thể đo lường.**
