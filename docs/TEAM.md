# Sigma --- Team & Responsibilities

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Team structure, ownership và responsibility\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`TEAM.md` định nghĩa cấu trúc vai trò và phạm vi trách nhiệm của đội ngũ
phát triển Sigma.

Tài liệu này nhằm:

-   làm rõ ownership của từng mảng;
-   tránh chồng chéo trách nhiệm;
-   xác định các technical/research responsibilities chính;
-   tạo cơ sở cho collaboration và review;
-   bảo đảm các thành phần quan trọng của Sigma đều có người phụ trách.

`TEAM.md` mô tả **role và responsibility**, không phải đánh giá năng lực
cá nhân hay chức danh tổ chức chính thức.

------------------------------------------------------------------------

# 2. Team Structure

Theo phân công hiện tại của đội, các role chính gồm:

``` text
Team Lead / System & Quantum Research Lead
Quantitative Finance & Risk Modelling
Data & Statistical Modeling Engineer
Classical Risk Engine Engineer
Quantum Computing Engineer
Backend, API & Product Integration
```

Đây là một team structure theo **responsibility**, không nhất thiết
tương ứng với số lượng thành viên.

Một thành viên có thể đảm nhiệm nhiều role nếu quy mô team yêu cầu.

------------------------------------------------------------------------

# 3. Team Leadership

## 3.1. Team Lead / System & Quantum Research Lead

**Người phụ trách:** Julius

### Phạm vi

-   Team leadership;
-   system-level direction;
-   research direction;
-   quantum research direction;
-   architectural coordination;
-   technical decision making.

### Trách nhiệm chính

``` text
Product / Research Direction
        ↓
System Architecture
        ↓
Technical Coordination
        ↓
Research Validation
        ↓
Final Integration
```

Cụ thể:

-   duy trì technical vision của Sigma;
-   bảo đảm các module đi đúng architecture;
-   điều phối Classical và Quantum research;
-   review các quyết định quan trọng về methodology;
-   bảo đảm Quantum được sử dụng đúng financial problem;
-   điều phối benchmark và scientific conclusion;
-   review các thay đổi ảnh hưởng đến architecture hoặc research
    direction;
-   giữ consistency giữa PRD, Design, Architecture, Schema, Rules và
    implementation.

### Decision Scope

Team Lead có responsibility cao nhất đối với các quyết định ảnh hưởng
tới:

``` text
System Architecture
Research Direction
Quantum Strategy
Cross-module Integration
```

Các quyết định chuyên môn sâu vẫn cần được trao đổi với owner của domain
tương ứng.

------------------------------------------------------------------------

# 4. Quantitative Finance & Risk Modelling

**Người phụ trách:** Nguyễn Minh Ngọc

## Scope

Role này chịu trách nhiệm về **financial meaning và risk methodology**
của Sigma.

### Trách nhiệm chính

-   định nghĩa financial problem;
-   xác định risk quantities;
-   portfolio risk formulation;
-   return/loss conventions;
-   risk horizon;
-   confidence level;
-   VaR;
-   CVaR / Expected Shortfall;
-   scenario/risk assumptions;
-   financial interpretation của model output.

### Ownership

``` text
Financial Problem
        ↓
Risk Formulation
        ↓
Model Assumptions
        ↓
Risk Interpretation
```

### Nguyên tắc

Role này không chỉ chọn model vì model phổ biến.

Mọi methodology phải có financial/statistical justification.

Ví dụ:

``` text
GARCH
HMM
Student-t
Monte Carlo
```

chỉ được sử dụng khi phù hợp với problem và data.

### Collaboration

Làm việc chặt với:

``` text
Data & Statistical Modeling
Classical Risk Engine
Quantum Computing
Team Lead
```

------------------------------------------------------------------------

# 5. Data & Statistical Modeling Engineer

**Người phụ trách:** Lương Minh Quân 

## Scope

Role này chịu trách nhiệm về data pipeline và statistical modeling
layer.

### Trách nhiệm chính

-   market data ingestion;
-   data validation;
-   data cleaning;
-   return calculation;
-   volatility estimation;
-   regime modeling;
-   distribution fitting;
-   statistical diagnostics;
-   dataset provenance;
-   reproducibility của data/modeling pipeline.

### Data Flow

``` text
Market Data
    ↓
Validation
    ↓
Cleaning / Transformation
    ↓
Returns
    ↓
Volatility / Regime
    ↓
Distribution
    ↓
Scenario Inputs
```

### Ownership

Đảm bảo các dữ liệu đưa vào Risk Engine có:

``` text
Correct Identity
Correct Time Ordering
Correct Frequency
Correct Return Convention
Clear Provenance
```

### Collaboration

Làm việc với:

``` text
Quantitative Finance & Risk Modelling
Classical Risk Engine
Quantum Computing
```

đặc biệt tại boundary giữa:

``` text
Financial Data
        ↔
Risk Model
```

------------------------------------------------------------------------

# 6. Classical Risk Engine Engineer

**Người phụ trách:** Nguyễn Việt Phương

## Scope

Role này chịu trách nhiệm xây dựng **classical computational baseline**
của Sigma.

### Trách nhiệm chính

-   portfolio risk calculation;
-   Monte Carlo engine;
-   scenario processing;
-   loss distribution;
-   VaR;
-   CVaR;
-   risk contribution;
-   stress testing;
-   computational validation;
-   classical performance measurement.

### Pipeline

``` text
Portfolio
    +
Market / Model Inputs
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

### Critical Responsibility

Classical Risk Engine phải:

-   độc lập với Quantum;
-   có test coverage phù hợp;
-   có financial correctness;
-   làm baseline cho Quantum benchmark.

Không được benchmark Quantum dựa trên một Classical baseline chưa được
kiểm chứng.

------------------------------------------------------------------------

# 7. Quantum Computing Engineer

**Người phụ trách:** Hoàng Ngọc Tuấn 

## Scope

Role này chịu trách nhiệm về Quantum computational layer của Sigma.

### Trách nhiệm chính

-   quantum formulation;
-   quantum circuit design;
-   state preparation;
-   oracle construction;
-   amplitude estimation;
-   QAE experiments;
-   quantum simulation;
-   noise-aware evaluation;
-   quantum resource measurement.

### Pipeline

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
Post-processing
        ↓
Risk Estimate
```

### Resource Ownership

Khi phù hợp, phải theo dõi:

``` text
Qubit Count
Circuit Depth
Gate Count
Shots
Oracle Queries
Runtime
Noise Model
Backend
```

### Critical Rule

Quantum Computing Engineer không tự định nghĩa financial meaning của
risk quantity.

Financial formulation thuộc:

``` text
Quantitative Finance & Risk Modelling
```

Quantum layer chịu trách nhiệm biểu diễn và ước lượng computational
problem một cách đúng đắn.

------------------------------------------------------------------------

# 8. Backend, API & Product Integration

**Người phụ trách:** Trần Thành

## Scope

Role này chịu trách nhiệm biến các computational capabilities thành
product interface.

### Trách nhiệm chính

-   FastAPI;
-   API contracts;
-   request/response models;
-   application services;
-   integration;
-   error handling;
-   product-facing workflows;
-   kết nối UI với backend;
-   integration giữa các engine.

### Architecture

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
   ├── Risk
   └── Quantum
```

### Critical Boundary

Backend/API không được trở thành nơi chứa financial computation.

FastAPI chịu trách nhiệm:

``` text
Routing
Validation
Serialization
Integration
```

Core chịu trách nhiệm:

``` text
Financial Computation
Risk Logic
Quantum Logic
```

------------------------------------------------------------------------

# 9. Cross-Functional Ownership

Sigma có các boundary cần collaboration giữa nhiều role.

## 9.1. Data → Risk

``` text
Data & Statistical Modeling
        ↓
Quantitative Finance
        ↓
Classical Risk Engine
```

Mục tiêu:

-   data đúng;
-   financial interpretation đúng;
-   calculation đúng.

------------------------------------------------------------------------

## 9.2. Risk → Quantum

``` text
Quantitative Finance
        ↓
Classical Risk Engine
        ↓
Quantum Computing
```

Quantum implementation chỉ bắt đầu sau khi target financial quantity và
Classical formulation đủ rõ.

------------------------------------------------------------------------

## 9.3. Core → Product

``` text
Core
  ↓
Application
  ↓
FastAPI
  ↓
Taipy
```

Product integration không được bypass architecture để gọi internal
computation trực tiếp.

------------------------------------------------------------------------

# 10. Decision Ownership

  -----------------------------------------------------------------------
  Area                    Primary Owner           Collaboration
  ----------------------- ----------------------- -----------------------
  System Architecture     Team Lead / System &    All technical roles
                          Quantum Research Lead   

  Research Direction      Team Lead / System &    Quant + Quantum
                          Quantum Research Lead   

  Financial Formulation   Quantitative Finance &  Team Lead
                          Risk Modelling          

  Market Data             Data & Statistical      Quant
                          Modeling Engineer       

  Statistical Modeling    Data & Statistical      Quant
                          Modeling Engineer       

  Classical Risk          Classical Risk Engine   Quant
                          Engineer                

  Quantum Method          Quantum Computing       Quant + Team Lead
                          Engineer                

  API                     Backend, API & Product  Core owners
                          Integration             

  Product Integration     Backend, API & Product  Team
                          Integration             

  Cross-module            Team Lead               Relevant owners
  Integration                                     
  -----------------------------------------------------------------------

Bảng này là **ownership**, không có nghĩa một role được phép tự quyết
mọi vấn đề liên quan mà không review.

------------------------------------------------------------------------

# 11. Research Workflow Ownership

Research flow của Sigma:

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

Phân công chính:

``` text
Problem / Risk Formulation
    → Quantitative Finance

Data / Statistical Formulation
    → Data & Statistical Modeling

Classical Baseline
    → Classical Risk Engine

Quantum Method
    → Quantum Computing

Benchmark / Research Direction
    → Team Lead + relevant owners

Productization
    → Backend / API / Product Integration
```

------------------------------------------------------------------------

# 12. Review Responsibilities

Mọi thay đổi quan trọng nên được review bởi owner của concern tương ứng.

Ví dụ:

### Financial methodology change

``` text
Quantitative Finance
+
Team Lead
```

### Data/modeling change

``` text
Data & Statistical Modeling
+
Quantitative Finance
```

### Classical risk change

``` text
Classical Risk Engine
+
Quantitative Finance
```

### Quantum algorithm change

``` text
Quantum Computing
+
Quantitative Finance
+
Team Lead
```

### API/architecture change

``` text
Backend / API
+
Team Lead
```

------------------------------------------------------------------------

# 13. No Single-Person Black Box

Không để một critical component chỉ có một người hiểu hoàn toàn.

Các component quan trọng nên có:

``` text
Primary Owner
+
At least one Reviewer / Collaborator
```

Đặc biệt với:

-   risk methodology;
-   Classical Risk Engine;
-   Quantum formulation;
-   API contracts;
-   system architecture.

Mục tiêu là giảm knowledge silo và tăng khả năng review.

------------------------------------------------------------------------

# 14. Team Collaboration Model

Sigma sử dụng mô hình:

``` text
Domain Ownership
        +
Cross-functional Review
```

Không sử dụng:

``` text
Everyone changes everything
```

và cũng không sử dụng:

``` text
Each person works in isolation
```

Mỗi người có ownership rõ nhưng các boundary quan trọng phải được review
chéo.

------------------------------------------------------------------------

# 15. Communication Principle

Khi có technical disagreement, ưu tiên:

``` text
Requirement
→ Evidence
→ Experiment
→ Measurement
→ Decision
```

Không quyết định chỉ dựa trên:

``` text
Preference
Popularity
Authority
```

Đặc biệt với research/Quantum:

> **Benchmark và evidence quan trọng hơn narrative.**

------------------------------------------------------------------------

# 16. Role Boundaries

Các role được phân biệt để tránh overlap:

``` text
Quantitative Finance
→ What financial quantity means

Data / Statistical Modeling
→ How data is prepared and statistically modeled

Classical Risk Engine
→ How risk is computationally estimated classically

Quantum Computing
→ How selected computational problems are implemented quantumly

Backend / Product Integration
→ How capabilities become a usable product

Team Lead / System & Quantum Research Lead
→ How the whole system and research direction remain coherent
```

------------------------------------------------------------------------

# 17. Team North Star

Mục tiêu của team không phải:

``` text
Build as much technology as possible
```

mà là:

``` text
Financial Problem
        ↓
Correct Data
        ↓
Sound Modeling
        ↓
Reliable Classical Risk
        ↓
Justified Quantum Enhancement
        ↓
Fair Benchmark
        ↓
Useful Risk Intelligence
        ↓
Product
```

Mỗi role đóng góp vào một đoạn khác nhau của cùng một pipeline.

------------------------------------------------------------------------

# 18. Definition of Good Collaboration

Một collaboration tốt khi:

-   responsibility rõ;
-   interface rõ;
-   assumptions được nói ra;
-   financial meaning thống nhất;
-   technical decisions có evidence;
-   research result có thể reproduce;
-   thay đổi một module không tùy tiện phá module khác.

------------------------------------------------------------------------

# 19. Team Evolution

Team structure có thể thay đổi khi Sigma phát triển.

V1 ưu tiên:

``` text
Small Team
+
Clear Ownership
+
Strong Cross-functional Collaboration
```

Không tạo thêm role chỉ vì organization chart đẹp hơn.

Role mới chỉ nên xuất hiện khi có:

``` text
New Responsibility
+
Sustained Workload
+
Clear Ownership Need
```

------------------------------------------------------------------------

# 20. Final Team Principle

> **Mỗi người sở hữu một domain, nhưng Sigma là một hệ thống thống
> nhất.**

Không có:

``` text
Finance team
vs
Engineering team
vs
Quantum team
```

mà là:

``` text
Finance
   ×
Data
   ×
Classical Risk
   ×
Quantum
   ×
Backend / Product
```

cùng xây dựng một Risk Intelligence system.

------------------------------------------------------------------------

# 21. Team North Star

``` text
                 SIGMA TEAM
                      │
       ┌──────────────┼──────────────┐
       │              │              │
   FINANCE          DATA          SYSTEM
       │              │              │
       ▼              ▼              ▼
 Risk Meaning    Statistical      Architecture
       │          Modeling            │
       └──────────────┬───────────────┘
                      ▼
               CLASSICAL RISK
                      │
                      ▼
                  QUANTUM
                      │
                      ▼
                 BENCHMARK
                      │
                      ▼
                PRODUCT/API
                      │
                      ▼
             RISK INTELLIGENCE
```

> **Build together. Own clearly. Validate scientifically. Ship
> responsibly.**
