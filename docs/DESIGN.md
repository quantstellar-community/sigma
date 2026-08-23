# Sigma --- Product Design Document

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Sản phẩm:** Sigma Risk Intelligence\
> **Định hướng trải nghiệm:** Professional Quant / Risk Intelligence
> Workstation\
> **Reference Client V1:** Taipy\
> **Product Interface:** FastAPI + client UI

------------------------------------------------------------------------

## 1. Mục đích tài liệu

`DESIGN.md` định nghĩa trải nghiệm sản phẩm và cách người dùng tương tác
với Sigma.

Tài liệu này trả lời:

-   Người dùng của Sigma là ai?
-   Họ cần hoàn thành những nhiệm vụ nào?
-   Sigma nên tổ chức thông tin như thế nào?
-   Các màn hình chính gồm những gì?
-   Người dùng đi qua workflow nào?
-   Risk results được trình bày ra sao?
-   Scenario và stress testing được tương tác như thế nào?
-   Classical--Quantum benchmark được trình bày như thế nào?
-   Những nguyên tắc UX/UI nào phải được giữ nhất quán?

Tài liệu này **không** định nghĩa chi tiết implementation của Risk
Engine, database schema, API internals hoặc technology decisions. Các
nội dung đó thuộc `ARCHITECTURE.md`, `SCHEMA.md` và `TECH_STACK.md`.

------------------------------------------------------------------------

# 2. Design Vision

Sigma không nên được thiết kế như một consumer finance application,
trading app hoặc chatbot.

Định hướng trải nghiệm của Sigma là:

> **Professional Risk Intelligence Workstation**

Giao diện cần tạo cảm giác:

-   chuyên nghiệp;
-   phân tích;
-   có mật độ thông tin hợp lý;
-   rõ ràng về assumptions;
-   tập trung vào risk;
-   hỗ trợ investigation;
-   không màu mè;
-   không biến Quantum thành một gimmick trực quan.

Tham chiếu về information density và workstation-style interface có thể
lấy cảm hứng từ các hệ thống quant/risk chuyên nghiệp như ORE Studio,
nhưng Sigma chỉ kế thừa tinh thần workstation và không sao chép scope
enterprise của các hệ thống đó.

Sigma V1 chỉ tập trung vào:

``` text
Portfolio
    ↓
Risk
    ↓
Scenario
    ↓
Stress
    ↓
Quantum Benchmark
    ↓
Decision Support
```

------------------------------------------------------------------------

# 3. Design Principles

## 3.1. Risk First

Người dùng tài chính phải nhìn thấy risk result trước khi nhìn thấy chi
tiết kỹ thuật.

Primary information:

-   VaR;
-   CVaR;
-   volatility;
-   loss distribution;
-   risk contribution;
-   scenario impact.

Quantum benchmark là một lớp phân tích bổ sung, không được chiếm vị trí
của risk result.

------------------------------------------------------------------------

## 3.2. Analytical Before Decorative

Mọi thành phần UI phải có mục đích phân tích.

Không thêm:

-   animation chỉ để trang trí;
-   card không có information value;
-   biểu đồ không phục vụ một câu hỏi cụ thể;
-   metric chỉ để làm dashboard "nhiều số".

------------------------------------------------------------------------

## 3.3. Information Density có kiểm soát

Sigma cần dense hơn một consumer dashboard nhưng không được trở thành
một màn hình chứa quá nhiều thông tin không có hierarchy.

Nguyên tắc:

``` text
Primary Risk
    ↓
Key Drivers
    ↓
Distribution / Scenario
    ↓
Detailed Metrics
    ↓
Technical Details
```

------------------------------------------------------------------------

## 3.4. Progressive Disclosure

Thông tin được mở dần theo nhu cầu.

Ví dụ:

``` text
Risk Overview
    ↓
Risk Driver
    ↓
Scenario
    ↓
Model Assumptions
    ↓
Technical Details
```

Người dùng không cần nhìn thấy toàn bộ model parameters ngay khi mở
Sigma.

------------------------------------------------------------------------

## 3.5. Explain Before Conclude

Sigma không nên đưa ra một kết luận risk mà không cho người dùng biết cơ
sở.

Ví dụ:

Không chỉ hiển thị:

``` text
CVaR 99% = -12.4%
```

mà phải cho phép người dùng truy cập:

``` text
CVaR 99%
    ↓
Loss Distribution
    ↓
Tail Scenarios
    ↓
Risk Contributors
    ↓
Model / Scenario Assumptions
```

------------------------------------------------------------------------

## 3.6. No False Precision

UI không được làm cho một estimated quantity trông như một sự thật tuyệt
đối.

Các kết quả phải có context:

-   confidence level;
-   horizon;
-   scenario count;
-   model;
-   dataset;
-   assumptions;
-   estimation error khi phù hợp.

------------------------------------------------------------------------

## 3.7. Quantum Transparency

Không hiển thị:

``` text
Quantum = Better
```

như một kết luận mặc định.

Thay vào đó:

``` text
Classical
Estimate
Error
Runtime
Samples

Quantum
Estimate
Error
Runtime
Queries
Qubits
Depth
Shots
```

Sau đó mới đưa ra benchmark conclusion dựa trên kết quả thực nghiệm.

------------------------------------------------------------------------

## 3.8. Decision Support, Not Automated Decision

Sigma hỗ trợ người dùng hiểu risk.

Sigma V1 không tự động:

-   đặt lệnh;
-   rebalance;
-   thay đổi leverage;
-   hedge position.

UI phải phản ánh boundary này.

------------------------------------------------------------------------

# 4. Primary Users

## 4.1. Risk Analyst

Nhu cầu:

-   portfolio risk;
-   VaR/CVaR;
-   stress testing;
-   risk contribution;
-   scenario analysis.

Ưu tiên UI:

``` text
Risk Overview
→ Risk Drivers
→ Scenario
→ Stress
→ Report
```

------------------------------------------------------------------------

## 4.2. Portfolio Manager

Nhu cầu:

-   hiểu risk profile;
-   xem downside;
-   so sánh scenario;
-   nhận diện concentration;
-   hỗ trợ portfolio decision.

Ưu tiên:

``` text
Portfolio
→ Risk
→ Scenario
→ Decision Support
```

------------------------------------------------------------------------

## 4.3. Quant / Risk Researcher

Nhu cầu:

-   model assumptions;
-   distributions;
-   simulation parameters;
-   Classical baseline;
-   Quantum benchmark;
-   resource metrics.

Ưu tiên:

``` text
Risk
→ Model Details
→ Benchmark
→ Experiment Evidence
```

------------------------------------------------------------------------

## 4.4. Competition / Demonstration User

Nhu cầu:

-   nhanh chóng hiểu Sigma;
-   tạo một portfolio;
-   chạy risk analysis;
-   xem risk output;
-   xem Classical--Quantum comparison.

Demo flow phải hoàn thành được trong thời gian ngắn và không yêu cầu
người dùng hiểu toàn bộ internal methodology.

------------------------------------------------------------------------

# 5. Information Architecture

Sigma V1 sử dụng một navigation structure tập trung vào risk workflow:

``` text
SIGMA
│
├── Dashboard
│
├── Portfolios
│
├── Risk Analysis
│
├── Scenario Lab
│
├── Stress Testing
│
├── Quantum Benchmark
│
└── Reports
```

### Dashboard

Tổng quan portfolio và risk.

### Portfolios

Tạo, chọn và kiểm tra portfolio.

### Risk Analysis

Phân tích risk metrics và risk drivers.

### Scenario Lab

Khám phá simulated scenarios và loss distribution.

### Stress Testing

Đánh giá portfolio dưới các market shocks.

### Quantum Benchmark

So sánh Classical và Quantum estimation.

### Reports

Tổng hợp và xuất kết quả phân tích.

------------------------------------------------------------------------

# 6. Global Layout

Sigma nên sử dụng layout kiểu workstation:

``` text
┌─────────────────────────────────────────────────────────────┐
│ SIGMA   Portfolios  Risk  Scenarios  Quantum  Reports       │
├───────────────┬─────────────────────────────────────────────┤
│               │                                             │
│ Context /     │              Main Workspace                │
│ Portfolio     │                                             │
│ Explorer      │                                             │
│               │                                             │
│               │                                             │
├───────────────┴─────────────────────────────────────────────┤
│ Status / Dataset / Model / Analysis State                   │
└─────────────────────────────────────────────────────────────┘
```

Không bắt buộc phải giữ đúng hình thức này ở mọi màn hình, nhưng
hierarchy cần nhất quán.

------------------------------------------------------------------------

# 7. Global Context

Mỗi risk analysis nên luôn giữ được context:

``` text
Portfolio
Market Dataset
Analysis Date / Period
Risk Horizon
Confidence Level
Scenario Count
Model
```

Ví dụ:

``` text
Portfolio: Balanced Growth
Dataset: Market Universe V1
Period: 2018–2025
Horizon: 10D
Confidence: 99%
Scenarios: 100,000
Model: Regime-Aware
```

Người dùng không nên phải nhớ các setting này từ một màn hình khác.

------------------------------------------------------------------------

# 8. Core User Journey

Workflow chính:

``` text
Open Sigma
    ↓
Select / Create Portfolio
    ↓
Configure Analysis
    ↓
Run Risk Analysis
    ↓
Risk Overview
    ↓
Investigate Drivers
    ↓
Explore Scenarios
    ↓
Run Stress Test
    ↓
Optional: Quantum Benchmark
    ↓
Review Result
    ↓
Generate Report
```

------------------------------------------------------------------------

# 9. Screen 1 --- Dashboard

## Mục tiêu

Cho người dùng một snapshot nhanh về trạng thái risk hiện tại.

## Nội dung

### Portfolio Summary

-   Portfolio name;
-   portfolio value;
-   number of assets;
-   analysis date.

### Risk KPIs

-   VaR 95%;
-   VaR 99%;
-   CVaR 95%;
-   CVaR 99%;
-   volatility;
-   expected loss.

### Risk Distribution

Biểu đồ loss distribution với:

-   VaR threshold;
-   CVaR/tail region;
-   expected loss nếu phù hợp.

### Risk Contributors

Top contributors:

``` text
Asset
Weight
Risk Contribution
```

### Recent / Selected Scenario

Hiển thị scenario hoặc stress result gần nhất nếu có.

------------------------------------------------------------------------

# 10. Screen 2 --- Portfolio Explorer

## Mục tiêu

Cho phép người dùng hiểu portfolio trước khi chạy risk.

## Inputs

-   asset;
-   ticker;
-   weight;
-   position;
-   portfolio value.

## Validation

UI phải cảnh báo:

-   missing asset;
-   duplicate asset;
-   invalid weight;
-   total weight không hợp lệ;
-   missing market data.

Ví dụ:

``` text
Total Weight: 97.0%

[!] Portfolio weights do not sum to 100%.
```

Không tự động sửa dữ liệu mà không thông báo.

## Visualizations

-   allocation chart;
-   weight table;
-   asset summary;
-   optional correlation preview.

------------------------------------------------------------------------

# 11. Screen 3 --- Risk Analysis

Đây là màn hình trung tâm của Sigma.

## 11.1. Analysis Configuration

Người dùng cấu hình:

``` text
Confidence Level
Risk Horizon
Scenario Count
Market Period
Model
```

Các advanced settings có thể được ẩn dưới:

``` text
Advanced Configuration
```

------------------------------------------------------------------------

## 11.2. Risk Summary

Primary metrics:

``` text
VaR 95%
VaR 99%
CVaR 95%
CVaR 99%
Volatility
Expected Loss
```

Mỗi metric cần có:

-   value;
-   unit;
-   confidence/horizon context;
-   optional comparison với baseline.

------------------------------------------------------------------------

## 11.3. Loss Distribution

Biểu đồ chính của Risk Analysis.

Nên thể hiện:

``` text
Loss Density / Histogram
        │
        ├── VaR threshold
        ├── Tail region
        └── CVaR region
```

Không dùng màu sắc quá nhiều.

Tail phải được phân biệt rõ nhưng không gây cảm giác cảnh báo giả.

------------------------------------------------------------------------

## 11.4. Risk Contribution

Hiển thị:

``` text
Asset
Weight
Risk Contribution
Contribution %
```

Có thể dùng:

-   horizontal bar chart;
-   sortable table.

------------------------------------------------------------------------

## 11.5. Model Context

Hiển thị ngắn gọn:

``` text
Volatility Model
Regime Model
Distribution
Scenario Method
Scenario Count
```

Người dùng có thể mở rộng để xem assumptions.

------------------------------------------------------------------------

# 12. Screen 4 --- Scenario Lab

## Mục tiêu

Cho phép người dùng khám phá phân phối scenario thay vì chỉ nhìn summary
metrics.

## Main Components

### Scenario Distribution

-   portfolio return;
-   portfolio loss;
-   tail;
-   percentile markers.

### Scenario Table

Các trường có thể gồm:

``` text
Scenario ID
Regime
Portfolio Return
Portfolio Loss
Key Driver
```

### Filters

-   loss percentile;
-   regime;
-   asset;
-   scenario type.

### Scenario Detail

Khi chọn một scenario:

``` text
Scenario
    ↓
Portfolio Impact
    ↓
Asset Contributions
    ↓
Market State
```

------------------------------------------------------------------------

# 13. Screen 5 --- Stress Testing

## Mục tiêu

Đánh giá portfolio dưới các điều kiện bất lợi có chủ đích.

## Scenario Types

V1 có thể hỗ trợ:

-   market shock;
-   volatility shock;
-   asset shock;
-   sector shock;
-   historical crisis scenario;
-   custom scenario khi methodology hỗ trợ.

## Interaction

``` text
Select Scenario
      ↓
Configure Shock
      ↓
Run
      ↓
Compare Baseline vs Stress
```

## Result

Hiển thị:

``` text
Metric       Baseline    Stress    Change
VaR          ...         ...       ...
CVaR         ...         ...       ...
Loss         ...         ...       ...
Volatility   ...         ...       ...
```

Kèm:

-   affected assets;
-   largest contributors;
-   scenario assumptions.

------------------------------------------------------------------------

# 14. Screen 6 --- Quantum Benchmark Lab

Đây là màn hình dành cho research/technical analysis.

Không đặt Quantum benchmark làm màn hình mặc định của risk workflow.

## 14.1. Benchmark Setup

Hiển thị:

``` text
Financial Quantity
Confidence Level
Scenario / Distribution
Classical Method
Quantum Method
Quantum Backend
Shots / Queries
Noise Setting
```

------------------------------------------------------------------------

## 14.2. Comparison

Bảng chính:

  Metric                     Classical   Quantum
  ------------------------ ----------- ---------
  Estimate                         ---       ---
  Absolute Error                   ---       ---
  Relative Error                   ---       ---
  Runtime                          ---       ---
  Samples / Queries                ---       ---
  Qubits                           ---       ---
  Circuit Depth                    ---       ---
  Shots                            ---       ---
  State Preparation Cost           ---       ---
  Oracle Cost                      ---       ---

------------------------------------------------------------------------

## 14.3. Benchmark Conclusion

Kết luận phải được tạo từ experiment result.

Ví dụ:

``` text
Query-efficiency improvement observed.

No end-to-end runtime advantage
under the current simulator configuration.
```

Hoặc:

``` text
Quantum estimator achieved comparable accuracy
with lower query complexity.

Practical advantage remains unverified.
```

Không sử dụng các nhãn:

``` text
Quantum = Better
Quantum = Faster
Quantum = Superior
```

nếu benchmark không chứng minh điều đó.

------------------------------------------------------------------------

# 15. Quantum Transparency

Khi người dùng mở quantum result, UI nên cho phép xem:

``` text
Financial Quantity
        ↓
Mathematical Formulation
        ↓
State Preparation
        ↓
Oracle
        ↓
Estimator
        ↓
Measurement
```

Thông tin technical có thể được đặt trong expandable panel.

Ví dụ:

``` text
Quantum Details ▼

Qubits: 8
Depth: 184
Shots: 4096
Backend: Aer Simulator
Noise: Enabled
```

Điều này giúp Quantum không trở thành black box.

------------------------------------------------------------------------

# 16. Screen 7 --- Reports

Report phải tổng hợp được:

### Portfolio

-   holdings;
-   weights;
-   portfolio value.

### Market / Model

-   dataset;
-   period;
-   model;
-   assumptions.

### Risk

-   VaR;
-   CVaR;
-   volatility;
-   expected loss;
-   risk contribution.

### Scenarios

-   selected stress scenarios;
-   loss distribution;
-   key scenario results.

### Quantum

-   benchmark;
-   resource metrics;
-   conclusion.

Report phải phân biệt rõ:

``` text
Observed / Estimated Result
vs
Interpretation
vs
Assumption
```

------------------------------------------------------------------------

# 17. Visualization Principles

## 17.1. Loss Distribution

Biểu đồ phải ưu tiên:

-   distribution shape;
-   VaR;
-   CVaR;
-   tail.

Không nên nhồi quá nhiều annotation.

------------------------------------------------------------------------

## 17.2. Risk Contribution

Ưu tiên horizontal bar chart hoặc table.

Lý do:

-   dễ đọc tên asset;
-   dễ xếp hạng;
-   phù hợp với nhiều assets.

------------------------------------------------------------------------

## 17.3. Correlation

Correlation matrix chỉ xuất hiện khi có mục đích phân tích.

Không sử dụng heatmap chỉ vì "dashboard cần thêm chart".

------------------------------------------------------------------------

## 17.4. Scenario Comparison

Ưu tiên:

``` text
Baseline vs Stress
```

hơn là hai biểu đồ riêng biệt khó đối chiếu.

------------------------------------------------------------------------

## 17.5. Benchmark

Classical và Quantum phải được đặt cạnh nhau.

Không dùng một chart chỉ cho Quantum rồi bắt người dùng tự nhớ Classical
result.

------------------------------------------------------------------------

# 18. Color Semantics

Màu sắc phải có meaning nhất quán.

Ví dụ semantic system:

``` text
Neutral
→ normal information

Warning
→ elevated risk / model warning

Critical
→ severe risk / tail condition

Positive
→ improvement / reduction in risk

Quantum
→ technical/computational identity
```

Không sử dụng màu đỏ cho mọi risk metric.

Một metric âm không nhất thiết là "critical".

------------------------------------------------------------------------

# 19. Typography & Information Hierarchy

Ưu tiên hierarchy:

``` text
Page Title
    ↓
Section
    ↓
Primary Metric
    ↓
Supporting Metric
    ↓
Chart / Table
    ↓
Technical Detail
```

Các số quan trọng phải dễ scan.

Technical metadata không được cạnh tranh với primary risk result.

------------------------------------------------------------------------

# 20. Interaction States

Mọi màn hình có computation phải xử lý ít nhất:

``` text
Idle
Loading
Success
Warning
Error
Empty
```

## Loading

Ví dụ:

``` text
Running Risk Analysis...

Modeling market regime
Generating scenarios
Estimating risk
```

Nếu computation gồm nhiều bước, UI nên cho biết stage thay vì chỉ hiển
thị spinner.

## Success

Hiển thị timestamp / analysis context khi phù hợp.

## Warning

Ví dụ:

``` text
Insufficient historical observations
for reliable regime estimation.
```

Warning phải nói rõ:

-   vấn đề gì;
-   ảnh hưởng thế nào;
-   người dùng nên làm gì.

## Error

Không hiển thị stack trace cho end user.

Ví dụ:

``` text
Risk analysis could not be completed.

Reason:
Market data is unavailable for 2 assets.

Action:
Review portfolio data and try again.
```

## Empty

Ví dụ:

``` text
No portfolio selected.

Create or select a portfolio
to begin risk analysis.
```

------------------------------------------------------------------------

# 21. Long-Running Computation

Một số risk/quantum computation có thể mất thời gian.

UI không được giả định mọi operation hoàn thành ngay.

Với computation dài:

``` text
Queued
  ↓
Running
  ↓
Completed
  ↓
Failed
```

Nếu backend hỗ trợ progress:

``` text
Data Preparation      ✓
Risk Modeling         ✓
Scenario Generation   62%
Risk Estimation       —
```

Progress chỉ được hiển thị khi backend có thông tin đáng tin cậy.

Không giả lập progress giả chỉ để làm UI sinh động.

------------------------------------------------------------------------

# 22. Assumptions & Provenance

Risk result phải có khả năng truy ngược context.

UI nên cung cấp một khu vực:

``` text
Analysis Context
```

gồm:

``` text
Dataset
Period
Frequency
Adjustment Method
Portfolio
Confidence Level
Horizon
Scenario Count
Model
Distribution
Random Seed (nếu có)
```

Mục tiêu:

> Người dùng phải biết một risk number được tạo ra từ điều kiện nào.

------------------------------------------------------------------------

# 23. Data Freshness

Nếu dữ liệu được lấy từ external source, UI nên thể hiện:

``` text
Data Source
Last Updated
Data Period
```

Không để người dùng hiểu nhầm rằng historical dataset là real-time data.

------------------------------------------------------------------------

# 24. API / UI Boundary

UI là presentation/client layer.

Luồng:

``` text
User
  ↓
Taipy UI
  ↓
API Client
  ↓ HTTP
FastAPI
  ↓
Sigma Application / Core
  ↓
Result
  ↓
FastAPI
  ↓
API Client
  ↓
Taipy
```

UI không được:

``` text
import sigma.risk
import sigma.quantum
```

để trực tiếp thực hiện business computation.

UI chỉ:

-   collect input;
-   validate presentation-level input;
-   call API;
-   manage interaction state;
-   render result.

Business validation và financial calculation thuộc backend/core.

------------------------------------------------------------------------

# 25. Separation Between Product UI and Research UI

Sigma có hai nhóm nhu cầu:

### Product Risk UI

Dành cho:

-   Risk Analyst;
-   Portfolio Manager;
-   financial user.

Ưu tiên:

``` text
Risk
→ Scenario
→ Explanation
→ Decision Support
```

### Research / Benchmark UI

Dành cho:

-   Quant;
-   Quantum researcher;
-   technical evaluator.

Ưu tiên:

``` text
Method
→ Parameters
→ Resource
→ Accuracy
→ Benchmark
```

Hai nhóm có thể dùng cùng application nhưng không nên trộn toàn bộ
information vào một dashboard.

------------------------------------------------------------------------

# 26. Demo Experience

Competition/demo flow nên ngắn:

``` text
1. Select Demo Portfolio
        ↓
2. Run Risk Analysis
        ↓
3. Show VaR / CVaR
        ↓
4. Show Loss Distribution
        ↓
5. Open Risk Contribution
        ↓
6. Run Stress Scenario
        ↓
7. Open Quantum Benchmark
        ↓
8. Compare Classical vs Quantum
        ↓
9. Show Conclusion
```

Demo phải cho thấy:

``` text
Financial Problem
→ Risk Analysis
→ Quantum Research
→ Measured Result
```

không chỉ:

``` text
Quantum Circuit
→ Pretty Animation
```

------------------------------------------------------------------------

# 27. Responsive / Display Strategy

Sigma V1 ưu tiên desktop / large-screen experience.

Lý do:

-   nhiều bảng;
-   biểu đồ;
-   portfolio context;
-   benchmark metrics;
-   technical information.

Mobile-first không phải priority của V1.

Tuy nhiên, information hierarchy vẫn phải rõ để giao diện có thể được
chuyển sang các client khác trong tương lai.

------------------------------------------------------------------------

# 28. Accessibility & Usability

V1 phải chú ý:

-   text đủ rõ;
-   không phụ thuộc hoàn toàn vào màu sắc;
-   bảng có header rõ;
-   số liệu có unit;
-   biểu đồ có title;
-   error message có hành động rõ;
-   interactive element có trạng thái rõ.

------------------------------------------------------------------------

# 29. Future Client Independence

Taipy là reference client V1, không phải identity của Sigma Core.

Design system phải mô tả **experience và information architecture**,
không phụ thuộc vào một UI framework cụ thể.

Về dài hạn, Sigma có thể có:

``` text
                Sigma Core
                    │
                 FastAPI
                    │
       ┌────────────┼────────────┐
       │            │            │
     Taipy       Desktop       Other
     Client       Client       Client
```

Điều quan trọng là các client cùng tuân thủ:

-   information hierarchy;
-   risk terminology;
-   result semantics;
-   interaction contracts.

------------------------------------------------------------------------

# 30. Design Boundaries

`DESIGN.md` không quyết định:

-   module dependency;
-   class structure;
-   database implementation;
-   FastAPI internal architecture;
-   Qiskit implementation;
-   exact Python package configuration;
-   infrastructure deployment.

Những quyết định đó thuộc các tài liệu khác.

`DESIGN.md` chỉ định nghĩa:

``` text
Who uses Sigma
      ↓
What they need to do
      ↓
What they should see
      ↓
How they interact
      ↓
How results are communicated
```

------------------------------------------------------------------------

# 31. V1 Design Priorities

## P0

-   Portfolio Explorer.
-   Risk Analysis.
-   Loss Distribution.
-   VaR/CVaR presentation.
-   Risk Contribution.
-   Scenario/Stress Testing.
-   Clear analysis context.
-   Loading/error/empty states.

## P1

-   Quantum Benchmark Lab.
-   Classical--Quantum comparison.
-   Resource visualization.
-   Reports.

## P2

-   Advanced scenario exploration.
-   More detailed risk decomposition.
-   Richer investigation workflows.
-   Additional clients.

------------------------------------------------------------------------

# 32. Design Success Criteria

Thiết kế V1 được xem là đạt yêu cầu khi:

### Clarity

Người dùng có thể hiểu portfolio risk mà không cần đọc technical
documentation.

### Traceability

Người dùng có thể truy ngược:

``` text
Risk Result
→ Scenario
→ Model
→ Data
→ Assumption
```

ở mức phù hợp.

### Comparability

Classical và Quantum có thể được so sánh trực tiếp.

### Usability

Người dùng có thể hoàn thành core workflow mà không cần hiểu
implementation.

### Scientific Honesty

UI không exaggerate quantum performance và không biến research
hypothesis thành product claim.

### Product Identity

Sigma có cảm giác như một **professional risk intelligence system**,
không phải một notebook được đưa lên web.

------------------------------------------------------------------------

# 33. North Star Experience

Trải nghiệm cốt lõi của Sigma:

``` text
USER
  │
  ▼
PORTFOLIO
  │
  ▼
RISK OVERVIEW
  │
  ├───────────────┐
  ▼               ▼
RISK DRIVERS    LOSS DISTRIBUTION
  │               │
  └───────┬───────┘
          ▼
       SCENARIO
          │
          ▼
        STRESS
          │
          ▼
 CLASSICAL vs QUANTUM
          │
          ▼
    RISK INTELLIGENCE
          │
          ▼
   DECISION SUPPORT
```

Mục tiêu của UI không phải là hiển thị càng nhiều thông tin càng tốt.

Mục tiêu là:

> **Giúp người dùng hiểu risk, hiểu nguyên nhân, khám phá các điều kiện
> bất lợi và đánh giá một cách minh bạch giá trị của Classical và
> Quantum Computing.**

------------------------------------------------------------------------

# 34. Design North Star

> **Sigma phải nhìn và hoạt động như một Risk Intelligence Workstation:
> dense nhưng có hierarchy, technical nhưng dễ điều tra, và
> quantum-aware nhưng không quantum-hyped.**

Trải nghiệm cuối cùng cần kết nối:

``` text
Financial Understanding
        +
Risk Analysis
        +
Scenario Investigation
        +
Scientific Benchmarking
        +
Decision Support
```

→ **Sigma Risk Intelligence**
