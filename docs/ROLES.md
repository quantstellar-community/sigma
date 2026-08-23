# Sigma — Vai trò & Trách nhiệm

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Phạm vi:** Vai trò, ownership, trách nhiệm và phối hợp  
**Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

`ROLES.md` định nghĩa các vai trò chuyên môn trong đội ngũ Sigma, phạm vi trách nhiệm và ranh giới quyết định của từng vai trò.

Tài liệu bổ sung cho `TEAM.md`:

```text
TEAM.md
→ Ai sở hữu domain nào và team phối hợp ra sao?

ROLES.md
→ Mỗi role chịu trách nhiệm gì, quyết định gì và phối hợp với ai?
```

`ROLES.md` không phải organizational chart và không mô tả cấp bậc.

Một thành viên có thể đảm nhiệm nhiều role nếu ownership vẫn rõ ràng.

---

## 2. Nguyên tắc ownership

Sigma sử dụng mô hình:

```text
Domain Ownership
        +
Clear Responsibility
        +
Cross-functional Review
```

Mỗi role phải biết:

- mình sở hữu gì;
- mình đóng góp vào đâu;
- thay đổi nào cần review;
- quyết định nào không được tự đưa ra.

**Ownership không có nghĩa chỉ một người được sửa code.**

Ownership nghĩa là người đó chịu trách nhiệm chính để domain của mình đúng, nhất quán và được review.

Một concern nên có **một Primary Owner**, nhưng có thể có nhiều collaborator.

---

## 3. Các role chính

| Role | Trọng tâm |
|---|---|
| Team Lead / System & Research | System direction, research direction và Quantum strategy |
| Quantitative Finance & Risk Modeling | Financial meaning và risk methodology |
| Data & Statistical Modeling | Market data và statistical modeling |
| Classical Risk Engine | Classical risk computation và baseline |
| Quantum Computing | Quantum computation và benchmark |
| Backend, API & Product Integration | Application, API và product integration |

Các role phối hợp theo chuỗi:

```text
Financial Problem
      ↓
Data / Statistical Modeling
      ↓
Classical Risk Engine
      ↓
Quantum Enhancement
      ↓
Benchmark
      ↓
Backend / Product
```

Đây là luồng trách nhiệm chính, không phải dependency bắt buộc giữa mọi role.

---

## 4. Team Lead / System & Research

### Mục đích

Đảm bảo Sigma phát triển như một hệ thống thống nhất, đồng thời giữ research direction và Quantum strategy phù hợp với financial problem.

Role này chịu trách nhiệm ở cấp system/research, không thay thế chuyên môn của các role khác.

### Trách nhiệm

**System**

- technical direction cấp hệ thống;
- architecture consistency;
- technical boundaries;
- review thay đổi ảnh hưởng nhiều module;
- consistency giữa product, research và engineering.

**Research**

- research problem;
- research methodology;
- Classical–Quantum research direction;
- hypothesis và benchmark protocol;
- scientific conclusion review.

**Quantum strategy**

- xác định nơi Quantum đáng được nghiên cứu;
- tránh đưa Quantum vào chỉ vì có thể sử dụng;
- review các claim về Quantum advantage.

### Không sở hữu riêng

- toàn bộ financial modeling;
- toàn bộ data engineering;
- Classical Risk Engine;
- Quantum implementation;
- Backend.

### Output chính

```text
System Direction
Research Direction
Architecture Decisions
Cross-module Decisions
Research Review
Quantum Strategy
```

---

## 5. Quantitative Finance & Risk Modeling

### Mục đích

Đảm bảo Sigma giải quyết **đúng financial problem** và các risk quantity có financial/statistical meaning rõ ràng.

Đây là role sở hữu financial interpretation của hệ thống.

### Trách nhiệm

- financial problem formulation;
- portfolio risk formulation;
- return/loss convention;
- risk horizon;
- confidence level;
- VaR;
- CVaR / Expected Shortfall;
- risk assumptions;
- scenario assumptions;
- financial interpretation của model output.

### Model Selection

Model được lựa chọn dựa trên:

```text
Financial Problem
       +
Data Characteristics
       +
Statistical Assumptions
       +
Interpretability
       +
Practical Utility
```

Không chọn model chỉ vì phổ biến hoặc dễ triển khai.

Các phương pháp như GARCH, HMM, Student-t và Monte Carlo chỉ được sử dụng khi có justification phù hợp.

### Ranh giới

```text
Quant Finance
→ What risk quantity means

Classical Risk
→ How it is computed
```

```text
Quant Finance
→ Financial quantity / formulation

Quantum Computing
→ Quantum implementation
```

### Output chính

```text
Financial Formulation
Risk Definitions
Model Assumptions
Risk Methodology
Financial Interpretation
```

---

## 6. Data & Statistical Modeling

### Mục đích

Đảm bảo dữ liệu và statistical modeling layer đủ chính xác, nhất quán và có thể truy nguyên để phục vụ risk analysis.

### Trách nhiệm

**Data**

- market data ingestion;
- validation;
- cleaning;
- transformation;
- return calculation;
- dataset provenance;
- data quality checks.

**Statistical Modeling**

- volatility estimation;
- regime modeling;
- distribution fitting;
- statistical diagnostics;
- chuẩn bị scenario inputs.

### Data Context

Dữ liệu quan trọng cần có:

```text
Source
Dataset Version
Time Range
Frequency
Adjustment Policy
Collection / Snapshot Information
```

Data phải được validation trước khi đi vào risk modeling.

### Ranh giới

Data/Statistical Modeling chịu trách nhiệm về data representation và statistical outputs.

Quant Finance chịu trách nhiệm về financial interpretation và methodology.

Ví dụ:

```text
Data / Statistical Modeling
→ chuẩn bị return series

Quant Finance
→ quyết định return convention phù hợp với methodology
```

### Output chính

```text
Validated Market Data
Return Series
Volatility Inputs
Regime Outputs
Distribution Inputs
Dataset Metadata
Statistical Diagnostics
```

---

## 7. Classical Risk Engine

### Mục đích

Xây dựng và duy trì **Classical Risk Engine** — computational baseline của Sigma.

Classical Risk Engine phải hoạt động độc lập với Quantum layer.

### Trách nhiệm

- portfolio risk calculation;
- scenario processing;
- Monte Carlo engine;
- loss distribution;
- VaR;
- CVaR;
- risk contribution;
- stress testing;
- computational validation;
- classical performance measurement.

### Pipeline

```text
Portfolio
    +
Model / Market Inputs
        ↓
Scenario Generation
        ↓
Portfolio P&L / Loss
        ↓
Loss Distribution
        ↓
VaR / CVaR
        ↓
Risk Intelligence
```

### Classical Baseline

Baseline phải đủ đáng tin cậy trước khi được dùng để benchmark Quantum:

```text
Financial Correctness
        +
Tests
        +
Validation
        +
Reproducibility
```

### Ranh giới

Classical Risk Engine không:

- tự định nghĩa financial semantics;
- phụ thuộc Quantum để chạy;
- chứa API/UI logic.

### Output chính

```text
Scenario Results
Loss Distribution
VaR
CVaR
Risk Contributions
Stress Results
Classical Benchmark Baseline
```

---

## 8. Quantum Computing

### Mục đích

Thiết kế và triển khai Quantum computational layer cho những phần của Sigma đã có financial justification.

### Trách nhiệm

- quantum formulation;
- circuit design;
- state preparation;
- oracle construction;
- amplitude estimation;
- QAE experiments;
- quantum simulation;
- noisy simulation;
- backend execution;
- quantum resource measurement.

### Workflow

```text
Financial Quantity
        ↓
Quantum Formulation
        ↓
State Preparation
        ↓
Oracle
        ↓
Quantum Estimation
        ↓
Measurement
        ↓
Post-processing
        ↓
Risk Estimate
```

### Financial boundary

Quantum Computing không tự quyết định financial semantics.

```text
Quant Finance
→ P(Loss > Threshold) là quantity cần estimate

Quantum Computing
→ thiết kế cách biểu diễn và estimate quantity đó bằng Quantum
```

### Benchmark responsibility

Khi chạy benchmark, cần ghi nhận:

- qubits;
- circuit depth;
- gate count;
- shots;
- oracle queries;
- runtime;
- noise model;
- backend.

Không chỉ báo cáo quantum output mà bỏ qua computational resources.

### Output chính

```text
Quantum Formulation
Quantum Circuits
State Preparation
Oracle
QAE / Estimator
Simulation Results
Quantum Resource Metrics
Quantum Benchmark Results
```

---

## 9. Backend, API & Product Integration

### Mục đích

Đưa computational capabilities của Sigma thành **product interface có thể sử dụng và tích hợp**.

### Trách nhiệm

**Backend**

- application services;
- application-level workflow orchestration;
- integration giữa core modules;
- error handling.

**API**

- FastAPI;
- endpoint design;
- request/response schemas;
- validation;
- serialization;
- API documentation.

**Product Integration**

- kết nối UI với API;
- product-facing workflows;
- kết nối risk results với presentation layer.

### Ranh giới

```text
Taipy
  ↓
FastAPI
  ↓
Application
  ↓
Sigma Core
```

Không:

```text
Taipy
  ↓
Direct Core Access
```

FastAPI không chứa:

```text
VaR Algorithm
CVaR Algorithm
Monte Carlo Logic
Quantum Circuit Logic
```

Các computation này thuộc Core/domain modules.

### Output chính

```text
API
Application Services
Integration Layer
Product Workflows
API Contracts
UI ↔ Backend Integration
```

---

## 10. Ma trận trách nhiệm

Trong bảng:

```text
P = Primary Owner
A = Accountable / Final Review
C = Collaborator
— = Không thuộc responsibility chính
```

| Concern | Team Lead | Quant | Data | Classical Risk | Quantum | Backend |
|---|---|---|---|---|---|---|
| System Architecture | **P** | C | C | C | C | C |
| Financial Formulation | A | **P** | C | C | C | — |
| Data Pipeline | C | C | **P** | C | C | C |
| Statistical Modeling | C | C | **P** | C | C | — |
| Classical Risk | C | A | C | **P** | C | C |
| Quantum Method | A | C | C | C | **P** | C |
| Benchmark | **A** | C | C | P | P | C |
| API | A | C | C | C | C | **P** |
| Product Integration | A | C | C | C | C | **P** |
| Architecture Review | **P** | C | C | C | C | C |

Nguyên tắc: một concern có thể có nhiều collaborator nhưng chỉ nên có một Primary Owner.

---

## 11. Ranh giới phối hợp

### Finance ↔ Data

```text
Quant Finance
      ↕
Data & Statistical Modeling
```

Finance xác định requirement và financial interpretation.

Data/Statistical Modeling cung cấp data representation và statistical outputs phù hợp.

### Finance ↔ Classical Risk

```text
Quant Finance
      ↓
Risk Definition
      ↓
Classical Risk Engine
      ↓
Risk Estimate
```

### Classical Risk ↔ Quantum

```text
Classical Risk
      ↓
Baseline
      ↓
Quantum
      ↓
Benchmark
```

Quantum không thay thế Classical baseline.

### Core ↔ Backend

```text
Core
 ↓
Application
 ↓
FastAPI
```

Backend chịu trách nhiệm integration, không tái triển khai business logic.

---

## 12. Research Lifecycle

Sigma research workflow:

```text
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
Resource Analysis
   ↓
Scientific Conclusion
   ↓
Product Evaluation
```

| Giai đoạn | Primary Role |
|---|---|
| Problem | Quant + Team Lead |
| Hypothesis | Team Lead + Quant |
| Mathematical Formulation | Quant + technical role liên quan |
| Classical Baseline | Classical Risk |
| Quantum Method | Quantum Computing |
| Fair Benchmark | Team Lead + Classical + Quantum |
| Resource Analysis | Quantum + Classical |
| Scientific Conclusion | Team Lead + domain owners |
| Product Evaluation | Backend / Product + Team Lead |

---

## 13. Ranh giới quyết định

### Financial Decision

**Primary:** Quantitative Finance & Risk Modeling  
**Review:** Team Lead

### Statistical / Data Decision

**Primary:** Data & Statistical Modeling  
**Review:** Quantitative Finance khi decision ảnh hưởng financial interpretation.

### Classical Computational Decision

**Primary:** Classical Risk Engine  
**Review:** Quantitative Finance khi thay đổi risk methodology.

### Quantum Computational Decision

**Primary:** Quantum Computing  
**Review:** Quantitative Finance + Team Lead

### API / Product Decision

**Primary:** Backend, API & Product Integration  
**Review:** Team Lead nếu thay đổi architecture hoặc contract quan trọng.

---

## 14. Những quyết định không được tự ý thực hiện

### Team Lead

Không trở thành bottleneck bằng cách tự làm mọi domain.

### Quantitative Finance

Không tự quyết định toàn bộ infrastructure hoặc API implementation.

### Data & Statistical Modeling

Không tự thay đổi financial semantics mà không thống nhất với Quant.

### Classical Risk Engine

Không coi Classical implementation là “ground truth” chỉ vì nó chạy được.

### Quantum Computing

Không claim Quantum advantage chỉ từ theoretical speedup hoặc circuit-level result.

### Backend / Product Integration

Không đưa financial computation vào API layer chỉ để implementation nhanh hơn.

---

## 15. Quy tắc phối hợp

Khi một thay đổi vượt qua boundary của một role:

```text
Primary Owner
      +
Affected Owner
      +
Review
```

Ví dụ:

**Thay đổi loss convention**

```text
Quant
  +
Classical Risk
  +
Quantum
```

**Thay đổi market-data schema**

```text
Data
  +
Quant
  +
Affected Consumers
```

**Thay đổi API contract**

```text
Backend
  +
Affected Core / UI Owners
```

**Thay đổi Quantum benchmark protocol**

```text
Quantum
  +
Classical Risk
  +
Quant
  +
Team Lead
```

---

## 16. Role Evolution

Một thành viên có thể đảm nhiệm nhiều role nếu ownership vẫn rõ.

Ví dụ:

```text
Data
  +
Statistical Modeling
```

hoặc:

```text
Backend
  +
Product Integration
```

Không cần tạo role mới chỉ vì một task mới xuất hiện.

Role mới chỉ nên được tạo khi có:

```text
New Responsibility
        +
Sustained Workload
        +
Clear Ownership Need
```

---

## 17. Definition of Done theo role

### Team Lead

```text
Direction clear
Architecture coherent
Research claim reviewed
```

### Quantitative Finance

```text
Financial formulation explicit
Assumptions explicit
Risk interpretation validated
```

### Data / Statistical Modeling

```text
Data validated
Model inputs reproducible
Statistical assumptions documented
```

### Classical Risk

```text
Calculation correct
Tests pass
Baseline reproducible
```

### Quantum

```text
Quantum formulation explicit
Resources measured
Benchmark reproducible
```

### Backend / Product

```text
API contract clear
Integration tested
Product workflow functional
```

---

## 18. Role North Star

Các role không tồn tại để tối ưu từng module riêng lẻ.

Mục tiêu chung:

```text
Correct Financial Problem
        ↓
Reliable Data
        ↓
Sound Statistical Modeling
        ↓
Reliable Classical Risk
        ↓
Justified Quantum Enhancement
        ↓
Fair Benchmark
        ↓
Usable Product
```

---

## 19. Final Principle

> **Clear ownership, shared responsibility for system integrity.**

Mỗi role phải biết:

```text
What I own
What I contribute to
What I must review
What I must not decide alone
```

Toàn đội cùng giữ:

```text
Financial Correctness
        +
Scientific Rigor
        +
Engineering Discipline
        +
Product Utility
        ↓
SIGMA
```
