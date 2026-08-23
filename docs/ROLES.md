# Sigma --- Roles & Responsibilities

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Định nghĩa role, trách nhiệm, boundary và collaboration\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`ROLES.md` định nghĩa **vai trò chuyên môn** trong đội ngũ Sigma và phạm
vi trách nhiệm của từng role.

Tài liệu này bổ sung cho `TEAM.md`:

``` text
TEAM.md
→ Ai sở hữu domain nào và team phối hợp ra sao?

ROLES.md
→ Mỗi role tồn tại để làm gì và chịu trách nhiệm cụ thể ở đâu?
```

`ROLES.md` không phải organizational chart và không nhằm mô tả cấp bậc
nhân sự.

Một thành viên có thể đảm nhiệm nhiều role tùy quy mô và cách phân công
thực tế của team.

------------------------------------------------------------------------

# 2. Role Model

Sigma sử dụng mô hình:

``` text
Domain Ownership
        +
Clear Responsibility
        +
Cross-functional Review
```

Mỗi role có:

-   phạm vi trách nhiệm;
-   output chính;
-   boundary với role khác;
-   responsibility trong research/product lifecycle.

Không role nào được xem là hoàn toàn độc lập với các role còn lại.

------------------------------------------------------------------------

# 3. Role Overview

Sigma hiện có 6 role chính:

  -----------------------------------------------------------------------
  Role                                Trọng tâm
  ----------------------------------- -----------------------------------
  Team Lead / System & Quantum        System direction & research
  Research Lead                       direction

  Quantitative Finance & Risk         Financial meaning & risk
  Modelling                           methodology

  Data & Statistical Modeling         Data & statistical modeling
  Engineer                            

  Classical Risk Engine Engineer      Classical risk computation

  Quantum Computing Engineer          Quantum computation

  Backend, API & Product Integration  Product integration & system
                                      interface
  -----------------------------------------------------------------------

Có thể hình dung:

``` text
                    Sigma
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   Financial         Data          System
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              Classical Risk
                      │
                      ▼
                   Quantum
                      │
                      ▼
                Benchmark
                      │
                      ▼
              Backend / Product
```

------------------------------------------------------------------------

# 4. Team Lead / System & Quantum Research Lead

## 4.1. Mục đích của Role

Đảm bảo Sigma phát triển như **một hệ thống thống nhất**, đồng thời duy
trì research direction và Quantum strategy phù hợp với financial
problem.

Role này chịu trách nhiệm ở cấp system/research, không thay thế domain
expertise của các role chuyên môn.

------------------------------------------------------------------------

## 4.2. Trách nhiệm chính

### System

-   duy trì system-level technical direction;
-   bảo đảm các module tuân thủ architecture;
-   điều phối các technical boundary;
-   review các thay đổi ảnh hưởng đến toàn hệ thống;
-   giữ consistency giữa product, research và engineering.

### Research

-   định hướng research problem;
-   review research methodology;
-   điều phối Classical--Quantum research;
-   bảo đảm hypothesis và benchmark có scientific basis;
-   review scientific conclusion.

### Quantum Strategy

-   xác định nơi Quantum có thể được nghiên cứu;
-   bảo đảm Quantum không được đưa vào chỉ vì có thể sử dụng;
-   phối hợp với Quantitative Finance và Quantum Computing Engineer;
-   review các claim về Quantum advantage.

------------------------------------------------------------------------

## 4.3. Không sở hữu

Role này không tự động sở hữu:

-   toàn bộ financial modeling;
-   toàn bộ data engineering;
-   toàn bộ Classical Risk Engine;
-   toàn bộ Quantum implementation;
-   toàn bộ Backend.

Các domain này vẫn thuộc owner tương ứng.

------------------------------------------------------------------------

## 4.4. Output chính

``` text
System Direction
Research Direction
Architecture Decisions
Cross-module Decisions
Research Review
Quantum Strategy
```

------------------------------------------------------------------------

# 5. Quantitative Finance & Risk Modelling

## 5.1. Mục đích của Role

Đảm bảo Sigma giải quyết **đúng financial problem** và các risk
quantities có financial/statistical meaning rõ ràng.

Đây là role sở hữu financial interpretation của hệ thống.

------------------------------------------------------------------------

## 5.2. Trách nhiệm chính

-   financial problem formulation;
-   portfolio risk formulation;
-   return/loss convention;
-   risk horizon;
-   confidence level;
-   VaR;
-   CVaR / Expected Shortfall;
-   risk assumptions;
-   scenario assumptions;
-   financial interpretation của model output.

------------------------------------------------------------------------

## 5.3. Model Selection

Role này tham gia quyết định model dựa trên:

``` text
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

Không chọn model chỉ vì:

-   phổ biến;
-   dễ implement;
-   có sẵn trong library.

Các phương pháp như:

``` text
GARCH
HMM
Student-t
Monte Carlo
```

chỉ được sử dụng khi có justification phù hợp.

------------------------------------------------------------------------

## 5.4. Boundary

### Với Data & Statistical Modeling

``` text
Data Engineer
→ Data / Statistical Representation

Quant Finance
→ Financial Interpretation / Modeling Requirement
```

### Với Classical Risk

``` text
Quant Finance
→ What risk quantity means

Classical Risk
→ How it is computed
```

### Với Quantum

``` text
Quant Finance
→ Financial quantity / formulation

Quantum Engineer
→ Quantum implementation
```

------------------------------------------------------------------------

## 5.5. Output chính

``` text
Financial Formulation
Risk Definitions
Model Assumptions
Risk Methodology
Financial Interpretation
```

------------------------------------------------------------------------

# 6. Data & Statistical Modeling Engineer

## 6.1. Mục đích của Role

Đảm bảo dữ liệu và statistical modeling layer đủ chính xác, nhất quán và
có thể truy nguyên để phục vụ risk analysis.

------------------------------------------------------------------------

## 6.2. Trách nhiệm chính

### Data

-   market data ingestion;
-   validation;
-   cleaning;
-   transformation;
-   return calculation;
-   dataset provenance;
-   data quality checks.

### Statistical Modeling

-   volatility estimation;
-   regime modeling;
-   distribution fitting;
-   statistical diagnostics;
-   preparation của scenario inputs.

------------------------------------------------------------------------

## 6.3. Data Contract

Dữ liệu quan trọng phải có context phù hợp:

``` text
Source
Dataset Version
Time Range
Frequency
Adjustment Policy
Collection / Snapshot Information
```

Data phải được validation trước khi đi vào risk modeling.

------------------------------------------------------------------------

## 6.4. Boundary

Role này không sở hữu financial meaning của risk quantity.

Ví dụ:

``` text
Data Engineer
→ tính / chuẩn bị return series

Quant Finance
→ quyết định return convention phù hợp với methodology
```

------------------------------------------------------------------------

## 6.5. Output chính

``` text
Validated Market Data
Return Series
Volatility Inputs
Regime Outputs
Distribution Inputs
Dataset Metadata
Statistical Diagnostics
```

------------------------------------------------------------------------

# 7. Classical Risk Engine Engineer

## 7.1. Mục đích của Role

Xây dựng và duy trì **Classical Risk Engine** --- computational baseline
của Sigma.

Classical Risk Engine phải có khả năng hoạt động độc lập với Quantum
layer.

------------------------------------------------------------------------

## 7.2. Trách nhiệm chính

-   portfolio risk calculation;
-   scenario processing;
-   Monte Carlo engine;
-   loss distribution;
-   VaR;
-   CVaR;
-   risk contribution;
-   stress testing;
-   computational validation;
-   classical performance measurement.

------------------------------------------------------------------------

## 7.3. Pipeline Ownership

``` text
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

------------------------------------------------------------------------

## 7.4. Classical Baseline

Classical implementation phải đủ đáng tin cậy trước khi được dùng làm
benchmark cho Quantum.

Điều này bao gồm:

``` text
Financial Correctness
+
Tests
+
Validation
+
Reproducibility
```

------------------------------------------------------------------------

## 7.5. Boundary

Classical Risk Engine không:

-   định nghĩa financial semantics một mình;
-   phụ thuộc Quantum để chạy;
-   chứa API/UI logic.

------------------------------------------------------------------------

## 7.6. Output chính

``` text
Scenario Results
Loss Distribution
VaR
CVaR
Risk Contributions
Stress Results
Classical Benchmark Baseline
```

------------------------------------------------------------------------

# 8. Quantum Computing Engineer

## 8.1. Mục đích của Role

Thiết kế và triển khai Quantum computational layer cho những phần của
Sigma đã có financial justification.

------------------------------------------------------------------------

## 8.2. Trách nhiệm chính

-   quantum formulation;
-   circuit design;
-   state preparation;
-   oracle construction;
-   amplitude estimation;
-   QAE experiments;
-   quantum simulation;
-   noisy simulation;
-   backend execution;
-   quantum resource measurement.

------------------------------------------------------------------------

## 8.3. Quantum Workflow

``` text
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

------------------------------------------------------------------------

## 8.4. Financial Boundary

Quantum Computing Engineer không tự quyết định financial semantics.

Ví dụ:

``` text
Quant Finance
→ P(Loss > Threshold) là quantity cần estimate

Quantum Engineer
→ thiết kế cách biểu diễn và estimate quantity đó bằng Quantum
```

------------------------------------------------------------------------

## 8.5. Benchmark Responsibility

Khi chạy Quantum benchmark, role này phải phối hợp để ghi nhận:

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

Không được chỉ báo cáo quantum output mà bỏ qua computational resources.

------------------------------------------------------------------------

## 8.6. Output chính

``` text
Quantum Formulation
Quantum Circuits
State Preparation
Oracle
QAE / Estimator
Simulation Results
Quantum Resource Metrics
Quantum Benchmark Results
```

------------------------------------------------------------------------

# 9. Backend, API & Product Integration

## 9.1. Mục đích của Role

Đưa các computational capabilities của Sigma thành một **product
interface có thể sử dụng và tích hợp**.

------------------------------------------------------------------------

## 9.2. Trách nhiệm chính

### Backend

-   application services;
-   workflow orchestration ở application level;
-   integration giữa các core modules;
-   error handling.

### API

-   FastAPI;
-   endpoint design;
-   request/response schemas;
-   validation;
-   serialization;
-   API documentation.

### Product Integration

-   kết nối UI với API;
-   product-facing workflows;
-   integration giữa risk results và presentation layer.

------------------------------------------------------------------------

## 9.3. Boundary

Architecture chính:

``` text
Taipy
  ↓
FastAPI
  ↓
Application
  ↓
Sigma Core
```

Không:

``` text
Taipy
  ↓
Direct Core Access
```

FastAPI không chứa:

``` text
VaR Algorithm
CVaR Algorithm
Monte Carlo Logic
Quantum Circuit Logic
```

Các computation này thuộc Core/domain modules.

------------------------------------------------------------------------

## 9.4. Output chính

``` text
API
Application Services
Integration Layer
Product Workflows
API Contracts
UI ↔ Backend Integration
```

------------------------------------------------------------------------

# 10. Role Interaction Matrix

  ---------------------------------------------------------------------------------
  Concern         Team Lead      Quant       Data   Classical    Quantum    Backend
                                                         Risk            
  -------------- ---------- ---------- ---------- ----------- ---------- ----------
  System              **P**          C          C           C          C          C
  Architecture                                                           

  Financial               A      **P**          C           C          C         \-
  Formulation                                                            

  Data Pipeline           C          C      **P**           C          C          C

  Statistical             C          C      **P**           C          C         \-
  Modeling                                                               

  Classical Risk          C          A          C       **P**          C          C

  Quantum Method          A          C          C           C      **P**          C

  Benchmark           **A**          C          C           P          P          C

  API                     A          C          C           C          C      **P**

  Product                 A          C          C           C          C      **P**
  Integration                                                            

  Architecture        **P**          C          C           C          C          C
  Review                                                                 
  ---------------------------------------------------------------------------------

Trong bảng:

``` text
P = Primary Owner
A = Accountable / Final Review
C = Collaborator
- = Không thuộc responsibility chính
```

Một concern có thể có nhiều collaborator nhưng chỉ nên có một primary
owner.

------------------------------------------------------------------------

# 11. Cross-Role Interfaces

## 11.1. Finance ↔ Data

``` text
Quant Finance
      ↕
Data & Statistical Modeling
```

Finance xác định requirement và financial interpretation.

Data/Statistical Modeling cung cấp data representation và statistical
outputs phù hợp.

------------------------------------------------------------------------

## 11.2. Finance ↔ Classical Risk

``` text
Quant Finance
      ↓
Risk Definition
      ↓
Classical Risk Engine
      ↓
Risk Estimate
```

------------------------------------------------------------------------

## 11.3. Classical Risk ↔ Quantum

``` text
Classical Risk
      ↓
Baseline
      ↓
Quantum
      ↓
Benchmark
```

Quantum không thay thế Classical baseline.

------------------------------------------------------------------------

## 11.4. Core ↔ Backend

``` text
Core
  ↓
Application
  ↓
FastAPI
```

Backend chịu trách nhiệm integration chứ không tái implement business
logic.

------------------------------------------------------------------------

# 12. Research Lifecycle Ownership

Sigma research workflow:

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
Resource Analysis
   ↓
Scientific Conclusion
   ↓
Product Evaluation
```

Ownership:

  Giai đoạn                  Primary Role
  -------------------------- ---------------------------------
  Problem                    Quant + Team Lead
  Hypothesis                 Team Lead + Quant
  Mathematical Formulation   Quant + relevant technical role
  Classical Baseline         Classical Risk
  Quantum Method             Quantum Computing
  Fair Benchmark             Team Lead + Classical + Quantum
  Resource Analysis          Quantum + Classical
  Scientific Conclusion      Team Lead + domain owners
  Product Evaluation         Backend / Product + Team Lead

------------------------------------------------------------------------

# 13. Decision Boundaries

## Financial Decision

Primary:

``` text
Quantitative Finance & Risk Modelling
```

Review:

``` text
Team Lead
```

------------------------------------------------------------------------

## Statistical/Data Decision

Primary:

``` text
Data & Statistical Modeling Engineer
```

Review:

``` text
Quantitative Finance
```

khi decision ảnh hưởng financial interpretation.

------------------------------------------------------------------------

## Classical Computational Decision

Primary:

``` text
Classical Risk Engine Engineer
```

Review:

``` text
Quantitative Finance
```

khi thay đổi risk methodology.

------------------------------------------------------------------------

## Quantum Computational Decision

Primary:

``` text
Quantum Computing Engineer
```

Review:

``` text
Quantitative Finance
+
Team Lead
```

------------------------------------------------------------------------

## API/Product Decision

Primary:

``` text
Backend, API & Product Integration
```

Review:

``` text
Team Lead
```

nếu thay đổi architecture hoặc contract quan trọng.

------------------------------------------------------------------------

# 14. What Roles Must Not Do

## Team Lead

Không trở thành bottleneck bằng cách tự làm mọi domain.

## Quant Finance

Không tự implement toàn bộ infrastructure/API.

## Data Engineer

Không tự thay đổi financial semantics mà không thống nhất với Quant.

## Classical Risk Engineer

Không coi Classical implementation là "ground truth" chỉ vì nó chạy
được.

## Quantum Engineer

Không claim Quantum advantage chỉ từ theoretical speedup hoặc
circuit-level result.

## Backend Engineer

Không đưa financial computation vào API layer chỉ để implementation
nhanh hơn.

------------------------------------------------------------------------

# 15. Collaboration Rules

Khi một thay đổi vượt qua boundary của một role:

``` text
Primary Owner
        +
Affected Owner
        +
Review
```

Ví dụ:

### Thay đổi loss convention

``` text
Quant
+
Classical Risk
+
Quantum
```

### Thay đổi market-data schema

``` text
Data
+
Quant
+
Affected Consumers
```

### Thay đổi API contract

``` text
Backend
+
Affected Core / UI Owners
```

### Thay đổi Quantum benchmark protocol

``` text
Quantum
+
Classical Risk
+
Quant
+
Team Lead
```

------------------------------------------------------------------------

# 16. Ownership vs Implementation

Ownership không có nghĩa:

> "Chỉ người này mới được sửa code."

Ownership nghĩa:

> "Người này chịu trách nhiệm chính để domain đó đúng, coherent và được
> review."

Thành viên khác có thể đóng góp code, review hoặc research vào domain
đó.

------------------------------------------------------------------------

# 17. Role Evolution

Role có thể mở rộng hoặc thu hẹp theo giai đoạn phát triển.

Ví dụ một thành viên có thể đồng thời đảm nhiệm:

``` text
Data
+
Statistical Modeling
```

hoặc:

``` text
Backend
+
Product Integration
```

Điều này không phá vỡ role model miễn là ownership vẫn rõ.

Role mới chỉ nên được tạo khi có:

``` text
New Responsibility
+
Sustained Workload
+
Clear Ownership Need
```

------------------------------------------------------------------------

# 18. Definition of Done by Role

## Team Lead

``` text
Direction clear
Architecture coherent
Research claim reviewed
```

## Quant Finance

``` text
Financial formulation explicit
Assumptions explicit
Risk interpretation validated
```

## Data / Statistical Modeling

``` text
Data validated
Model inputs reproducible
Statistical assumptions documented
```

## Classical Risk

``` text
Calculation correct
Tests pass
Baseline reproducible
```

## Quantum

``` text
Quantum formulation explicit
Resources measured
Benchmark reproducible
```

## Backend / Product

``` text
API contract clear
Integration tested
Product workflow functional
```

------------------------------------------------------------------------

# 19. Role North Star

Các role không tồn tại để tối ưu từng module riêng lẻ.

Mục tiêu chung là:

``` text
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

------------------------------------------------------------------------

# 20. Final Principle

> **Clear ownership, shared responsibility for system integrity.**

Mỗi role phải biết:

``` text
What I own
What I contribute to
What I must review
What I must not decide alone
```

Và toàn đội phải cùng giữ một nguyên tắc:

``` text
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

------------------------------------------------------------------------

# 21. Final Role Map

``` text
                         SIGMA
                           │
             ┌─────────────┴─────────────┐
             │                           │
       SYSTEM / RESEARCH            FINANCIAL DOMAIN
             │                           │
       Team Lead                  Quant Finance
             │                           │
             └─────────────┬─────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
            DATA                    CLASSICAL RISK
              │                         │
              └────────────┬────────────┘
                           ▼
                        QUANTUM
                           │
                           ▼
                       BENCHMARK
                           │
                           ▼
                  BACKEND / PRODUCT
                           │
                           ▼
                 RISK INTELLIGENCE
```

> **Mỗi role có một trách nhiệm rõ ràng. Tất cả role cùng chịu trách
> nhiệm cho sự đúng đắn của Sigma.**
