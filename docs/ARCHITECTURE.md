# Sigma --- Architecture Document

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Sản phẩm:** Sigma Risk Intelligence\
> **Kiến trúc:** Modular Monolith\
> **Interface:** FastAPI\
> **Reference Client:** Taipy

------------------------------------------------------------------------

## 1. Mục đích

`ARCHITECTURE.md` định nghĩa cấu trúc hệ thống Sigma, ranh giới giữa các
module, hướng phụ thuộc, luồng dữ liệu và cách các lớp giao tiếp với
nhau.

Tài liệu này trả lời:

-   Sigma được cấu trúc như thế nào?
-   Các module có trách nhiệm gì?
-   Module nào được phép phụ thuộc module nào?
-   Research, Core, API và UI liên kết ra sao?
-   Financial computation nằm ở đâu?
-   Quantum computation nằm ở đâu?
-   Dữ liệu đi qua hệ thống như thế nào?
-   API boundary được đặt ở đâu?
-   Hệ thống có thể phát triển như thế nào mà không phá vỡ core?

Tài liệu này là architectural source of truth ở cấp hệ thống. Chi tiết
về data/domain objects thuộc `SCHEMA.md`; technology selection thuộc
`TECH_STACK.md`; các quy tắc bất biến thuộc `RULES.md`.

------------------------------------------------------------------------

# 2. Architectural Vision

Sigma được xây dựng như một **Modular Monolith** với một Risk
Intelligence Core rõ ràng, một API boundary ổn định và các client có thể
thay thế.

Kiến trúc mục tiêu:

``` text
Research
   ↓
Sigma Core
   ↓
Application
   ↓
FastAPI
   ↓
Taipy / Other Clients
```

Core phải độc lập với UI và API framework.

Nguyên tắc:

> **One Repository → Modular Core → Clear Boundaries → API-first →
> Replaceable Clients**

Sigma không được thiết kế theo hướng microservices ở V1.

------------------------------------------------------------------------

# 3. Architectural Principles

## 3.1. Modular Monolith

Toàn bộ Sigma V1 nằm trong một repository và một application boundary
chính.

Các module được tách theo trách nhiệm nghiệp vụ và computational
responsibility, không tách thành các service độc lập chỉ để tạo cảm giác
enterprise.

Lợi ích:

-   development đơn giản;
-   debugging dễ;
-   testing trực tiếp;
-   research integration thuận tiện;
-   giảm network overhead;
-   phù hợp với quy mô V1.

------------------------------------------------------------------------

## 3.2. Separation of Concerns

Mỗi layer có một trách nhiệm rõ ràng:

``` text
Domain
→ Financial concepts

Data
→ Market data

Modeling
→ Statistical / financial models

Scenarios
→ Scenario generation

Risk
→ Risk quantities and metrics

Quantum
→ Quantum estimation

Application
→ Orchestration

API
→ External interface

UI
→ Presentation
```

------------------------------------------------------------------------

## 3.3. Domain Independence

`domain/` không phụ thuộc:

-   FastAPI;
-   Taipy;
-   Qiskit;
-   database implementation;
-   external UI.

Domain định nghĩa financial concepts cần thiết cho Sigma.

------------------------------------------------------------------------

## 3.4. Classical First

Classical implementation là baseline của risk methodology.

Quantum không được trở thành dependency bắt buộc để chạy Classical Risk
Analysis.

Nếu Quantum backend lỗi, Classical Risk Analysis vẫn phải hoạt động.

------------------------------------------------------------------------

## 3.5. Quantum Where Justified

Quantum chỉ được sử dụng tại những computational problem đã có:

``` text
Financial Problem
→ Mathematical Formulation
→ Classical Baseline
→ Quantum Formulation
→ Benchmark
```

Quantum không phải một pipeline độc lập thay thế toàn bộ Sigma.

------------------------------------------------------------------------

## 3.6. API First

FastAPI là interface giữa Sigma Core và external clients.

Taipy không được truy cập trực tiếp internal core modules.

``` text
Taipy
   ↓ HTTP
FastAPI
   ↓
Application
   ↓
Core
```

------------------------------------------------------------------------

## 3.7. Research Is Not Production Core

`research/` là nơi:

-   exploration;
-   hypothesis testing;
-   experiments;
-   benchmark;
-   prototyping.

Logic ổn định mới được promotion vào `src/sigma/`.

Không copy-paste notebook thành production implementation.

------------------------------------------------------------------------

# 4. Repository Architecture

Cấu trúc repository:

``` text
sigma/
│
├── src/
│   └── sigma/
│       ├── domain/
│       ├── data/
│       ├── modeling/
│       ├── scenarios/
│       ├── risk/
│       ├── quantum/
│       ├── application/
│       └── api/
│
├── ui/
│
├── research/
│   ├── notebooks/
│   └── experiments/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── artifacts/
│
├── configs/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── docs/
│
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
└── Makefile
```

Repository structure là organizational boundary. Không phải mọi folder
đều là runtime layer.

------------------------------------------------------------------------

# 5. System Context

Sigma nằm giữa các nguồn dữ liệu, người dùng tài chính, external clients
và computational backends.

``` mermaid
flowchart LR
    User["Risk Analyst / Portfolio Manager / Quant"]
    Data["Market Data Sources"]
    UI["Taipy Reference Client"]
    API["Sigma API"]
    Core["Sigma Risk Intelligence Core"]
    Quantum["Quantum Simulator / Hardware"]

    User --> UI
    UI --> API
    Data --> Core
    API --> Core
    Core --> Quantum
    Core --> API
    API --> UI
    UI --> User
```

### Context interpretation

-   Người dùng tương tác với Sigma thông qua client.
-   Taipy là reference client V1.
-   FastAPI cung cấp product-facing interface.
-   Core thực hiện financial computation.
-   Market data đi vào Data layer.
-   Quantum backend chỉ được sử dụng khi một computation path yêu cầu.
-   Quantum backend không phải system-of-record của Sigma.

------------------------------------------------------------------------

# 6. High-Level Architecture

``` mermaid
flowchart TD
    UI["Taipy Reference UI"]

    API["FastAPI API"]

    APP["Application Layer"]

    DOMAIN["Domain"]
    DATA["Data"]
    MODEL["Modeling"]
    SCENARIOS["Scenarios"]
    RISK["Risk"]
    QUANTUM["Quantum"]

    UI --> API
    API --> APP

    APP --> DOMAIN
    APP --> DATA
    APP --> MODEL
    APP --> SCENARIOS
    APP --> RISK
    APP --> QUANTUM

    DATA --> DOMAIN
    MODEL --> DOMAIN
    SCENARIOS --> DOMAIN
    RISK --> DOMAIN
    QUANTUM --> DOMAIN
```

Đây là conceptual architecture. Chi tiết class/interface thuộc
implementation và schema documents.

------------------------------------------------------------------------

# 7. Core Layers

## 7.1. Domain Layer

Path:

``` text
src/sigma/domain/
```

Gồm các financial concepts như:

``` text
portfolio.py
market.py
scenario.py
risk.py
```

Domain có trách nhiệm biểu diễn các khái niệm mà các module khác cùng
hiểu.

Ví dụ conceptual objects:

``` text
Portfolio
Position
MarketData
Scenario
RiskEstimate
```

Domain không thực hiện:

-   HTTP;
-   UI;
-   quantum circuit execution;
-   external API orchestration.

------------------------------------------------------------------------

# 8. Data Layer

Path:

``` text
src/sigma/data/
```

Các module:

``` text
loaders.py
sources.py
preprocessing.py
```

Data layer chịu trách nhiệm:

``` text
External / Stored Data
        ↓
Loading
        ↓
Validation / Preprocessing
        ↓
Domain-compatible Data
```

Data layer không quyết định VaR/CVaR và không chứa UI logic.

Data source abstraction cho phép Sigma thay đổi nguồn dữ liệu mà không
thay đổi risk methodology.

------------------------------------------------------------------------

# 9. Modeling Layer

Path:

``` text
src/sigma/modeling/
```

Các module:

``` text
returns.py
volatility.py
regime.py
distribution.py
```

Modeling chịu trách nhiệm biến market observations thành
statistical/financial representations phục vụ scenario generation và
risk estimation.

Conceptual flow:

``` text
Market Data
    ↓
Returns
    ↓
Volatility
    ↓
Regime
    ↓
Distribution
```

Modeling không trực tiếp điều khiển UI hoặc API.

------------------------------------------------------------------------

# 10. Scenario Layer

Path:

``` text
src/sigma/scenarios/
```

Các module:

``` text
monte_carlo.py
stress.py
```

Scenario layer chịu trách nhiệm:

-   scenario generation;
-   portfolio scenario propagation;
-   stress scenario construction.

Conceptual flow:

``` text
Distribution / Market State
        ↓
Scenario Engine
        ↓
Portfolio Outcomes
        ↓
Loss Distribution
```

Monte Carlo là Classical baseline quan trọng của Sigma.

------------------------------------------------------------------------

# 11. Risk Layer

Path:

``` text
src/sigma/risk/
```

Các module:

``` text
var.py
cvar.py
metrics.py
```

Risk layer định nghĩa và tính toán risk quantities.

Ví dụ:

``` text
VaR
CVaR / Expected Shortfall
Expected Loss
Risk Metrics
Risk Contribution
```

Risk layer không phụ thuộc Quantum.

Điều này rất quan trọng:

``` text
Risk
  ↑
Classical Estimator
  ↑
Scenario / Distribution
```

Quantum có thể cung cấp một estimator cho một quantity phù hợp, nhưng
khái niệm financial risk không thuộc Quantum layer.

------------------------------------------------------------------------

# 12. Quantum Layer

Path:

``` text
src/sigma/quantum/
```

Các module:

``` text
amplitude_estimation.py
state_preparation.py
oracle.py
benchmark.py
```

Quantum layer chịu trách nhiệm về computational implementation của các
quantum estimation methods.

Conceptual flow:

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
Estimate
```

Quantum layer phải theo dõi các resource factors phù hợp:

-   qubits;
-   circuit depth;
-   shots;
-   query count;
-   state preparation cost;
-   oracle cost;
-   noise;
-   runtime.

Quantum layer không:

-   load raw market data trực tiếp;
-   thực hiện UI;
-   điều khiển FastAPI;
-   định nghĩa product workflow.

------------------------------------------------------------------------

# 13. Application Layer

Path:

``` text
src/sigma/application/
```

Các module:

``` text
portfolio_analysis.py
quantum_benchmark.py
```

Application layer là orchestration layer.

Nó kết nối các capabilities:

``` text
Data
 ↓
Modeling
 ↓
Scenarios
 ↓
Risk
```

và:

``` text
Classical Estimator
        ↕
Quantum Estimator
        ↓
Benchmark
```

Application layer không nên chứa low-level statistical implementation.

Nó quyết định **workflow nào được thực hiện**, không tự implement toàn
bộ computation.

------------------------------------------------------------------------

# 14. API Layer

Path:

``` text
src/sigma/api/
```

Cấu trúc:

``` text
api/
├── main.py
├── routes/
│   ├── health.py
│   ├── portfolios.py
│   ├── scenarios.py
│   └── quantum.py
└── schemas/
    ├── portfolio.py
    ├── risk.py
    └── quantum.py
```

API layer là external interface.

Responsibilities:

-   request handling;
-   response serialization;
-   API validation;
-   routing;
-   dependency wiring;
-   HTTP concerns.

API không được trở thành nơi chứa:

``` text
GARCH calculation
Monte Carlo implementation
VaR calculation
QAE circuit construction
```

Các computation đó thuộc Core.

------------------------------------------------------------------------

# 15. UI Layer

Path:

``` text
ui/
```

Cấu trúc:

``` text
ui/
├── app.py
├── pages/
├── components/
├── api_client.py
└── assets/
```

Taipy là reference client.

UI chịu trách nhiệm:

-   user interaction;
-   input collection;
-   presentation;
-   visualization;
-   interaction state.

UI giao tiếp với backend qua:

``` text
ui/api_client.py
        ↓ HTTP
FastAPI
```

UI không import:

``` text
sigma.risk
sigma.quantum
sigma.modeling
```

để thực hiện business computation.

------------------------------------------------------------------------

# 16. Research Layer

Path:

``` text
research/
├── notebooks/
└── experiments/
```

Research được thiết kế như experimental boundary.

## Notebooks

Dùng cho:

-   exploration;
-   visualization;
-   hypothesis testing;
-   methodology prototyping.

## Experiments

``` text
experiments/
├── classical/
└── quantum/
```

Dùng cho reproducible experiments và benchmark.

Research có thể import Core:

``` text
Research
   ↓
Sigma Core
```

nhưng Core không import Research:

``` text
Sigma Core
   ✕
Research
```

------------------------------------------------------------------------

# 17. Tests & Evaluation

Path:

``` text
tests/
├── unit/
├── integration/
└── evaluation/
```

## Unit

Kiểm tra module/function behavior.

## Integration

Kiểm tra interaction giữa các modules và API/application boundaries.

## Evaluation

Đây là lớp scientific evaluation.

Dùng cho:

-   Classical baseline;
-   Quantum benchmark;
-   accuracy;
-   convergence;
-   resource usage;
-   noise sensitivity;
-   end-to-end comparison.

Evaluation không chỉ kiểm tra "code chạy".

------------------------------------------------------------------------

# 18. End-to-End Data Flow

``` mermaid
flowchart TD
    MARKET["Market Data"]
    VALIDATE["Validation / Cleaning"]
    RETURNS["Returns"]
    VOL["Volatility"]
    REGIME["Regime"]
    DIST["Regime-Aware Distribution"]
    SCENARIO["Scenario Generation"]
    LOSS["Portfolio Loss Distribution"]
    CLASSICAL["Classical Risk Estimation"]
    QUANTUM["Quantum Risk Estimation"]
    RISK["VaR / CVaR"]
    INTEL["Risk Intelligence"]
    API["FastAPI"]
    UI["Taipy"]

    MARKET --> VALIDATE
    VALIDATE --> RETURNS
    RETURNS --> VOL
    VOL --> REGIME
    REGIME --> DIST
    DIST --> SCENARIO
    SCENARIO --> LOSS

    LOSS --> CLASSICAL
    LOSS --> QUANTUM

    CLASSICAL --> RISK
    QUANTUM --> RISK

    RISK --> INTEL
    INTEL --> API
    API --> UI
```

Đây là logical data flow. Chi tiết data schema sẽ được định nghĩa trong
`SCHEMA.md`.

------------------------------------------------------------------------

# 19. Classical--Quantum Boundary

Sigma có hai computational paths:

``` text
                 Financial Quantity
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
         Classical            Quantum
         Estimator             Estimator
              │                   │
              └─────────┬─────────┘
                        ▼
                    Benchmark
                        │
                        ▼
                Risk Intelligence
```

Classical path có thể sử dụng:

``` text
Monte Carlo
```

Quantum path có thể sử dụng:

``` text
Amplitude Estimation
```

Benchmark phải so sánh cùng quantity.

------------------------------------------------------------------------

# 20. Quantum Is Not a Separate Product

Không sử dụng architecture:

``` text
Sigma Risk
     +
Sigma Quantum
```

theo kiểu hai hệ thống độc lập.

Thay vào đó:

``` text
Sigma
│
└── Risk Intelligence
      │
      ├── Classical Methods
      │
      └── Quantum Methods
```

Quantum là computational enhancement layer.

Điều này cho phép:

-   Classical fallback;
-   fair benchmark;
-   independent evolution;
-   tránh coupling risk methodology với quantum implementation.

------------------------------------------------------------------------

# 21. Application Execution Flow

Một portfolio risk analysis có thể đi theo:

``` text
Client
  ↓
FastAPI
  ↓
Application
  ↓
Load / Validate Data
  ↓
Build Portfolio Context
  ↓
Model Returns / Volatility / Regime
  ↓
Build Distribution
  ↓
Generate Scenarios
  ↓
Build Loss Distribution
  ↓
Calculate Risk
  ↓
Return Risk Result
```

Quantum benchmark là workflow riêng:

``` text
Client
  ↓
FastAPI
  ↓
Application
  ↓
Define Financial Quantity
  ↓
Run Classical Baseline
  ↓
Prepare Quantum Representation
  ↓
Run Quantum Estimator
  ↓
Collect Resources
  ↓
Compare
  ↓
Return Benchmark
```

------------------------------------------------------------------------

# 22. API Boundary

Boundary:

``` mermaid
flowchart LR
    CLIENT["Taipy / External Client"]
    API["FastAPI"]
    APP["Application"]
    CORE["Sigma Core"]

    CLIENT -->|HTTP| API
    API --> APP
    APP --> CORE
```

API request không được truyền trực tiếp vào low-level model functions mà
không qua application contract khi workflow có orchestration.

API response phải là product-facing representation của kết quả, không
expose internal implementation details không cần thiết.

------------------------------------------------------------------------

# 23. Dependency Direction

Dependency direction được giữ một chiều ở mức architecture:

``` text
UI
 ↓ HTTP
API
 ↓
Application
 ↓
Core Modules
```

Trong Core:

``` text
Application
 ↓
Domain
Data
Modeling
Scenarios
Risk
Quantum
```

Research:

``` text
Research
 ↓
Core
```

Không được:

``` text
Core
 ↓
Research
```

và không được:

``` text
Domain
 ↓
API
UI
Quantum Framework
```

------------------------------------------------------------------------

# 24. Dependency Rules

## Rule 1

Domain không biết API/UI.

## Rule 2

Risk không phụ thuộc Quantum.

## Rule 3

Quantum không phụ thuộc UI.

## Rule 4

UI chỉ giao tiếp với backend thông qua API.

## Rule 5

API không chứa financial business logic.

## Rule 6

Research không trở thành runtime dependency của Core.

## Rule 7

Application orchestrates; engines compute.

## Rule 8

Infrastructure/framework details không được leak vào Domain nếu không
cần thiết.

------------------------------------------------------------------------

# 25. Configuration Boundary

Configuration nằm tại:

``` text
configs/
├── default.yaml
└── benchmark.yaml
```

Configuration có thể định nghĩa:

-   model parameters;
-   scenario parameters;
-   benchmark settings;
-   experiment settings.

Configuration không nên chứa business logic.

Secrets không nằm trong repository.

`.env.example` mô tả environment variables cần thiết; secret thật được
quản lý bên ngoài source code.

------------------------------------------------------------------------

# 26. Data Storage Boundary

Repository có:

``` text
data/
├── raw/
├── processed/
└── artifacts/
```

Conceptual flow:

``` text
Raw
 ↓
Processed
 ↓
Artifacts
```

Data storage là supporting layer, không phải business logic.

Risk Engine không nên phụ thuộc cứng vào một local file format nếu data
contract có thể được abstraction.

------------------------------------------------------------------------

# 27. Deployment Architecture --- V1

V1 ưu tiên deployment đơn giản:

``` mermaid
flowchart TB
    USER["User"]
    UI["Taipy Client"]
    API["FastAPI Application"]
    CORE["Sigma Core"]
    DATA["Data Sources / Local Data"]
    QS["Quantum Simulator / Backend"]

    USER --> UI
    UI --> API
    API --> CORE
    DATA --> CORE
    CORE --> QS
```

Không yêu cầu:

-   Kubernetes;
-   microservices;
-   distributed service mesh;
-   message broker.

Các thành phần mới chỉ được thêm khi có workload hoặc product
requirement thực sự.

------------------------------------------------------------------------

# 28. Runtime Separation

Về logical runtime:

``` text
UI Runtime
    │
    │ HTTP
    ▼
API Runtime
    │
    ▼
Sigma Core
```

Trong V1, các thành phần Core có thể chạy trong cùng application/process
boundary khi phù hợp.

Điều này không có nghĩa architecture mất modularity.

**Module boundary và process boundary là hai khái niệm khác nhau.**

------------------------------------------------------------------------

# 29. Scalability Strategy

Sigma V1 không tối ưu cho distributed scale trước khi có evidence cần
thiết.

Evolution path:

``` text
Modular Monolith
      ↓
Profile Bottlenecks
      ↓
Identify Real Workload
      ↓
Optimize Core
      ↓
Scale Specific Component
```

Nếu sau này một computation trở thành bottleneck thực sự, component đó
mới được xem xét tách riêng.

Ví dụ:

``` text
Quantum Job Execution
```

có thể trở thành asynchronous external job nếu workload thực tế yêu cầu.

Không tách service trước khi có bottleneck.

------------------------------------------------------------------------

# 30. Research-to-Production Boundary

Logic được promotion theo flow:

``` text
Hypothesis
    ↓
Notebook
    ↓
Experiment
    ↓
Validation
    ↓
Stable Method
    ↓
Core Module
    ↓
Application
    ↓
API
    ↓
UI
```

Không đi ngược:

``` text
UI
 ↓
Notebook
```

và không lấy demo code làm production core.

------------------------------------------------------------------------

# 31. Scientific Reproducibility Boundary

Mỗi experiment quan trọng nên có:

``` text
Dataset
Model
Parameters
Random Seed
Method
Backend
Quantum Resources
Output Metrics
```

Research artifacts phải có khả năng truy ngược tới methodology và code
version phù hợp.

------------------------------------------------------------------------

# 32. Failure Isolation

Một failure trong Quantum path không được làm mất Classical Risk
capability.

Conceptually:

``` text
Risk Analysis
      │
      ├── Classical → available
      │
      └── Quantum → optional / research path
```

Nếu Quantum backend không khả dụng:

``` text
Quantum Failure
      ↓
Benchmark unavailable
      ↓
Classical Risk Analysis remains available
```

Đây là architectural requirement quan trọng.

------------------------------------------------------------------------

# 33. Observability Boundary

V1 chỉ cần observability ở mức phù hợp:

-   application errors;
-   API errors;
-   computation duration;
-   benchmark metadata;
-   experiment results.

Không cần xây một distributed observability platform khi chưa có
distributed architecture.

------------------------------------------------------------------------

# 34. Security Boundary

Security responsibility được phân lớp:

``` text
Client
  ↓
API Boundary
  ↓
Application
  ↓
Core
```

Secrets:

``` text
.env / external secret management
```

không nằm trong:

``` text
source code
configs/default.yaml
notebooks
```

Financial data access policy phải được xác định theo deployment context.

------------------------------------------------------------------------

# 35. Architecture Decisions

## ADR-01 --- Modular Monolith

**Decision:** Sigma V1 sử dụng Modular Monolith.

**Reason:** giảm complexity và giữ development/research velocity trong
giai đoạn đầu.

------------------------------------------------------------------------

## ADR-02 --- FastAPI as Product API

**Decision:** FastAPI là interface giữa Sigma và clients.

**Reason:** giữ Core độc lập với UI và tạo integration boundary rõ ràng.

------------------------------------------------------------------------

## ADR-03 --- Taipy as Reference Client

**Decision:** Taipy là reference UI client V1.

**Reason:** phù hợp với Python-centric research/product prototype và cho
phép xây dashboard nhanh mà không đưa UI logic vào Core.

------------------------------------------------------------------------

## ADR-04 --- Research Outside Core

**Decision:** Research notebooks và experiments nằm ngoài `src/sigma`.

**Reason:** bảo vệ production core khỏi exploratory code.

------------------------------------------------------------------------

## ADR-05 --- Quantum Inside Core Boundary

**Decision:** Quantum là module trong Sigma Core thay vì một service độc
lập.

**Reason:** V1 chưa có workload justification cho quantum microservice;
giữ computation gần financial formulation và benchmark logic.

------------------------------------------------------------------------

## ADR-06 --- Risk Independent from Quantum

**Decision:** Risk layer không phụ thuộc Quantum layer.

**Reason:** risk concepts phải tồn tại độc lập với computational
implementation.

------------------------------------------------------------------------

## ADR-07 --- No Premature Infrastructure

**Decision:** Không thêm microservices, Kubernetes, Kafka,
Airflow/Prefect hoặc distributed infrastructure vào V1 nếu chưa có
requirement.

**Reason:** tránh over-engineering và giữ architecture aligned với
actual workload.

------------------------------------------------------------------------

# 36. Architectural Non-Goals

V1 không hướng tới:

-   microservices;
-   Kubernetes;
-   enterprise distributed architecture;
-   real-time trading infrastructure;
-   high-frequency computation;
-   autonomous portfolio management;
-   quantum-only architecture;
-   database-heavy architecture khi chưa cần;
-   frontend/backend code duplication;
-   infrastructure abstraction chỉ để "trông enterprise".

------------------------------------------------------------------------

# 37. Architecture Evolution

Architecture phải cho phép mở rộng:

``` text
                 Sigma
                   │
        ┌──────────┴──────────┐
        │                     │
 Risk Intelligence       Future Intelligence
        │
 ┌──────┼────────┐
 │      │        │
Classical Quantum Scenario
```

Các capability tương lai có thể được thêm vào bằng module boundaries rõ
ràng thay vì phá vỡ Core.

Nếu một module trở thành independent scalability bottleneck, nó có thể
được tách thành service sau khi có evidence.

------------------------------------------------------------------------

# 38. Architectural Success Criteria

Kiến trúc V1 được xem là đạt yêu cầu khi:

### Modularity

Các module có responsibility rõ ràng.

### Dependency Safety

Không có dependency direction ngược từ Core lên API/UI.

### Classical Independence

Classical Risk Analysis hoạt động không cần Quantum backend.

### API Isolation

Client không truy cập trực tiếp internal Core.

### Research Isolation

Exploratory research không trở thành production dependency.

### Testability

Core modules có thể test độc lập.

### Reproducibility

Research/evaluation có thể tái tạo theo configuration và metadata.

### Evolvability

Có thể thay đổi UI/client hoặc data source mà không viết lại Risk
Engine.

------------------------------------------------------------------------

# 39. Architecture North Star

Sigma được tổ chức theo:

``` text
                    USER
                      │
                      ▼
                 TAIPY / CLIENT
                      │
                     HTTP
                      │
                      ▼
                   FASTAPI
                      │
                      ▼
                APPLICATION
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      DOMAIN        ENGINES       DATA
        │             │
        │      ┌──────┼──────┐
        │      ▼      ▼      ▼
        │   MODEL  SCENARIO RISK
        │                    │
        │                    ▼
        │                 QUANTUM
        │
        └─────────────┬──────────────
                      ▼
                RISK INTELLIGENCE
                      │
                      ▼
                DECISION SUPPORT
```

Nguyên tắc cuối cùng:

> **Sigma Core phải là một Financial Risk Intelligence Engine độc lập
> với giao diện; API là boundary để productize Core; Taipy là client có
> thể thay thế; Research là experimental layer; Quantum là computational
> enhancement layer; và mọi thành phần phải giữ đúng ranh giới trách
> nhiệm của mình.**

------------------------------------------------------------------------

# 40. Architecture Principle

> **Structure follows responsibility.**
>
> **Interfaces surround the Core.**
>
> **Research informs the Core.**
>
> **Classical establishes the baseline.**
>
> **Quantum enhances only where justified.**
>
> **Complexity is introduced only when the system has earned it.**

→ **SIGMA MODULAR RISK INTELLIGENCE ARCHITECTURE**
