# Sigma --- Technology Stack

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Runtime, API, UI, Data, Modeling, Quantum, Testing và
> Development Tooling\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`TECH_STACK.md` định nghĩa các công nghệ được lựa chọn cho Sigma V1, vai
trò của từng công nghệ và boundary sử dụng chúng.

Tài liệu này trả lời:

-   Sigma sử dụng ngôn ngữ và runtime nào?
-   API được xây dựng bằng gì?
-   UI/reference client sử dụng gì?
-   Financial/ML computation sử dụng ecosystem nào?
-   Quantum layer sử dụng gì?
-   Testing và development tooling ra sao?
-   Công nghệ nào là bắt buộc, công nghệ nào là optional?
-   Những công nghệ nào **cố tình chưa đưa vào V1**?

Tài liệu này không thay thế `ARCHITECTURE.md`, `SCHEMA.md` hoặc
`RULES.md`.

------------------------------------------------------------------------

# 2. Technology Philosophy

Technology selection của Sigma tuân theo:

``` text
Financial Requirement
        ↓
Architectural Requirement
        ↓
Technical Requirement
        ↓
Technology Selection
```

Không chọn technology chỉ vì:

-   đang phổ biến;
-   "enterprise";
-   có nhiều stars;
-   có quantum branding;
-   làm architecture trông phức tạp hơn.

Nguyên tắc:

> **Use the simplest technology that satisfies the actual requirement.**

------------------------------------------------------------------------

# 3. V1 Technology Overview

  -----------------------------------------------------------------------
  Layer                   Technology              Vai trò
  ----------------------- ----------------------- -----------------------
  Language                Python 3.12.x           Runtime chính

  Package / Environment   `uv`                    Dependency &
                                                  environment management

  API                     FastAPI                 Product API

  API Server              Uvicorn                 ASGI server

  UI                      Taipy                   Reference client V1

  DataFrame               pandas                  Tabular financial data

  Numerical Computing     NumPy                   Numerical primitives

  Scientific Computing    SciPy                   Statistical/numerical
                                                  methods

  Visualization           Plotly                  Interactive charts

  Statistical Modeling    statsmodels             Classical statistical
                                                  models khi phù hợp

  ML                      scikit-learn            Classical ML /
                                                  evaluation khi cần

  Quantum SDK             Qiskit                  Quantum circuit /
                                                  algorithm
                                                  implementation

  Quantum Simulation      Qiskit Aer              Local simulation

  Testing                 pytest                  Unit/integration tests

  Formatting              Ruff                    Formatting

  Linting                 Ruff                    Linting

  Type Checking           Pyright                 Static type checking

  Documentation           Markdown + Mermaid      Project documentation

  Version Control         Git                     Source control
  -----------------------------------------------------------------------

Các package cụ thể phải được pin/lock trong project dependency
configuration; bảng này mô tả vai trò, không thay thế
`pyproject.toml`/lockfile.

------------------------------------------------------------------------

# 4. Python Runtime

## 4.1. Python 3.12

Sigma V1 sử dụng:

``` text
Python 3.12.x
```

Python là runtime chính cho:

-   Core;
-   Data;
-   Modeling;
-   Risk;
-   Quantum;
-   FastAPI;
-   Taipy;
-   Research.

### Lý do

Python phù hợp với toàn bộ ecosystem hiện tại của Sigma:

``` text
Financial Computing
+
Scientific Computing
+
ML
+
Quantum Computing
+
API
+
Research
```

------------------------------------------------------------------------

## 4.2. Python Version Policy

Project phải pin minor/patch version phù hợp với development
environment.

Ví dụ:

``` text
.python-version
```

được dùng để đảm bảo team sử dụng cùng Python runtime.

Không upgrade Python giữa chừng chỉ vì có version mới hơn.

Upgrade phải được xem như dependency/runtime change và cần verification.

------------------------------------------------------------------------

# 5. Package & Environment Management --- uv

Sigma sử dụng:

``` text
uv
```

cho:

-   Python version management;
-   virtual environment;
-   dependency management;
-   lockfile;
-   reproducible development environment.

Primary workflow:

``` text
uv python
uv venv
uv add
uv sync
uv run
```

Dependency installation phải thông qua project configuration và lockfile
thay vì cài package thủ công ngoài environment.

------------------------------------------------------------------------

# 6. API Stack

## 6.1. FastAPI

FastAPI là product API boundary của Sigma.

``` text
Client
  ↓ HTTP
FastAPI
  ↓
Application
  ↓
Sigma Core
```

FastAPI chịu trách nhiệm:

-   routing;
-   request/response;
-   validation;
-   serialization;
-   API documentation;
-   dependency wiring.

FastAPI không chịu trách nhiệm:

-   VaR implementation;
-   CVaR implementation;
-   Monte Carlo engine;
-   regime modeling;
-   QAE circuit logic.

------------------------------------------------------------------------

## 6.2. Uvicorn

Uvicorn là ASGI server cho FastAPI.

Development:

``` text
uv run uvicorn sigma.api.main:app --reload
```

Production/deployment configuration có thể thay đổi theo environment.

------------------------------------------------------------------------

# 7. UI Stack --- Taipy

Taipy là **reference client V1** của Sigma.

Architecture:

``` text
Taipy
  ↓ HTTP
FastAPI
  ↓
Sigma Core
```

Taipy chịu trách nhiệm:

-   dashboard;
-   portfolio interaction;
-   risk visualization;
-   scenario exploration;
-   stress testing interface;
-   quantum benchmark presentation.

Taipy không chứa:

``` text
Financial Business Logic
Risk Engine
Quantum Engine
```

------------------------------------------------------------------------

# 8. Why Taipy

Taipy phù hợp với V1 vì:

-   Python-native;
-   phù hợp với data/analytics application;
-   cho phép xây interactive UI nhanh;
-   phù hợp với prototype/product interface;
-   có thể giao tiếp với FastAPI qua HTTP.

Tuy nhiên:

> **Taipy là client, không phải Sigma Core.**

Nếu tương lai thay Taipy bằng một client khác, Core và API contract
không nên phải được viết lại.

------------------------------------------------------------------------

# 9. Data Stack

## 9.1. NumPy

NumPy là numerical foundation cho:

-   arrays;
-   vectorized computation;
-   numerical operations;
-   numerical representation.

NumPy được sử dụng ở low-level computational boundaries khi phù hợp.

------------------------------------------------------------------------

## 9.2. pandas

pandas dùng cho:

-   tabular market data;
-   time series;
-   preprocessing;
-   dataset inspection;
-   return calculation;
-   data transformation.

Ví dụ:

``` text
Market Data
    ↓
pandas
    ↓
Validated Time Series
```

pandas không phải financial domain model.

Core domain objects không nên phụ thuộc vào DataFrame representation nếu
không cần thiết.

------------------------------------------------------------------------

## 9.3. SciPy

SciPy được sử dụng cho:

-   statistical distributions;
-   numerical optimization;
-   numerical routines;
-   statistical computation.

Chỉ sử dụng module phù hợp với methodology.

------------------------------------------------------------------------

# 10. Statistical / Financial Modeling

## 10.1. statsmodels

`statsmodels` là một lựa chọn cho classical statistical modeling khi
methodology cần.

Có thể sử dụng cho:

-   statistical estimation;
-   time-series models;
-   econometric analysis.

Không mặc định mọi volatility/regime model đều phải dùng statsmodels.

------------------------------------------------------------------------

## 10.2. GARCH / Volatility

Nếu Sigma sử dụng GARCH hoặc volatility methodology khác, package được
lựa chọn dựa trên:

-   model correctness;
-   API stability;
-   compatibility;
-   testing;
-   reproducibility.

Không chọn package chỉ vì tiện import.

------------------------------------------------------------------------

# 11. Machine Learning

## scikit-learn

`scikit-learn` là classical ML toolkit khi Sigma cần:

-   baseline models;
-   preprocessing;
-   evaluation;
-   clustering/classification/regression;
-   model comparison.

ML không phải core identity của Sigma V1.

Sigma là **Risk Intelligence Engine**, vì vậy ML chỉ được thêm khi có
financial/statistical justification.

------------------------------------------------------------------------

# 12. Visualization --- Plotly

Plotly được dùng cho interactive visualization.

Primary use cases:

``` text
Loss Distribution
Risk Contribution
Scenario Analysis
Stress Comparison
Benchmark Comparison
```

Visualization phải phục vụ analysis.

Không thêm chart chỉ để dashboard có nhiều biểu đồ.

------------------------------------------------------------------------

# 13. Quantum Stack

## 13.1. Qiskit

Qiskit là primary quantum SDK của Sigma V1.

Vai trò:

-   quantum circuit construction;
-   quantum algorithm implementation;
-   state preparation;
-   oracle implementation;
-   amplitude estimation;
-   measurement.

Qiskit nằm trong:

``` text
src/sigma/quantum/
```

không lan sang:

``` text
domain/
risk/
api/
ui/
```

nếu không có architectural reason.

------------------------------------------------------------------------

## 13.2. Qiskit Aer

Qiskit Aer dùng cho local quantum simulation.

Các use cases:

-   ideal simulation;
-   noisy simulation;
-   circuit validation;
-   algorithm debugging;
-   benchmark experiments.

Simulator result phải được phân biệt với hardware result.

------------------------------------------------------------------------

# 14. Quantum Hardware Boundary

V1 không architecture-lock Sigma vào một quantum hardware provider duy
nhất.

Conceptual interface:

``` text
Quantum Method
      ↓
Quantum Backend
      ├── Simulator
      └── Hardware
```

Điều này cho phép benchmark:

``` text
Ideal
Noisy Simulator
Hardware
```

mà không thay đổi financial problem formulation.

Hardware integration chỉ được thêm khi research/product requirement cần.

------------------------------------------------------------------------

# 15. Quantum Resource Measurement

Quantum stack phải hỗ trợ thu thập khi phù hợp:

``` text
Qubits
Circuit Depth
Gate Count
Shots
Oracle Queries
Runtime
Noise Model
Backend
```

Các metrics này là một phần của benchmark evidence, không chỉ là
debugging information.

------------------------------------------------------------------------

# 16. Testing Stack --- pytest

`pytest` là testing framework chính.

Structure:

``` text
tests/
├── unit/
├── integration/
└── evaluation/
```

### Unit

Kiểm tra:

-   domain behavior;
-   numerical functions;
-   risk calculations;
-   quantum helper logic.

### Integration

Kiểm tra:

-   application workflows;
-   API;
-   module interaction.

### Evaluation

Kiểm tra:

-   model behavior;
-   Classical baseline;
-   Quantum benchmark;
-   accuracy;
-   resource behavior.

------------------------------------------------------------------------

# 17. Formatting & Linting --- Ruff

Ruff được sử dụng làm primary tool cho:

``` text
Formatting
Linting
```

Mục tiêu:

-   consistent code style;
-   fast feedback;
-   giảm toolchain fragmentation.

Không thêm nhiều formatter/linter khác nếu Ruff đã đáp ứng requirement.

------------------------------------------------------------------------

# 18. Type Checking --- Pyright

Pyright được sử dụng cho static type checking.

Mục tiêu:

-   phát hiện interface mismatch;
-   tăng reliability;
-   làm rõ module contracts;
-   giảm runtime errors.

Type checking phải hỗ trợ architecture, không biến code thành type
ceremony không cần thiết.

------------------------------------------------------------------------

# 19. Documentation Stack

Documentation sử dụng:

``` text
Markdown
+
Mermaid
```

Mermaid được dùng cho:

-   architecture diagrams;
-   data flow;
-   dependency relationships;
-   system context;
-   sequence/workflow khi cần.

Không lưu diagram architecture chính dưới dạng image nếu Mermaid có thể
biểu diễn rõ ràng.

Lợi ích:

-   version controlled;
-   diffable;
-   editable;
-   reproducible.

------------------------------------------------------------------------

# 20. Git

Git là version control system.

Git phải track:

``` text
Source
Tests
Docs
Configurations
Research Experiment Definitions
```

Không commit:

``` text
Secrets
Local virtual environments
Generated caches
Large unmanaged datasets
Temporary artifacts
```

------------------------------------------------------------------------

# 21. Data Source Boundary

Data provider không được trở thành core dependency.

Conceptual:

``` text
Data Source
    ↓
Data Adapter / Loader
    ↓
Sigma Data Contract
    ↓
Modeling
```

Điều này cho phép thay đổi provider mà không viết lại Risk Engine.

Nguồn dữ liệu cụ thể có thể thay đổi theo:

-   availability;
-   license;
-   cost;
-   data quality;
-   project stage.

`TECH_STACK.md` không khóa Sigma vào một vendor dữ liệu duy nhất.

------------------------------------------------------------------------

# 22. Configuration Stack

Configuration sử dụng file-based configuration + environment variables
khi phù hợp.

Ví dụ:

``` text
configs/
├── default.yaml
└── benchmark.yaml
```

Environment variables dùng cho:

``` text
API keys
Credentials
Environment-specific configuration
```

Không commit secrets.

------------------------------------------------------------------------

# 23. Dependency Categories

Dependencies của Sigma nên được phân nhóm:

``` text
Runtime
Development
Research
Optional
```

Ví dụ:

### Runtime

``` text
fastapi
uvicorn
numpy
pandas
scipy
plotly
taipy
```

### Research / Quantum

``` text
qiskit
qiskit-aer
```

### Development

``` text
pytest
ruff
pyright
```

Không phải mọi research dependency đều phải trở thành production
dependency.

------------------------------------------------------------------------

# 24. Production vs Research Dependencies

Một dependency chỉ được đưa vào production runtime khi production code
thực sự cần nó.

Ví dụ:

``` text
research/
    ↓
experimental package
```

không có nghĩa:

``` text
src/sigma/
    ↓
must depend on package
```

Điều này giúp giảm dependency footprint.

------------------------------------------------------------------------

# 25. Dependency Selection Rules

Một package mới chỉ nên được thêm khi có:

1.  Requirement rõ.
2.  Use case thực tế.
3.  Compatibility với Python 3.12.
4.  Compatibility với architecture.
5.  Maintenance/quality chấp nhận được.
6.  Không có giải pháp đơn giản hơn bằng dependency hiện có.

------------------------------------------------------------------------

# 26. Dependency Locking

Development environment phải reproducible.

Flow:

``` text
pyproject.toml
      ↓
uv lock
      ↓
uv.lock
      ↓
uv sync
```

Lockfile phải được commit vào repository nếu project workflow sử dụng
lockfile để reproducible environment.

------------------------------------------------------------------------

# 27. Environment Structure

Conceptual environments:

``` text
Local Development
        ↓
Research / Experiment
        ↓
Demo
        ↓
Production
```

V1 có thể sử dụng cùng Python project environment với dependency
groups/extras khi phù hợp thay vì tạo nhiều repository/environment phức
tạp.

------------------------------------------------------------------------

# 28. Local Development

Developer setup nên tối giản:

``` text
Python
uv
Git
```

Sau đó:

``` text
uv sync
```

và chạy application bằng `uv run`.

Không yêu cầu Docker để bắt đầu development nếu application không cần.

------------------------------------------------------------------------

# 29. API Documentation

FastAPI cung cấp API schema/documentation tự động.

API contract phải được xem là integration boundary.

Documentation phải phản ánh:

``` text
Request
Response
Validation
Error
```

Không expose implementation internals không cần thiết.

------------------------------------------------------------------------

# 30. Logging

V1 sử dụng application logging phù hợp với Python runtime.

Logging cần phục vụ:

-   debugging;
-   failed computation;
-   API errors;
-   benchmark execution;
-   important runtime events.

Không log:

``` text
API keys
Passwords
Sensitive credentials
```

------------------------------------------------------------------------

# 31. Observability

V1 chưa cần một distributed observability stack.

Theo dõi trước:

``` text
Application Errors
API Errors
Execution Time
Benchmark Metadata
Experiment Results
```

Nếu workload tăng và có evidence cần observability nâng cao, stack có
thể được mở rộng sau.

------------------------------------------------------------------------

# 32. Deployment Stack

V1 ưu tiên deployment đơn giản:

``` text
Taipy Client
      ↓
FastAPI
      ↓
Sigma Core
      ↓
Data / Quantum Backend
```

Không mặc định cần:

``` text
Kubernetes
Kafka
Service Mesh
Airflow
Prefect
```

chỉ để deployment "trông enterprise".

------------------------------------------------------------------------

# 33. Async / Background Computation

Nếu một computation trở nên long-running:

``` text
Risk Analysis
Quantum Benchmark
Large Scenario Generation
```

thì có thể bổ sung asynchronous execution.

Nhưng V1 không mặc định xây job orchestration platform.

Decision phải dựa trên:

``` text
Measured Runtime
User Experience
Concurrency
Workload
```

------------------------------------------------------------------------

# 34. Technology Boundaries

``` text
Taipy
  → UI only

FastAPI
  → API only

pandas
  → Data manipulation

NumPy / SciPy
  → Numerical computation

statsmodels / sklearn
  → Classical statistical / ML methods

Qiskit / Aer
  → Quantum computation

pytest
  → Testing

Ruff
  → Formatting / linting

Pyright
  → Type checking

uv
  → Environment / dependencies
```

Technology phải được sử dụng trong boundary phù hợp.

------------------------------------------------------------------------

# 35. Technologies Intentionally Not Required in V1

Các công nghệ sau **không phải default dependency**:

``` text
Docker
Kubernetes
Kafka
Airflow
Prefect
Redis
Celery
PostgreSQL
Spark
Ray
MLflow
Cloud-specific orchestration
```

Điều này không có nghĩa Sigma không bao giờ sử dụng chúng.

Nghĩa là:

> **Chưa có requirement đủ mạnh để đưa chúng vào V1.**

------------------------------------------------------------------------

# 36. Why No Database Is Locked Yet

Sigma V1 cần persistence nhưng `TECH_STACK.md` không nên khóa physical
database trước khi workload và persistence requirements được xác định
đầy đủ.

Logical data model đã được định nghĩa trong:

``` text
SCHEMA.md
```

Physical storage có thể được quyết định sau dựa trên:

-   persistence requirements;
-   concurrency;
-   deployment;
-   data volume;
-   query patterns.

------------------------------------------------------------------------

# 37. Why No MLOps Platform Yet

Sigma V1 không phải ML platform.

Nếu model training/deployment trở thành production requirement lớn, có
thể xem xét MLOps tooling.

Hiện tại:

``` text
Research
→ Experiment
→ Evaluation
→ Core
```

là đủ.

------------------------------------------------------------------------

# 38. Why No Workflow Orchestrator Yet

Sigma V1 không cần workflow orchestration platform chỉ để chạy:

``` text
Data
→ Modeling
→ Scenario
→ Risk
```

Application layer có thể orchestrate workflow.

Nếu sau này xuất hiện:

-   scheduled pipelines;
-   distributed jobs;
-   data dependencies;
-   retry-heavy workflows;

thì mới đánh giá orchestration technology.

------------------------------------------------------------------------

# 39. Technology Decision Matrix

  Requirement             Choice                Reason
  ----------------------- --------------------- -----------------------------------------
  General runtime         Python 3.12           Unified ecosystem
  Dependency management   uv                    Fast, reproducible
  API                     FastAPI               Clear API boundary
  UI                      Taipy                 Python-native analytics UI
  Numerical               NumPy                 Core numerical primitives
  Data                    pandas                Financial time-series/data manipulation
  Statistics              SciPy / statsmodels   Scientific/statistical methods
  ML                      scikit-learn          Classical ML baseline
  Visualization           Plotly                Interactive analytical charts
  Quantum                 Qiskit                Quantum SDK
  Simulation              Qiskit Aer            Local/noisy simulation
  Testing                 pytest                Python testing ecosystem
  Lint/format             Ruff                  Unified fast tooling
  Type checking           Pyright               Static analysis
  Docs                    Markdown/Mermaid      Version-controlled documentation
  VCS                     Git                   Collaboration/versioning

------------------------------------------------------------------------

# 40. Technology Evolution Rules

Technology changes phải tuân theo:

``` text
Requirement
    ↓
Evaluate Current Stack
    ↓
Identify Limitation
    ↓
Compare Alternatives
    ↓
Prototype
    ↓
Benchmark
    ↓
Decision
    ↓
Update Documentation
```

Không thay technology chỉ vì:

``` text
Newer
More Popular
More Enterprise
```

------------------------------------------------------------------------

# 41. Upgrade Policy

Dependency upgrade quan trọng phải kiểm tra:

``` text
Compatibility
Tests
Scientific Results
Benchmark Results
Performance
API Contracts
```

Đặc biệt với:

``` text
NumPy
SciPy
pandas
Qiskit
Taipy
FastAPI
```

các upgrade có thể ảnh hưởng behavior hoặc compatibility.

------------------------------------------------------------------------

# 42. Reproducibility Stack

Reproducibility của Sigma dựa trên:

``` text
Python Version
+
uv.lock
+
Git Commit
+
Dataset Version
+
Configuration
+
Model Version
+
Random Seed
+
Quantum Backend Configuration
```

Không cần mọi experiment phải có mọi field, nhưng experiment quan trọng
phải có đủ context để tái lập.

------------------------------------------------------------------------

# 43. Security Rules

Technology stack phải hỗ trợ nguyên tắc:

``` text
Secrets outside source code
```

API credentials:

``` text
Environment Variables
```

không:

``` text
hard-coded in Python
hard-coded in notebook
committed in config
```

------------------------------------------------------------------------

# 44. Performance Philosophy

Sigma không optimize prematurely.

Flow:

``` text
Correctness
    ↓
Profile
    ↓
Identify Bottleneck
    ↓
Optimize
    ↓
Measure Again
```

Không dùng:

``` text
Distributed Infrastructure
```

để giải quyết một bottleneck chưa được đo.

------------------------------------------------------------------------

# 45. Technology Stack Success Criteria

Technology stack V1 được xem là đạt yêu cầu khi:

-   developer có thể setup environment reproducibly;
-   Core chạy độc lập với UI;
-   API có boundary rõ;
-   Classical Risk Engine không phụ thuộc Quantum;
-   Quantum research có simulator;
-   testing có unit/integration/evaluation layers;
-   documentation được version-control;
-   dependencies không bị phình do premature infrastructure;
-   stack có thể evolve khi workload thực sự thay đổi.

------------------------------------------------------------------------

# 46. Final Stack

``` text
                    SIGMA
                      │
             ┌────────┴────────┐
             │                 │
          CLIENT             API
          Taipy            FastAPI
             │                 │
             └────────┬────────┘
                      ▼
                 SIGMA CORE
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
     Data          Modeling        Risk
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                  Scenarios
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Classical                 Quantum
                               Qiskit
                               Aer
          │                       │
          └───────────┬───────────┘
                      ▼
                 Benchmark
                      │
                      ▼
               Risk Intelligence
```

Development foundation:

``` text
Python 3.12
    +
uv
    +
Git
    +
pytest
    +
Ruff
    +
Pyright
```

------------------------------------------------------------------------

# 47. Technology North Star

> **Sigma uses Python as the unified computational ecosystem, FastAPI as
> the stable product boundary, Taipy as a replaceable reference client,
> classical scientific libraries as the baseline, and Qiskit as a
> controlled computational enhancement layer.**

Không technology nào là product identity.

Product identity là:

``` text
Financial Risk Intelligence
```

Technology chỉ là phương tiện để xây dựng nó.

------------------------------------------------------------------------

# 48. Final Principle

``` text
Requirement
    ↓
Architecture
    ↓
Technology
    ↓
Implementation
    ↓
Measurement
```

Không:

``` text
Technology
    ↓
Find a problem for it
```

Và đặc biệt:

``` text
Quantum Technology
    ↓
Financial Problem
```

không phải hướng của Sigma.

Hướng đúng là:

``` text
Financial Problem
    ↓
Scientific Formulation
    ↓
Classical Baseline
    ↓
Quantum Where Justified
    ↓
Measured Value
    ↓
Product
```

→ **SIGMA TECHNOLOGY STACK**
