# Sigma — Product Requirements Document

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Sản phẩm:** Sigma Risk Intelligence  
**Loại sản phẩm:** Regime-Aware Portfolio Risk Intelligence Engine  
**Lĩnh vực:** Market Risk & Portfolio Risk  
**Định hướng:** API-first, Modular Monolith

---

## 1. Mục đích

PRD định nghĩa **Sigma cần xây dựng gì, dành cho ai và tại sao sản phẩm cần tồn tại**.

Tài liệu là baseline cho:

- phạm vi sản phẩm;
- vấn đề cần giải quyết;
- người dùng mục tiêu;
- mục tiêu V1;
- yêu cầu chức năng;
- ranh giới sản phẩm;
- tiêu chí thành công;
- định hướng phát triển.

Chi tiết về UI/UX, kiến trúc, schema và công nghệ thuộc các tài liệu chuyên biệt.

---

## 2. Tổng quan sản phẩm

Sigma là **Regime-Aware Portfolio Risk Intelligence Engine**, biến dữ liệu thị trường và danh mục thành các đánh giá rủi ro định lượng:

```text
Market Data
    ↓
Risk Modeling
    ↓
Scenario Generation
    ↓
Loss Distribution
    ↓
Risk Estimation
    ↓
Risk Intelligence
    ↓
Decision Support
```

Sigma kết hợp phương pháp tài chính định lượng Classical với Quantum Computing ở những bài toán mà phương pháp lượng tử có vai trò tính toán rõ ràng.

Triết lý:

> **Classical First → Quantum Where Justified → Fair Benchmark → Measure Real Value → Risk Intelligence → Decision Support**

Sigma không giả định Quantum luôn vượt trội. Classical và Quantum phải được đánh giá trên cùng financial problem, với độ chính xác, chi phí tính toán và giá trị thực tế được đo lường rõ ràng.

---

## 3. Vấn đề cần giải quyết

### 3.1. Rủi ro thay đổi theo điều kiện thị trường

Phân phối lợi suất và mức độ biến động có thể thay đổi theo thời gian. Một risk analysis dựa trên distribution cố định có thể không phản ánh đầy đủ các market regime khác nhau.

Sigma hướng tới:

```text
Market State
    ↓
Return / Volatility Dynamics
    ↓
Risk Distribution
    ↓
Scenario Generation
    ↓
Portfolio Loss Distribution
    ↓
Risk Metrics
```

Mục tiêu là tạo risk analysis có xét đến bối cảnh thị trường, thay vì chỉ đưa ra một con số risk tách rời khỏi điều kiện tạo ra nó.

### 3.2. Chi phí tính toán của risk estimation

Monte Carlo là baseline quan trọng để ước lượng risk từ loss distribution. Một số phương pháp Quantum, đặc biệt Quantum Amplitude Estimation, có lợi thế lý thuyết về query complexity trong các bài toán phù hợp.

Tuy nhiên, lợi thế đó có thể bị ảnh hưởng bởi:

- state preparation;
- distribution loading;
- oracle construction;
- circuit depth;
- số qubit;
- shots;
- noise;
- runtime;
- chi phí toàn bộ pipeline.

Vì vậy, câu hỏi nghiên cứu của Sigma là:

> **Trong điều kiện nào lợi thế tính toán của Quantum còn tồn tại sau khi tính đến toàn bộ financial risk pipeline?**

---

## 4. Product Vision

### Vision

Xây dựng một nền tảng **Financial Risk Intelligence** có khả năng biến dữ liệu thị trường và thông tin danh mục thành đánh giá rủi ro định lượng, có khả năng giải thích và có thể tích hợp vào các hệ thống tài chính thông qua API.

### Định hướng

```text
Market Data
    ↓
Risk Modeling
    ↓
Scenario Generation
    ↓
Loss Distribution
    ↓
Risk Estimation
    ↓
Risk Intelligence
    ↓
Decision Support
```

Quantum là **computational enhancement layer**, không phải mục tiêu cuối cùng của sản phẩm.

### Định hướng dài hạn

Risk Analytics là nền tảng ban đầu. Sau khi V1 được kiểm chứng, Sigma có thể mở rộng sang:

- Portfolio Intelligence;
- Risk Contribution;
- Concentration Analysis;
- Portfolio Optimization;
- Credit Risk;
- Liquidity Risk;
- Dynamic Risk Management;
- các lớp Decision Intelligence rộng hơn.

Portfolio Management là lớp ứng dụng có thể phát triển phía trên Risk Engine, không phải lõi của Sigma V1.

---

## 5. Product Positioning

Sigma là **Risk Intelligence Engine, không phải Trading Bot**.

Sigma không nhằm:

- dự báo giá cổ phiếu;
- tự động giao dịch;
- thay thế Portfolio Manager;
- trở thành OMS/EMS;
- trở thành hệ thống Portfolio Management hoàn chỉnh.

Sigma tập trung vào câu hỏi:

> **Danh mục có thể chịu rủi ro như thế nào, trong những điều kiện nào, và mức độ bất định của kết quả là bao nhiêu?**

Sigma cung cấp risk intelligence để hỗ trợ quyết định, nhưng không tự động thực hiện quyết định đầu tư.

---

## 6. Người dùng mục tiêu

### Risk Analyst

Cần:

- portfolio risk;
- VaR/CVaR;
- loss distribution;
- risk contribution;
- stress testing;
- scenario analysis.

### Portfolio Manager

Cần:

- risk profile;
- tail risk drivers;
- portfolio response dưới các market scenarios;
- decision support.

### Quantitative Researcher / Risk Modeler

Cần:

- risk distributions;
- volatility/regime models;
- Monte Carlo;
- Quantum Amplitude Estimation;
- Classical–Quantum benchmarking.

### Financial Institutions

Định hướng dài hạn gồm:

- ngân hàng;
- công ty chứng khoán;
- công ty quản lý tài sản;
- fintech;
- các tổ chức tài chính có nhu cầu phân tích và quản trị rủi ro.

---

## 7. Các vấn đề người dùng

| Mã | Vấn đề |
|---|---|
| P1 | Định lượng rủi ro danh mục dưới các điều kiện thị trường khác nhau |
| P2 | Hiểu tail risk, Expected Shortfall và các tài sản đóng góp lớn |
| P3 | Mô hình hóa risk theo market regime thay vì distribution cố định |
| P4 | Phân tích scenario và stress |
| P5 | Đánh giá Classical và Quantum trên cùng financial problem |
| P6 | Tích hợp risk computation qua API |

---

## 8. Mục tiêu sản phẩm

### Goal 1 — Risk Analytics Core

Sigma phải có khả năng:

- xử lý market data;
- tính returns;
- mô hình hóa volatility;
- nhận diện market regime;
- xây dựng regime-aware distribution;
- sinh scenarios;
- tạo portfolio loss distribution;
- tính VaR;
- tính CVaR / Expected Shortfall;
- thực hiện stress testing.

### Goal 2 — Classical Baseline

Classical Monte Carlo là baseline để:

- kiểm chứng methodology;
- làm reference implementation;
- đánh giá accuracy;
- đối chứng với Quantum.

### Goal 3 — Quantum Enhancement

Nghiên cứu Quantum trên các financial estimation problem cụ thể, ưu tiên các bài toán phù hợp với Quantum Amplitude Estimation và các biến thể liên quan.

### Goal 4 — Fair Classical–Quantum Benchmark

Benchmark phải xem xét:

- accuracy;
- estimation error;
- samples / queries;
- runtime;
- qubits;
- circuit depth;
- shots;
- noise;
- state preparation cost;
- oracle cost;
- end-to-end computational cost.

### Goal 5 — Productize Risk Engine

Risk computation phải có API rõ ràng để có thể được sử dụng bởi dashboard, notebook, CLI và các client bên ngoài trong tương lai.

---

## 9. Nguyên tắc sản phẩm

### Classical First

Classical methods phải được xây dựng và kiểm chứng trước khi đưa Quantum vào.

### Quantum Where Justified

Mỗi Quantum component phải có:

- financial problem;
- mathematical formulation;
- computational motivation;
- classical baseline;
- benchmark protocol.

### Không giả định Quantum Advantage

Một kết quả hợp lệ có thể là:

```text
Quantum có lợi thế lý thuyết về query complexity
        ↓
State preparation chi phối chi phí
        ↓
Không có practical advantage ở cấp độ end-to-end
```

Đây vẫn là kết quả nghiên cứu có giá trị.

### Financial Validity First

Quantum result không có ý nghĩa nếu financial formulation hoặc risk methodology không hợp lệ.

### End-to-End Evaluation

Benchmark phải đánh giá toàn bộ computational pipeline, không chỉ một quantum circuit cô lập.

### Explainability

Risk output phải giúp người dùng hiểu:

- risk đến từ đâu;
- scenario nào tạo ra risk;
- tài sản nào đóng góp nhiều nhất;
- assumptions nào được sử dụng.

### API First

Risk Engine độc lập với UI. Taipy là reference client; API là product interface.

---

## 10. Phạm vi V1

Sigma V1 tập trung vào:

> **Regime-Aware Portfolio Risk Intelligence**

### Input

- historical market prices;
- portfolio positions / weights;
- portfolio value;
- confidence level;
- risk horizon;
- simulation parameters;
- scenario parameters.

### Data Processing

- data ingestion;
- validation;
- cleaning;
- adjusted price handling;
- return calculation;
- volatility estimation;
- covariance / correlation estimation.

### Market Modeling

- return modeling;
- conditional volatility modeling;
- market regime detection;
- regime-aware distribution modeling.

GARCH và HMM có thể được sử dụng khi phù hợp với financial/statistical assumptions.

### Scenario Generation

- Monte Carlo simulation;
- portfolio-level scenario generation;
- loss distribution;
- stress scenarios.

### Risk Metrics

- VaR;
- CVaR / Expected Shortfall;
- Expected Loss;
- volatility;
- simulated worst loss;
- probability of loss vượt threshold;
- risk contribution.

### Quantum Risk Estimation

V1 nghiên cứu:

- Quantum Amplitude Estimation;
- các biến thể phù hợp như Iterative / Maximum Likelihood Amplitude Estimation khi cần;
- quantum state preparation;
- risk / payoff oracle;
- quantum resource estimation.

Quantum module phải được benchmark với Classical baseline.

### Classical–Quantum Benchmark

Sigma phải so sánh Classical và Quantum trên cùng financial problem và cùng evaluation criteria.

### Stress Testing

V1 hỗ trợ:

- market shock;
- volatility shock;
- asset / sector shock;
- historical crisis scenarios;
- custom scenarios khi methodology phù hợp.

### API

API hỗ trợ các nhóm chức năng:

- portfolio analysis;
- risk estimation;
- scenario / stress analysis;
- Classical–Quantum benchmark.

### Dashboard

Taipy là:

- reference client;
- interactive risk console;
- visualization layer;
- benchmark interface;
- demonstration interface.

Dashboard không chứa financial business logic.

---

## 11. Luồng chính của V1

```text
Market Data
      ↓
Data Validation & Cleaning
      ↓
Returns / Risk Features
      ↓
Volatility Modeling
      ↓
Market Regime Modeling
      ↓
Regime-Aware Distribution
      ↓
Scenario Generation
      ↓
Portfolio Loss Distribution
      ↓
┌───────────────────────────┐
│ Classical Risk Estimation │
│            vs             │
│ Quantum Risk Estimation   │
└─────────────┬─────────────┘
              ↓
          VaR / CVaR
              ↓
        Stress Testing
              ↓
       Risk Intelligence
              ↓
       Decision Support
              ↓
        FastAPI / UI
```

Quantum là nhánh estimation/benchmark tùy trường hợp, không phải điều kiện bắt buộc của Classical risk workflow.

---

## 12. Product Outputs

### Risk Summary

- Portfolio Value;
- Volatility;
- VaR 95%;
- VaR 99%;
- CVaR 95%;
- CVaR 99%;
- Expected Loss.

### Risk Decomposition

- Asset Risk Contribution;
- Portfolio Concentration;
- Volatility Contribution;
- Covariance / Correlation;
- Top Risk Drivers.

### Scenario & Stress

- Portfolio Loss;
- Loss Distribution;
- Tail Loss;
- Stress Loss;
- VaR Change;
- CVaR Change;
- Worst Scenarios.

### Classical–Quantum Benchmark

- estimator;
- estimate;
- absolute error;
- relative error;
- runtime;
- samples / queries;
- qubits;
- circuit depth;
- shots;
- noise setting;
- state preparation cost;
- oracle cost.

Kết luận benchmark phải phản ánh kết quả thực nghiệm, không mặc định Quantum thắng.

---

## 13. Quantum Research Scope

Quantum trong V1 là computational layer cho các estimation problem đã có financial formulation.

Quantum không xử lý:

- raw data cleaning;
- market data ingestion;
- toàn bộ portfolio pipeline;
- financial preprocessing;
- API orchestration.

Quantum nhận một bài toán đã được chuẩn hóa, ví dụ:

```text
P(Loss > Threshold)
```

hoặc một expected value / tail-related quantity phù hợp.

Khi benchmark, Classical Monte Carlo và Quantum Amplitude Estimation phải ước lượng **cùng một financial quantity**.

---

## 14. Classical–Quantum Benchmark Philosophy

Sigma có thể nghiên cứu ba hướng:

### A. Pure Classical

```text
Historical Data
      ↓
Classical Scenario Generation
      ↓
Classical Monte Carlo
      ↓
VaR / CVaR
```

### B. Naive Hybrid

```text
Historical Data
      ↓
Classical Scenarios
      ↓
Quantum State Loading
      ↓
QAE
      ↓
VaR / CVaR
```

### C. Quantum / Co-designed Architecture

```text
Historical Data
      ↓
Classical Parameter Estimation
      ↓
Quantum Scenario Generation
      ↓
Quantum Estimation
      ↓
VaR / CVaR
```

Đây là các hướng nghiên cứu, không phải kết luận trước về practical advantage.

Mục tiêu là kiểm tra liệu lợi thế lý thuyết có còn tồn tại sau:

- state preparation;
- distribution loading;
- oracle construction;
- circuit execution;
- noise;
- overhead của toàn pipeline.

---

## 15. Non-Goals — V1 không làm

Sigma V1 không bao gồm:

- stock price prediction;
- automated trading;
- broker execution;
- OMS/EMS;
- full portfolio management;
- production auto-rebalancing;
- dynamic leverage như core functionality;
- QAOA portfolio optimization;
- full credit risk platform;
- full liquidity risk platform;
- XVA;
- enterprise real-time trading infrastructure;
- microservices architecture;
- Kubernetes;
- Kafka;
- mobile application;
- LLM financial advisor.

Các hướng trên chỉ được xem xét khi có financial hoặc product justification rõ ràng.

---

## 16. Decision Support Boundary

Sigma cung cấp **risk intelligence**, không tự động thay thế quyết định đầu tư.

Sigma có thể cho biết:

```text
CVaR 99% tăng đáng kể dưới volatility shock.

NVDA đóng góp lớn nhất vào portfolio tail risk.
```

Sigma hỗ trợ người dùng hiểu:

- risk level;
- risk drivers;
- scenario impact;
- tail behavior.

V1 không tự động:

- đặt lệnh;
- rebalance portfolio;
- thay đổi leverage;
- hedge position.

---

## 17. Product Interfaces

### API

FastAPI là product-facing interface.

Client tương tác với Sigma thông qua API contract thay vì truy cập trực tiếp internal modules.

### Dashboard

Taipy là reference client cho:

- portfolio setup;
- risk analysis;
- scenario analysis;
- stress testing;
- benchmark visualization.

### Future Clients

```text
Taipy
Notebook
CLI
Web Application
Financial Institution System
Third-party Application
        ↓
     Sigma API
```

---

## 18. Business Direction

Sigma được định hướng **B2B trước**.

Các nhóm khách hàng dài hạn:

- ngân hàng;
- công ty chứng khoán;
- công ty quản lý tài sản;
- fintech;
- các tổ chức tài chính.

Các hình thức sản phẩm có thể gồm:

- Risk Intelligence Platform;
- Risk Analytics API;
- specialized risk modules;
- integration services.

Business model không phải mục tiêu trực tiếp của V1.

V1 ưu tiên kiểm chứng:

```text
Problem
   ↓
Methodology
   ↓
Engine
   ↓
Benchmark
   ↓
Product Utility
```

trước khi mở rộng commercial deployment.

---

## 19. Tiêu chí thành công

### Financial Correctness

- Risk methodology được định nghĩa rõ;
- VaR/CVaR được tính nhất quán;
- scenario generation có assumptions rõ ràng;
- kết quả có thể kiểm chứng bằng tests.

### Technical Correctness

- Core modules hoạt động độc lập;
- API contract rõ ràng;
- Dashboard sử dụng API;
- Classical baseline có thể tái lập;
- Quantum module có thể chạy trên simulator và/hoặc backend phù hợp.

### Scientific Validity

- Classical baseline được thiết lập trước;
- Quantum formulation rõ ràng;
- benchmark dùng cùng problem và evaluation criteria;
- resource overhead được ghi nhận;
- không tuyên bố quantum advantage nếu dữ liệu thực nghiệm không chứng minh.

### Product Utility

Người dùng có thể:

```text
Configure Portfolio
      ↓
Run Risk Analysis
      ↓
Inspect Risk Metrics
      ↓
Explore Scenarios
      ↓
Understand Risk Drivers
      ↓
Compare Classical / Quantum
```

### Reproducibility

Mỗi experiment quan trọng cần ghi nhận:

- data source;
- dataset version / snapshot;
- model assumptions;
- simulation parameters;
- quantum parameters;
- benchmark configuration;
- output metrics.

---

## 20. Key Product Metrics

### Risk Engine

- VaR estimation error;
- CVaR estimation error;
- scenario convergence;
- simulation runtime;
- reproducibility.

### Quantum

- estimation error;
- query count;
- circuit depth;
- qubit count;
- shots;
- state preparation cost;
- oracle cost;
- noise sensitivity;
- end-to-end runtime.

### Product

- end-to-end analysis time;
- successful analysis rate;
- API reliability;
- interpretability of risk results;
- usability of risk output.

Không dùng một metric duy nhất như:

```text
Quantum runtime < Classical runtime
```

để kết luận quantum advantage.

---

## 21. Ràng buộc

Sigma V1 được phát triển trong điều kiện:

- giới hạn thời gian;
- giới hạn computational resources;
- giới hạn quantum hardware;
- giới hạn dữ liệu;
- giới hạn nhân lực;
- yêu cầu reproducibility;
- yêu cầu scientific credibility.

Vì vậy, ưu tiên:

```text
Correctness
    >
Complexity

Scientific Validity
    >
Feature Count

Measured Value
    >
Quantum Hype
```

---

## 22. Ưu tiên phát triển V1

### P0 — Core Risk Foundation

- Data;
- Returns;
- Volatility;
- Regime;
- Distribution;
- Monte Carlo;
- Loss Distribution;
- VaR/CVaR.

### P1 — Quantum Research

- Quantum formulation;
- state preparation;
- oracle;
- QAE-family;
- benchmarking;
- resource tracking.

### P2 — Productization

- FastAPI;
- API schemas;
- Taipy dashboard;
- Scenario Lab;
- Quantum Benchmark Lab.

### P3 — Extended Intelligence

- Risk decomposition;
- advanced stress testing;
- decision-support features.

---

## 23. Roadmap

### Phase 1 — Foundation

```text
Scope
  ↓
Data
  ↓
Methodology
  ↓
Core Architecture
```

### Phase 2 — Classical Risk Engine

```text
Returns
  ↓
Volatility
  ↓
Regime
  ↓
Distribution
  ↓
Monte Carlo
  ↓
VaR/CVaR
```

### Phase 3 — Quantum Research

```text
Financial Problem
  ↓
Quantum Formulation
  ↓
State Preparation
  ↓
Oracle
  ↓
QAE
  ↓
Benchmark
```

### Phase 4 — Product Integration

```text
Risk Engine
  ↓
FastAPI
  ↓
Taipy
```

### Phase 5 — Validation

```text
Scientific Validation
        +
Financial Validation
        +
Engineering Validation
        +
Product Validation
```

---

## 24. Định hướng phát triển sau V1

Sau khi V1 được kiểm chứng:

```text
V1
Risk Analytics
    ↓
V2
Portfolio Intelligence
    ↓
V3
Dynamic Risk Management
    ↓
V4
Multi-Layer Financial Risk Intelligence
```

Capability tương lai có thể gồm:

- Portfolio optimization;
- Risk-aware allocation;
- Dynamic risk monitoring;
- Credit Risk;
- Liquidity Risk;
- broader scenario intelligence;
- advanced quantum financial computing.

Mọi capability mới phải đáp ứng:

```text
Financial Need
      +
Scientific Justification
      +
Technical Feasibility
      +
Product Value
```

---

## 25. Product Boundaries

```text
                     Sigma
                       │
         ┌─────────────┴─────────────┐
         │                           │
 Risk Intelligence            Decision Support
         │                           │
   ┌─────┼─────┬────────┐            │
   │     │     │        │            │
 Data  Model Scenario Quantum     Future Layer
         │
         ▼
    Risk Metrics
    VaR / CVaR
```

Quantum là computational enhancement layer bên trong Risk Intelligence, không phải product độc lập.

---

## 26. Product Definition

> **Sigma là một Regime-Aware Portfolio Risk Intelligence Engine sử dụng dữ liệu thị trường để mô hình hóa điều kiện thị trường, sinh kịch bản, xây dựng phân phối tổn thất và ước lượng các chỉ số rủi ro như VaR/CVaR; đồng thời nghiên cứu khả năng sử dụng Quantum Amplitude Estimation để tăng cường một số bài toán ước lượng và đánh giá phương pháp lượng tử một cách công bằng với Classical Computing.**

Sigma không tuyên bố Quantum Advantage trước khi có bằng chứng thực nghiệm.

Giá trị của Sigma nằm ở:

```text
Financially Meaningful Problem
            +
Rigorous Risk Modeling
            +
Classical Baseline
            +
Quantum Enhancement
            +
Fair Benchmark
            +
Risk Intelligence
            +
API-first Product
```

---

## 27. North Star

> **Sigma không xây Quantum để chứng minh Quantum.**

> **Sigma xây Risk Intelligence, và sử dụng Quantum ở những nơi Quantum thực sự có thể tạo ra giá trị có thể đo lường.**

Mục tiêu cuối cùng:

```text
Scientifically Rigorous
        +
Technically Feasible
        +
Empirically Validated
        +
Practically Useful
        +
Productizable
        ↓
SIGMA RISK INTELLIGENCE
```

---

## 28. Document Boundary

PRD định nghĩa **what và why** của Sigma.

| Nội dung | Tài liệu |
|---|---|
| Product experience và UI/UX | `DESIGN.md` |
| System architecture và dependency direction | `ARCHITECTURE.md` |
| Data / domain schema | `SCHEMA.md` |
| Engineering / research rules | `RULES.md` |
| Technology selection | `TECH_STACK.md` |
| Team ownership | `TEAM.md` / `ROLES.md` |
| Development workflow | `WORKFLOW.md` |

PRD là baseline để các tài liệu khác phát triển nhất quán, không phải nơi chứa toàn bộ implementation detail của Sigma.
