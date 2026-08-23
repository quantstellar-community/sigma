# Sigma --- Product Requirements Document

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Sản phẩm:** Sigma Risk Intelligence\
> **Loại sản phẩm:** Regime-Aware Portfolio Risk Intelligence Engine\
> **Lĩnh vực:** Market Risk & Portfolio Risk\
> **Định hướng:** API-first, Modular Monolith

------------------------------------------------------------------------

## 1. Tổng quan

Sigma là một **Regime-Aware Portfolio Risk Intelligence Engine** nhằm hỗ
trợ phân tích và định lượng rủi ro danh mục đầu tư thông qua mô hình hóa
điều kiện thị trường, sinh kịch bản, xây dựng phân phối lãi/lỗ và tính
toán các chỉ số rủi ro như VaR và CVaR.

Sigma kết hợp phương pháp tài chính định lượng cổ điển với Quantum
Computing tại những bước mà phương pháp lượng tử có vai trò tính toán rõ
ràng.

Triết lý cốt lõi:

> **Classical First → Quantum Where Justified → Fair Benchmark → Measure
> Real Value → Risk Intelligence → Decision Support**

Sigma không giả định Quantum Computing luôn vượt trội so với Classical
Computing. Hệ thống phải cho phép đặt các phương pháp trên cùng một bài
toán để đánh giá độ chính xác, tài nguyên tính toán và giá trị thực tế.

------------------------------------------------------------------------

## 2. Vấn đề cần giải quyết

### 2.1. Risk modeling trong điều kiện thị trường thay đổi

Phân phối lợi suất và mức độ biến động của thị trường không nhất thiết
ổn định theo thời gian. Một quy trình risk analysis dựa trên một
distribution cố định có thể không phản ánh đầy đủ sự thay đổi của market
regimes.

Sigma mô hình hóa quá trình:

``` text
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

Mục tiêu là tạo ra risk analysis có xét đến điều kiện thị trường thay vì
chỉ tạo ra một con số risk độc lập với bối cảnh.

### 2.2. Computational challenge

Monte Carlo là một phương pháp quan trọng để ước lượng các đại lượng rủi
ro từ phân phối tổn thất, nhưng sai số sampling giảm theo tốc độ
(O(1/`\sqrt{N}`{=tex})).

Quantum Amplitude Estimation có lợi thế lý thuyết về query complexity
trong một số bài toán ước lượng xác suất và kỳ vọng. Tuy nhiên, state
preparation, distribution loading, oracle construction, circuit depth,
số qubit, shots, noise và runtime có thể làm giảm hoặc loại bỏ lợi thế
lý thuyết.

Vì vậy, câu hỏi của Sigma không phải:

> "Quantum có nhanh hơn Classical không?"

mà là:

> **"Trong điều kiện nào lợi thế tính toán của Quantum có thể tồn tại
> sau khi tính đến toàn bộ financial risk pipeline?"**

------------------------------------------------------------------------

## 3. Product Vision

### 3.1. Vision

Xây dựng một nền tảng **Financial Risk Intelligence** có khả năng biến
dữ liệu thị trường và thông tin danh mục thành các đánh giá rủi ro định
lượng, có khả năng giải thích và có thể tích hợp vào các hệ thống tài
chính khác thông qua API.

### 3.2. Product direction

``` text
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

Quantum được xem là **computational enhancement layer**, không phải mục
tiêu cuối cùng của sản phẩm.

### 3.3. Long-term direction

Risk Analytics là nền tảng ban đầu. Sigma có thể mở rộng về sau sang
Portfolio Intelligence, Risk Contribution, Concentration Analysis,
Portfolio Optimization, Credit Risk, Liquidity Risk, Dynamic Risk
Management và các lớp Decision Intelligence rộng hơn.

Portfolio Management là lớp ứng dụng có thể phát triển phía trên Risk
Engine, không phải lõi của Sigma V1.

------------------------------------------------------------------------

## 4. Product Positioning

Sigma được định vị là:

> **Risk Intelligence Engine, không phải Trading Bot.**

Sigma không nhằm:

-   dự báo giá cổ phiếu;
-   tự động giao dịch;
-   thay thế portfolio manager;
-   trở thành OMS/EMS;
-   trở thành hệ thống portfolio management hoàn chỉnh.

Sigma tập trung vào câu hỏi:

> **"Danh mục có thể chịu rủi ro như thế nào, trong những điều kiện nào,
> và mức độ bất định của kết quả là bao nhiêu?"**

Sigma cung cấp risk intelligence để hỗ trợ quyết định, nhưng không mặc
định tự động thực hiện quyết định đầu tư.

------------------------------------------------------------------------

## 5. Target Users

### 5.1. Risk Analysts

-   Phân tích portfolio risk.
-   Tính VaR/CVaR.
-   Phân tích loss distribution.
-   Phân tích risk contribution.
-   Thực hiện stress testing.
-   So sánh scenario.

### 5.2. Portfolio Managers

-   Đánh giá mức độ rủi ro của danh mục.
-   Xác định các nguồn đóng góp lớn vào tail risk.
-   Đánh giá portfolio dưới các market scenarios.
-   Hỗ trợ quyết định quản trị danh mục.

### 5.3. Quantitative Researchers / Risk Modelers

-   Nghiên cứu risk distributions.
-   Thử nghiệm volatility/regime models.
-   Nghiên cứu Monte Carlo.
-   Nghiên cứu Quantum Amplitude Estimation.
-   Benchmark Classical--Quantum approaches.

### 5.4. Financial Institutions

Định hướng dài hạn:

-   Ngân hàng.
-   Công ty chứng khoán.
-   Công ty quản lý tài sản.
-   Fintech.
-   Các tổ chức tài chính có nhu cầu phân tích và quản trị rủi ro.

------------------------------------------------------------------------

## 6. User Problems

### P1 --- Portfolio Risk Quantification

Người dùng cần biết mức độ rủi ro của một danh mục dưới các điều kiện
thị trường khác nhau.

### P2 --- Tail Risk Understanding

Người dùng cần hiểu:

-   xác suất xảy ra loss lớn;
-   mức loss tại tail;
-   Expected Shortfall;
-   các scenario xấu;
-   tài sản đóng góp lớn vào tail risk.

### P3 --- Regime-Aware Risk

Người dùng cần mô hình hóa risk trong bối cảnh thị trường thay đổi thay
vì giả định một distribution cố định.

### P4 --- Scenario & Stress Analysis

Người dùng cần đánh giá portfolio dưới các market shock hoặc scenario cụ
thể.

### P5 --- Classical--Quantum Evaluation

Nhà nghiên cứu cần một framework để đặt Classical và Quantum trên cùng
một financial problem và đánh giá một cách công bằng.

### P6 --- Integration

Các hệ thống tài chính khác cần sử dụng risk computation thông qua API
thay vì phụ thuộc vào giao diện Sigma.

------------------------------------------------------------------------

## 7. Product Goals

### Goal 1 --- Risk Analytics Core

Sigma phải có khả năng:

-   xử lý market data;
-   tính returns;
-   mô hình hóa volatility;
-   nhận diện market regime;
-   xây dựng regime-aware distribution;
-   sinh scenarios;
-   tạo portfolio loss distribution;
-   tính VaR;
-   tính CVaR / Expected Shortfall;
-   thực hiện stress testing.

### Goal 2 --- Classical Baseline

Classical Monte Carlo phải là baseline chính để:

-   kiểm chứng methodology;
-   làm reference implementation;
-   đánh giá accuracy;
-   làm đối chứng cho Quantum.

### Goal 3 --- Quantum Enhancement

Quantum được đưa vào một financial estimation problem cụ thể, ưu tiên
các bài toán phù hợp với Quantum Amplitude Estimation và các biến thể
phù hợp.

### Goal 4 --- Fair Classical--Quantum Benchmark

Benchmark phải xem xét:

-   accuracy;
-   estimation error;
-   number of samples / queries;
-   runtime;
-   qubits;
-   circuit depth;
-   shots;
-   noise;
-   state preparation cost;
-   oracle cost;
-   end-to-end computational cost.

### Goal 5 --- Productize Risk Engine

Risk computation phải có API rõ ràng để có thể được sử dụng bởi
dashboard, notebook, CLI và các client bên ngoài trong tương lai.

------------------------------------------------------------------------

## 8. Product Principles

### 8.1. Classical First

Classical methods phải được xây dựng và kiểm chứng trước khi đưa Quantum
vào.

### 8.2. Quantum Where Justified

Mỗi Quantum component phải có:

-   financial problem;
-   mathematical formulation;
-   computational motivation;
-   classical baseline;
-   benchmark protocol.

### 8.3. No Assumed Quantum Advantage

Sigma không được mặc định Quantum thắng.

Một kết quả hợp lệ có thể là:

``` text
Quantum has theoretical query advantage
        ↓
State preparation dominates
        ↓
No end-to-end practical advantage
```

Đây vẫn là một kết quả nghiên cứu có giá trị.

### 8.4. Financial Validity First

Quantum result không có ý nghĩa nếu financial formulation hoặc risk
methodology không hợp lệ.

### 8.5. End-to-End Evaluation

Benchmark phải tính đến toàn bộ computational pipeline thay vì chỉ
benchmark một quantum circuit cô lập.

### 8.6. Explainability

Risk output phải giúp người dùng hiểu:

-   risk đến từ đâu;
-   scenario nào tạo ra risk;
-   tài sản nào đóng góp nhiều nhất;
-   assumptions nào được sử dụng.

### 8.7. API First

Risk Engine phải độc lập với UI. Taipy là reference client; API là
product interface.

------------------------------------------------------------------------

## 9. V1 Product Scope

Sigma V1 tập trung vào:

> **Regime-Aware Portfolio Risk Intelligence**

### 9.1. Input

-   historical market prices;
-   portfolio positions / weights;
-   portfolio value;
-   confidence level;
-   risk horizon;
-   simulation parameters;
-   scenario parameters.

### 9.2. Data Processing

-   data ingestion;
-   data validation;
-   cleaning;
-   adjusted price handling;
-   return calculation;
-   volatility estimation;
-   covariance/correlation estimation.

### 9.3. Market Modeling

-   return modeling;
-   conditional volatility modeling;
-   market regime detection;
-   regime-aware distribution modeling.

GARCH và HMM có thể được sử dụng khi phù hợp với financial/statistical
assumptions.

### 9.4. Scenario Generation

-   Monte Carlo simulation;
-   portfolio-level scenario generation;
-   loss distribution;
-   stress scenarios.

### 9.5. Risk Metrics

-   VaR;
-   CVaR / Expected Shortfall;
-   Expected Loss;
-   volatility;
-   simulated worst loss;
-   probability of loss vượt threshold;
-   risk contribution.

### 9.6. Quantum Risk Estimation

V1 nghiên cứu:

-   Quantum Amplitude Estimation;
-   các biến thể phù hợp như Iterative / Maximum Likelihood Amplitude
    Estimation khi cần;
-   quantum state preparation;
-   risk/payoff oracle;
-   quantum resource estimation.

Quantum module phải được benchmark với Classical baseline.

### 9.7. Classical--Quantum Benchmark

Sigma phải có khả năng so sánh Classical và Quantum trên cùng financial
problem với cùng evaluation criteria.

### 9.8. Stress Testing

V1 hỗ trợ:

-   market shock;
-   volatility shock;
-   asset/sector shock;
-   historical crisis scenarios;
-   custom scenarios khi phù hợp.

### 9.9. API

API phải hỗ trợ các nhóm chức năng:

-   portfolio analysis;
-   risk estimation;
-   scenario/stress analysis;
-   Classical--Quantum benchmark.

### 9.10. Dashboard

Taipy đóng vai trò:

-   reference client;
-   interactive risk console;
-   visualization layer;
-   benchmark interface;
-   demonstration interface.

Dashboard không chứa financial business logic.

------------------------------------------------------------------------

## 10. V1 Core Workflow

``` text
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
│          vs               │
│ Quantum Estimation        │
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

------------------------------------------------------------------------

## 11. Product Outputs

### 11.1. Risk Summary

-   Portfolio Value.
-   Volatility.
-   VaR 95%.
-   VaR 99%.
-   CVaR 95%.
-   CVaR 99%.
-   Expected Loss.

### 11.2. Risk Decomposition

-   Asset Risk Contribution.
-   Portfolio Concentration.
-   Volatility Contribution.
-   Covariance / Correlation.
-   Top Risk Drivers.

### 11.3. Scenario & Stress Results

-   Portfolio Loss.
-   Loss Distribution.
-   Tail Loss.
-   Stress Loss.
-   VaR Change.
-   CVaR Change.
-   Worst Scenarios.

### 11.4. Classical--Quantum Benchmark

-   Estimator.
-   Estimate.
-   Absolute Error.
-   Relative Error.
-   Runtime.
-   Number of Samples / Queries.
-   Qubits.
-   Circuit Depth.
-   Shots.
-   Noise Setting.
-   State Preparation Cost.
-   Oracle Cost.

Kết luận benchmark phải phản ánh kết quả thực nghiệm thay vì mặc định
Quantum thắng.

------------------------------------------------------------------------

## 12. Quantum Research Scope

Quantum trong V1 là computational layer cho một số estimation problems
đã được financial formulation.

Quantum không xử lý:

-   raw data cleaning;
-   market data ingestion;
-   toàn bộ portfolio pipeline;
-   financial preprocessing;
-   API orchestration.

Quantum nhận một bài toán đã được chuẩn hóa, ví dụ:

``` text
P(Loss > Threshold)
```

hoặc một expected value / tail-related quantity phù hợp.

Classical Monte Carlo và Quantum Amplitude Estimation được đánh giá trên
cùng quantity.

------------------------------------------------------------------------

## 13. Classical--Quantum Benchmark Philosophy

Sigma có thể nghiên cứu ba architecture:

### A. Pure Classical

``` text
Historical Data
→ Classical Scenario Generation
→ Classical Monte Carlo
→ VaR/CVaR
```

### B. Naive Hybrid

``` text
Historical Data
→ Classical Scenarios
→ Quantum State Loading
→ QAE
→ VaR/CVaR
```

### C. Quantum / Co-designed Architecture

``` text
Historical Data
→ Classical Parameter Estimation
→ Quantum Scenario Generation
→ Quantum Estimation
→ VaR/CVaR
```

Các architecture trên là research directions, không phải kết luận trước
về practical advantage.

Mục tiêu là kiểm tra liệu theoretical quantum advantage có còn tồn tại
sau state preparation, distribution loading, oracle construction và các
overhead của toàn pipeline hay không.

------------------------------------------------------------------------

## 14. Non-Goals --- V1 không làm

Sigma V1 không bao gồm:

-   stock price prediction;
-   automated trading;
-   broker execution;
-   OMS/EMS;
-   full portfolio management;
-   production auto-rebalancing;
-   dynamic leverage như core functionality;
-   QAOA portfolio optimization;
-   full credit risk platform;
-   full liquidity risk platform;
-   XVA;
-   enterprise real-time trading infrastructure;
-   microservices architecture;
-   Kubernetes;
-   Kafka;
-   mobile application;
-   LLM financial advisor.

Các hướng trên có thể được xem xét trong roadmap nếu có
financial/product justification.

------------------------------------------------------------------------

## 15. Decision Support Boundary

Sigma cung cấp **risk intelligence**, không tự động thay thế quyết định
đầu tư.

Sigma có thể cho biết:

``` text
CVaR 99% tăng đáng kể dưới volatility shock.

NVDA đóng góp lớn nhất vào portfolio tail risk.
```

Sigma có thể hỗ trợ hiểu:

-   risk level;
-   risk drivers;
-   scenario impact;
-   tail behavior.

V1 không tự động:

-   đặt lệnh;
-   rebalance portfolio;
-   thay đổi leverage;
-   hedge position.

------------------------------------------------------------------------

## 16. Product Interfaces

### 16.1. API

FastAPI là product-facing interface.

Client tương tác với Sigma thông qua API contract thay vì truy cập trực
tiếp internal modules.

### 16.2. Dashboard

Taipy là reference client cho:

-   portfolio setup;
-   risk analysis;
-   scenario analysis;
-   stress testing;
-   benchmark visualization.

### 16.3. Future Clients

``` text
Taipy
Notebook
CLI
Web Application
Financial Institution System
Third-party Application
        ↓
     Sigma API
```

------------------------------------------------------------------------

## 17. Business Direction

Sigma được định hướng **B2B trước**.

Các nhóm khách hàng dài hạn:

-   ngân hàng;
-   công ty chứng khoán;
-   công ty quản lý tài sản;
-   fintech;
-   các tổ chức tài chính.

Các hình thức sản phẩm có thể gồm:

-   Risk Intelligence Platform;
-   Risk Analytics API;
-   specialized risk modules;
-   integration services.

Business model không phải mục tiêu trực tiếp của V1. V1 ưu tiên kiểm
chứng:

``` text
Problem
→ Methodology
→ Engine
→ Benchmark
→ Product Utility
```

trước khi mở rộng commercial deployment.

------------------------------------------------------------------------

## 18. Success Criteria

### 18.1. Financial Correctness

-   Risk methodology được định nghĩa rõ.
-   VaR/CVaR được tính nhất quán.
-   Scenario generation có assumptions rõ ràng.
-   Kết quả có thể được kiểm chứng bằng tests.

### 18.2. Technical Correctness

-   Core modules hoạt động độc lập.
-   API contract rõ ràng.
-   Dashboard sử dụng API.
-   Classical baseline reproducible.
-   Quantum module có thể chạy trên simulator và/hoặc backend phù hợp.

### 18.3. Scientific Validity

-   Classical baseline được thiết lập trước.
-   Quantum formulation rõ ràng.
-   Benchmark sử dụng cùng problem và evaluation criteria.
-   Resource overhead được ghi nhận.
-   Không tuyên bố quantum advantage nếu dữ liệu thực nghiệm không chứng
    minh.

### 18.4. Product Utility

Người dùng có thể:

``` text
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

### 18.5. Reproducibility

Mỗi experiment cần có khả năng ghi nhận:

-   data source;
-   dataset version/snapshot;
-   model assumptions;
-   simulation parameters;
-   quantum parameters;
-   benchmark configuration;
-   output metrics.

------------------------------------------------------------------------

## 19. Key Product Metrics

### Risk Engine

-   VaR estimation error;
-   CVaR estimation error;
-   scenario convergence;
-   simulation runtime;
-   reproducibility.

### Quantum

-   estimation error;
-   query count;
-   circuit depth;
-   qubit count;
-   shots;
-   state preparation cost;
-   oracle cost;
-   noise sensitivity;
-   end-to-end runtime.

### Product

-   end-to-end analysis time;
-   successful analysis rate;
-   API reliability;
-   interpretability of risk results;
-   usability of risk output.

Không sử dụng một metric duy nhất như "Quantum runtime \< Classical
runtime" để kết luận quantum advantage.

------------------------------------------------------------------------

## 20. Constraints

Sigma V1 được phát triển trong điều kiện:

-   giới hạn thời gian của cuộc thi;
-   giới hạn computational resources;
-   giới hạn quantum hardware;
-   giới hạn dữ liệu;
-   giới hạn nhân lực;
-   yêu cầu reproducibility;
-   yêu cầu scientific credibility.

Do đó ưu tiên:

``` text
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

------------------------------------------------------------------------

## 21. V1 Development Priorities

### P0 --- Core Risk Foundation

-   Data.
-   Returns.
-   Volatility.
-   Regime.
-   Distribution.
-   Monte Carlo.
-   Loss Distribution.
-   VaR/CVaR.

### P1 --- Quantum Research

-   Quantum formulation.
-   State preparation.
-   Oracle.
-   QAE-family.
-   Benchmarking.
-   Resource tracking.

### P2 --- Productization

-   FastAPI.
-   API schemas.
-   Taipy dashboard.
-   Scenario Lab.
-   Quantum Benchmark Lab.

### P3 --- Extended Intelligence

-   Risk decomposition.
-   Advanced stress testing.
-   Decision-support features.

------------------------------------------------------------------------

## 22. Initial Roadmap

### Phase 1 --- Foundation

``` text
Scope
→ Data
→ Methodology
→ Core Architecture
```

### Phase 2 --- Classical Risk Engine

``` text
Returns
→ Volatility
→ Regime
→ Distribution
→ Monte Carlo
→ VaR/CVaR
```

### Phase 3 --- Quantum Research

``` text
Financial Problem
→ Quantum Formulation
→ State Preparation
→ Oracle
→ QAE
→ Benchmark
```

### Phase 4 --- Product Integration

``` text
Risk Engine
→ FastAPI
→ Taipy
```

### Phase 5 --- Validation

``` text
Scientific Validation
+
Financial Validation
+
Engineering Validation
+
Product Validation
```

------------------------------------------------------------------------

## 23. Future Product Direction

Sau khi V1 được kiểm chứng:

``` text
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

Các capability tương lai có thể bao gồm:

-   Portfolio optimization.
-   Risk-aware allocation.
-   Dynamic risk monitoring.
-   Credit Risk.
-   Liquidity Risk.
-   Broader scenario intelligence.
-   Advanced quantum financial computing.

Mọi capability mới phải đáp ứng:

``` text
Financial Need
+
Scientific Justification
+
Technical Feasibility
+
Product Value
```

------------------------------------------------------------------------

## 24. Product Boundaries

``` text
                    Sigma
                      │
        ┌─────────────┴─────────────┐
        │                           │
   Risk Intelligence          Decision Support
        │                           │
   ┌────┼────┬────────┐             │
   │    │    │        │             │
 Data Model Scenario Quantum    Future Layer
        │
        ▼
   Risk Metrics
   VaR / CVaR
```

Quantum là computational enhancement layer bên trong Risk Intelligence,
không phải product độc lập.

------------------------------------------------------------------------

## 25. Product Definition

> **Sigma là một Regime-Aware Portfolio Risk Intelligence Engine sử dụng
> dữ liệu thị trường để mô hình hóa điều kiện thị trường, sinh kịch bản,
> xây dựng phân phối tổn thất và ước lượng các chỉ số rủi ro như
> VaR/CVaR; đồng thời nghiên cứu khả năng sử dụng Quantum Amplitude
> Estimation để tăng cường một số bài toán ước lượng và đánh giá phương
> pháp lượng tử một cách công bằng với Classical Computing.**

Sigma không tuyên bố Quantum Advantage trước khi có bằng chứng thực
nghiệm.

Giá trị của Sigma nằm ở:

``` text
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

------------------------------------------------------------------------

## 26. North Star

> **Sigma không xây Quantum để chứng minh Quantum.**
>
> **Sigma xây Risk Intelligence, và sử dụng Quantum ở những nơi Quantum
> thực sự có thể tạo ra giá trị có thể đo lường.**

Mục tiêu cuối cùng:

``` text
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

------------------------------------------------------------------------

## 27. Document Boundary

PRD này định nghĩa **what và why** của Sigma.

Các nội dung sau không thuộc phạm vi chi tiết của PRD và sẽ được quy
định trong các tài liệu chuyên biệt:

-   Product experience và UI/UX → `DESIGN.md`
-   System architecture và dependency direction → `ARCHITECTURE.md`
-   Data/domain schema → `SCHEMA.md`
-   Engineering/research rules → `RULES.md`
-   Technology selection → `TECH_STACK.md`
-   Team ownership → `TEAM.md` và `ROLES.md`
-   Development workflow → `WORKFLOW.md`

PRD là baseline để các tài liệu tiếp theo phát triển nhất quán, không
phải nơi chứa toàn bộ implementation detail của Sigma.
