# Sigma — Công nghệ Sử dụng

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Phạm vi:** Runtime, API, UI, Data, Modeling, Quantum, Testing và Development Tooling  
**Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

`TECH_STACK.md` định nghĩa công nghệ Sigma V1 sử dụng, vai trò của từng công nghệ và boundary của chúng.

Tài liệu trả lời:

- Sigma dùng runtime và công cụ phát triển nào?
- API và UI sử dụng gì?
- Financial / statistical computation dùng ecosystem nào?
- Quantum layer dùng gì?
- Công nghệ nào là bắt buộc, optional hoặc chưa cần?
- Vì sao một số công nghệ chưa được đưa vào V1?

`TECH_STACK.md` không thay thế:

```text
ARCHITECTURE.md → System Structure
SCHEMA.md       → Data Meaning
RULES.md        → Constraints
```

---

# 2. Nguyên tắc lựa chọn công nghệ

Technology selection đi theo:

```text
Financial Requirement
      ↓
Architectural Requirement
      ↓
Technical Requirement
      ↓
Technology Selection
```

Không chọn technology chỉ vì:

- phổ biến;
- nhiều stars;
- có “enterprise” branding;
- có quantum branding;
- làm architecture trông phức tạp hơn.

> **Dùng công nghệ đơn giản nhất đáp ứng đúng requirement thực tế.**

---

# 3. V1 Technology Overview

| Layer | Technology | Vai trò |
|---|---|---|
| Runtime | Python 3.12.x | Runtime chính |
| Environment / Dependencies | `uv` | Python, virtual environment, dependencies, lockfile |
| API | FastAPI | Product API |
| API Server | Uvicorn | ASGI server |
| UI | Taipy | Reference client V1 |
| Numerical | NumPy | Numerical primitives |
| Data | pandas | Tabular / time-series data |
| Scientific | SciPy | Statistical / numerical methods |
| Statistical Modeling | statsmodels | Classical statistical models khi phù hợp |
| ML | scikit-learn | Classical ML / evaluation khi cần |
| Visualization | Plotly | Interactive analytical charts |
| Quantum | Qiskit | Quantum circuits / algorithms |
| Quantum Simulation | Qiskit Aer | Local / noisy simulation |
| Testing | pytest | Unit / integration / evaluation |
| Formatting / Linting | Ruff | Code formatting và linting |
| Type Checking | Pyright | Static type checking |
| Documentation | Markdown + Mermaid | Project documentation |
| Version Control | Git | Source control |

Package versions cụ thể phải được quản lý trong `pyproject.toml` và lockfile. Bảng này mô tả **vai trò**, không thay thế dependency configuration.

---

# 4. Python Runtime

## 4.1. Python 3.12

Sigma V1 sử dụng:

```text
Python 3.12.x
```

Python là runtime chung cho:

```text
Core
Data
Modeling
Risk
Quantum
FastAPI
Taipy
Research
```

Lý do chính là Python cung cấp một ecosystem thống nhất cho:

```text
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

## 4.2. Version Policy

Project phải pin version phù hợp với development environment, ví dụ qua:

```text
.python-version
```

Không upgrade Python giữa chừng chỉ vì có version mới.

Runtime upgrade phải được xem như một thay đổi dependency và cần verification.

---

# 5. Package & Environment — uv

Sigma sử dụng:

```text
uv
```

cho:

- Python version management;
- virtual environment;
- dependency management;
- lockfile;
- reproducible development environment.

Workflow chính:

```text
uv python
uv venv
uv add
uv sync
uv run
```

Dependency phải được quản lý qua project configuration và lockfile thay vì cài thủ công ngoài environment.

---

# 6. API Stack

## 6.1. FastAPI

FastAPI là product API boundary:

```text
Client
  ↓ HTTP
FastAPI
  ↓
Application
  ↓
Sigma Core
```

FastAPI chịu trách nhiệm:

- routing;
- request / response;
- validation;
- serialization;
- API documentation;
- dependency wiring.

FastAPI không chịu trách nhiệm:

```text
VaR / CVaR
Monte Carlo
Regime Modeling
QAE Logic
```

Financial computation thuộc Core.

## 6.2. Uvicorn

Uvicorn là ASGI server cho FastAPI.

Development có thể chạy:

```text
uv run uvicorn sigma.api.main:app --reload
```

Deployment configuration có thể thay đổi theo environment.

---

# 7. UI — Taipy

Taipy là **reference client V1**:

```text
Taipy
  ↓ HTTP
FastAPI
  ↓
Sigma Core
```

Taipy chịu trách nhiệm:

- dashboard;
- portfolio interaction;
- risk visualization;
- scenario exploration;
- stress testing interface;
- quantum benchmark presentation.

Taipy không chứa:

```text
Financial Business Logic
Risk Engine
Quantum Engine
```

### Vì sao Taipy?

Taipy phù hợp với V1 vì:

- Python-native;
- phù hợp với data / analytics application;
- xây interactive UI nhanh;
- phù hợp cho prototype và product interface;
- giao tiếp được với FastAPI qua HTTP.

> **Taipy là client, không phải Sigma Core.**

Nếu thay Taipy trong tương lai, Core và API contract không nên phải viết lại.

---

# 8. Data & Numerical Stack

## NumPy

Dùng cho:

- arrays;
- vectorized computation;
- numerical operations;
- numerical representation.

## pandas

Dùng cho:

- market data;
- time series;
- preprocessing;
- dataset inspection;
- return calculation;
- data transformation.

Luồng cơ bản:

```text
Market Data
    ↓
pandas
    ↓
Validated Time Series
```

pandas không phải financial domain model. Core domain objects không nên phụ thuộc vào DataFrame representation nếu không cần.

## SciPy

Dùng khi methodology cần:

- statistical distributions;
- numerical optimization;
- numerical routines;
- statistical computation.

Chỉ sử dụng phần phù hợp với methodology.

---

# 9. Statistical & Financial Modeling

## statsmodels

`statsmodels` là lựa chọn cho classical statistical modeling khi cần, chẳng hạn:

- statistical estimation;
- time-series models;
- econometric analysis.

Không mặc định mọi volatility hoặc regime model đều phải dùng `statsmodels`.

## Volatility / GARCH

Nếu Sigma sử dụng GARCH hoặc volatility methodology khác, package phải được chọn dựa trên:

```text
Model Correctness
API Stability
Compatibility
Testing
Reproducibility
```

Không chọn package chỉ vì tiện import.

---

# 10. Machine Learning — scikit-learn

`scikit-learn` được dùng khi Sigma cần:

- baseline models;
- preprocessing;
- evaluation;
- clustering / classification / regression;
- model comparison.

ML không phải core identity của Sigma V1.

> ML chỉ được thêm khi có financial/statistical justification.

---

# 11. Visualization — Plotly

Plotly dùng cho interactive analytical visualization.

Các use case chính:

```text
Loss Distribution
Risk Contribution
Scenario Analysis
Stress Comparison
Benchmark Comparison
```

Visualization phải phục vụ analysis.

Không thêm chart chỉ để dashboard có nhiều biểu đồ.

---

# 12. Quantum Stack

## 12.1. Qiskit

Qiskit là primary quantum SDK của Sigma V1.

Vai trò:

- quantum circuit construction;
- quantum algorithm implementation;
- state preparation;
- oracle implementation;
- amplitude estimation;
- measurement.

Quantum code thuộc:

```text
src/sigma/quantum/
```

Không lan sang:

```text
domain/
risk/
api/
ui/
```

nếu không có architectural reason.

## 12.2. Qiskit Aer

Qiskit Aer dùng cho local quantum simulation:

- ideal simulation;
- noisy simulation;
- circuit validation;
- algorithm debugging;
- benchmark experiments.

Simulator result phải được phân biệt với hardware result.

---

# 13. Quantum Hardware Boundary

V1 không khóa Sigma vào một quantum hardware provider.

```text
Quantum Method
      ↓
Quantum Backend
      ├── Simulator
      └── Hardware
```

Có thể benchmark:

```text
Ideal
Noisy Simulator
Hardware
```

mà không thay đổi financial problem formulation.

Hardware integration chỉ được thêm khi research hoặc product requirement cần.

---

# 14. Quantum Resource Measurement

Khi phù hợp, quantum benchmark phải có khả năng ghi nhận:

```text
Qubits
Circuit Depth
Gate Count
Shots
Oracle Queries
Runtime
Noise Model
Backend
```

Đây là benchmark evidence, không chỉ là debugging information.

---

# 15. Testing — pytest

`pytest` là testing framework chính.

```text
tests/
├── unit/
├── integration/
└── evaluation/
```

### Unit

Kiểm tra:

- domain behavior;
- numerical functions;
- risk calculations;
- quantum helper logic.

### Integration

Kiểm tra:

- application workflows;
- API;
- module interaction.

### Evaluation

Đánh giá:

- model behavior;
- Classical baseline;
- Quantum benchmark;
- accuracy;
- resource behavior.

---

# 16. Formatting & Linting — Ruff

Ruff là tool chính cho:

```text
Formatting
Linting
```

Mục tiêu:

- code style nhất quán;
- feedback nhanh;
- giảm toolchain fragmentation.

Không thêm formatter/linter khác nếu Ruff đã đáp ứng requirement.

---

# 17. Type Checking — Pyright

Pyright dùng cho static type checking.

Mục tiêu:

- phát hiện interface mismatch;
- làm rõ module contracts;
- tăng reliability;
- giảm runtime errors.

Type checking phải hỗ trợ architecture, không trở thành type ceremony không cần thiết.

---

# 18. Documentation — Markdown & Mermaid

Documentation sử dụng:

```text
Markdown
+
Mermaid
```

Mermaid phù hợp cho:

- architecture;
- data flow;
- dependency relationships;
- system context;
- workflow / sequence khi cần.

Ưu điểm:

```text
Version-controlled
Diffable
Editable
Reproducible
```

Không cần lưu architecture diagram chính dưới dạng image nếu Mermaid biểu diễn đủ rõ.

---

# 19. Version Control — Git

Git track:

```text
Source
Tests
Docs
Configurations
Research Experiment Definitions
```

Không commit:

```text
Secrets
Local Virtual Environments
Generated Caches
Large Unmanaged Datasets
Temporary Artifacts
```

---

# 20. Data Source Boundary

Data provider không trở thành core dependency.

```text
Data Source
    ↓
Data Adapter / Loader
    ↓
Sigma Data Contract
    ↓
Modeling
```

Mục tiêu là thay đổi provider mà không phải viết lại Risk Engine.

Data source cụ thể có thể thay đổi theo:

- availability;
- license;
- cost;
- data quality;
- project stage.

Sigma V1 không khóa vào một vendor dữ liệu duy nhất.

---

# 21. Configuration

Configuration dùng file-based configuration và environment variables khi phù hợp.

Ví dụ:

```text
configs/
├── default.yaml
└── benchmark.yaml
```

Environment variables dành cho:

```text
API Keys
Credentials
Environment-specific Configuration
```

Không commit secrets.

---

# 22. Dependency Categories

Dependencies nên được phân nhóm:

```text
Runtime
Development
Research
Optional
```

Ví dụ:

### Runtime

```text
fastapi
uvicorn
numpy
pandas
scipy
plotly
taipy
```

### Research / Quantum

```text
qiskit
qiskit-aer
```

### Development

```text
pytest
ruff
pyright
```

Không phải research dependency nào cũng trở thành production dependency.

---

# 23. Production vs Research Dependencies

Một dependency chỉ vào production runtime khi production code thực sự cần nó.

```text
research/
    ↓
experimental package
```

không có nghĩa:

```text
src/sigma/
    ↓
must depend on package
```

Mục tiêu là giữ production dependency footprint nhỏ.

---

# 24. Quy tắc thêm Dependency

Package mới chỉ nên được thêm khi có:

1. Requirement rõ.
2. Use case thực tế.
3. Compatibility với Python 3.12.
4. Compatibility với architecture.
5. Maintenance / quality chấp nhận được.
6. Không có giải pháp đơn giản hơn bằng dependency hiện có.

---

# 25. Dependency Locking

Flow:

```text
pyproject.toml
      ↓
uv lock
      ↓
uv.lock
      ↓
uv sync
```

Nếu project sử dụng lockfile cho reproducibility, `uv.lock` phải được commit.

---

# 26. Environment

Conceptual environments:

```text
Local Development
        ↓
Research / Experiment
        ↓
Demo
        ↓
Production
```

V1 có thể dùng cùng Python project với dependency groups/extras khi phù hợp thay vì tạo nhiều repository/environment phức tạp.

---

# 27. Local Development

Developer setup nên tối giản:

```text
Python
uv
Git
```

Sau đó:

```text
uv sync
```

và chạy application bằng `uv run`.

Không yêu cầu Docker để bắt đầu development nếu application không cần.

---

# 28. API Documentation

FastAPI cung cấp API schema/documentation tự động.

API contract phải phản ánh:

```text
Request
Response
Validation
Error
```

Không expose implementation internals không cần thiết.

---

# 29. Logging

Application logging phục vụ:

- debugging;
- failed computation;
- API errors;
- benchmark execution;
- important runtime events.

Không log:

```text
API Keys
Passwords
Sensitive Credentials
```

---

# 30. Observability

V1 chưa cần distributed observability stack.

Theo dõi trước:

```text
Application Errors
API Errors
Execution Time
Benchmark Metadata
Experiment Results
```

Nếu workload tăng và có evidence cần observability nâng cao, stack có thể mở rộng sau.

---

# 31. Deployment

V1 ưu tiên deployment đơn giản:

```text
Taipy Client
      ↓
FastAPI
      ↓
Sigma Core
      ↓
Data / Quantum Backend
```

Không mặc định cần:

```text
Kubernetes
Kafka
Service Mesh
Airflow
Prefect
```

chỉ để deployment trông “enterprise”.

---

# 32. Async / Background Computation

Nếu computation trở thành long-running, ví dụ:

```text
Risk Analysis
Quantum Benchmark
Large Scenario Generation
```

có thể bổ sung asynchronous execution.

V1 không mặc định xây job orchestration platform.

Quyết định phải dựa trên:

```text
Measured Runtime
User Experience
Concurrency
Workload
```

---

# 33. Technology Boundaries

```text
Taipy
  → UI

FastAPI
  → API

pandas
  → Data Manipulation

NumPy / SciPy
  → Numerical Computation

statsmodels / scikit-learn
  → Classical Statistical / ML Methods

Qiskit / Aer
  → Quantum Computation

pytest
  → Testing

Ruff
  → Formatting / Linting

Pyright
  → Type Checking

uv
  → Environment / Dependencies
```

Technology phải được sử dụng trong boundary phù hợp.

---

# 34. Công nghệ chưa cần trong V1

Các công nghệ sau **không phải default dependency**:

```text
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
Cloud-specific Orchestration
```

Điều này không có nghĩa Sigma không bao giờ sử dụng chúng.

Chỉ có nghĩa:

> **Hiện chưa có requirement đủ mạnh để đưa chúng vào V1.**

---

# 35. Chưa khóa Database

`SCHEMA.md` đã định nghĩa logical data model.

`TECH_STACK.md` không khóa physical database trước khi persistence requirements được xác định đầy đủ.

Database có thể được quyết định dựa trên:

```text
Persistence Requirements
Concurrency
Deployment
Data Volume
Query Patterns
```

---

# 36. Chưa cần MLOps Platform

Sigma V1 không phải ML platform.

Nếu model training/deployment trở thành production requirement lớn, có thể xem xét MLOps tooling.

Hiện tại:

```text
Research
    ↓
Experiment
    ↓
Evaluation
    ↓
Core
```

là đủ.

---

# 37. Chưa cần Workflow Orchestrator

V1 không cần orchestration platform chỉ để chạy:

```text
Data
  ↓
Modeling
  ↓
Scenario
  ↓
Risk
```

Application layer có thể điều phối workflow.

Chỉ đánh giá orchestration khi xuất hiện:

- scheduled pipelines;
- distributed jobs;
- data dependencies;
- retry-heavy workflows.

---

# 38. Technology Decision Matrix

| Requirement | Choice | Lý do |
|---|---|---|
| General runtime | Python 3.12 | Unified ecosystem |
| Dependency management | uv | Fast, reproducible |
| API | FastAPI | Clear API boundary |
| UI | Taipy | Python-native analytics UI |
| Numerical | NumPy | Core numerical primitives |
| Data | pandas | Financial time-series / data manipulation |
| Statistics | SciPy / statsmodels | Scientific / statistical methods |
| ML | scikit-learn | Classical ML baseline |
| Visualization | Plotly | Interactive analytical charts |
| Quantum | Qiskit | Quantum SDK |
| Simulation | Qiskit Aer | Local / noisy simulation |
| Testing | pytest | Python testing ecosystem |
| Lint / format | Ruff | Unified fast tooling |
| Type checking | Pyright | Static analysis |
| Docs | Markdown / Mermaid | Version-controlled documentation |
| VCS | Git | Collaboration / versioning |

---

# 39. Technology Evolution

Technology changes đi theo:

```text
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

```text
Newer
More Popular
More Enterprise
```

---

# 40. Upgrade Policy

Dependency upgrade quan trọng phải kiểm tra:

```text
Compatibility
Tests
Scientific Results
Benchmark Results
Performance
API Contracts
```

Đặc biệt với:

```text
NumPy
SciPy
pandas
Qiskit
Taipy
FastAPI
```

vì upgrade có thể ảnh hưởng behavior hoặc compatibility.

---

# 41. Reproducibility Stack

Reproducibility dựa trên:

```text
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

Không phải experiment nào cũng cần mọi field, nhưng experiment quan trọng phải có đủ context để tái lập.

---

# 42. Security

Secrets phải nằm ngoài source code.

API credentials:

```text
Environment Variables
```

Không:

```text
hard-coded in Python
hard-coded in notebook
committed in config
```

---

# 43. Performance Philosophy

Sigma không optimize prematurely.

```text
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

Không dùng distributed infrastructure để giải quyết bottleneck chưa được đo.

---

# 44. Technology Stack Success Criteria

Technology stack V1 đạt yêu cầu khi:

- developer setup environment reproducibly;
- Core chạy độc lập với UI;
- API có boundary rõ;
- Classical Risk Engine không phụ thuộc Quantum;
- Quantum research có simulator;
- testing có unit / integration / evaluation;
- documentation được version-control;
- dependency footprint không phình vì premature infrastructure;
- stack có thể evolve khi workload thực sự thay đổi.

---

# 45. Final Stack

```text
                         SIGMA
                           │
                 ┌─────────┴─────────┐
                 │                   │
               CLIENT               API
               Taipy              FastAPI
                 │                   │
                 └─────────┬─────────┘
                           ▼
                       SIGMA CORE
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
            Data        Modeling       Risk
              │            │            │
              └────────────┼────────────┘
                           ▼
                       Scenarios
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             Classical            Quantum
                                  Qiskit
                                  Aer
                 │                   │
                 └─────────┬─────────┘
                           ▼
                       Benchmark
                           │
                           ▼
                    Risk Intelligence
```

Development foundation:

```text
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

---

# 46. Technology North Star

> **Sigma dùng Python làm computational ecosystem thống nhất, FastAPI làm product boundary ổn định, Taipy làm reference client có thể thay thế, classical scientific libraries làm baseline và Qiskit làm computational enhancement layer được kiểm soát.**

Không technology nào là product identity.

Product identity là:

```text
Financial Risk Intelligence
```

Technology chỉ là phương tiện để xây dựng nó.

---

# 47. Final Principle

```text
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

```text
Technology
    ↓
Find a problem for it
```

Đặc biệt:

```text
Quantum Technology
    ↓
Financial Problem
```

không phải hướng của Sigma.

Hướng đúng:

```text
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
