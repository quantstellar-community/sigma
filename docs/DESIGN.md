# Sigma — Thiết kế sản phẩm

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Sản phẩm:** Sigma Risk Intelligence  
**Định hướng:** Professional Risk Intelligence Workstation  
**Reference Client V1:** Taipy  
**Product Interface:** FastAPI + Client UI

---

## 1. Mục đích

`DESIGN.md` mô tả cách người dùng tương tác với Sigma và cách hệ thống trình bày thông tin rủi ro.

Tài liệu tập trung vào:

- người dùng và nhu cầu chính;
- luồng sử dụng;
- cấu trúc thông tin;
- màn hình và thành phần giao diện;
- cách trình bày kết quả rủi ro;
- scenario và stress testing;
- Classical–Quantum benchmark;
- nguyên tắc UX/UI.

Tài liệu này không định nghĩa kiến trúc Core, schema dữ liệu, API internals, Risk Engine, Quantum implementation hoặc lựa chọn công nghệ. Các nội dung đó thuộc `ARCHITECTURE.md`, `SCHEMA.md` và `TECH_STACK.md`.

---

## 2. Định hướng trải nghiệm

Sigma không phải consumer finance app, trading app hay chatbot.

Định hướng của Sigma là **Professional Risk Intelligence Workstation**: một môi trường phân tích rủi ro chuyên nghiệp, có mật độ thông tin cao nhưng rõ ràng, minh bạch về giả định và hỗ trợ điều tra.

Nguyên tắc trải nghiệm:

- ưu tiên risk;
- tập trung vào phân tích;
- thông tin nhiều nhưng có hierarchy rõ;
- minh bạch về assumptions;
- hỗ trợ investigation;
- hạn chế trang trí không có giá trị phân tích;
- không biến Quantum thành yếu tố trình diễn.

Workflow trọng tâm:

```text
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

Sigma có thể tham khảo tinh thần của các quant/risk workstation chuyên nghiệp, nhưng không sao chép scope enterprise của chúng.

---

## 3. Nguyên tắc thiết kế

### 3.1. Risk First

Risk result luôn là thông tin ưu tiên.

Các thông tin chính gồm:

- VaR;
- CVaR;
- volatility;
- loss distribution;
- risk contribution;
- scenario impact.

Quantum benchmark là lớp phân tích bổ sung, không thay thế risk result.

### 3.2. Phân tích trước trang trí

Mọi thành phần giao diện phải có mục đích.

Không thêm:

- animation chỉ để trang trí;
- card không có information value;
- biểu đồ không trả lời câu hỏi phân tích;
- metric chỉ để làm dashboard nhiều số hơn.

### 3.3. Mật độ thông tin có kiểm soát

Sigma cần có mật độ thông tin cao hơn consumer dashboard nhưng vẫn phải dễ quét:

```text
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

### 3.4. Progressive Disclosure

Thông tin được mở dần theo nhu cầu:

```text
Risk Overview
    ↓
Risk Drivers
    ↓
Scenario
    ↓
Model Assumptions
    ↓
Technical Details
```

Người dùng không cần nhìn thấy toàn bộ tham số mô hình ngay khi mở Sigma.

### 3.5. Giải thích trước khi kết luận

Risk result cần có khả năng truy ngược về cơ sở tạo ra nó:

```text
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

### 3.6. Không tạo cảm giác chính xác giả

Một giá trị ước lượng không được trình bày như sự thật tuyệt đối.

Khi phù hợp, kết quả cần có:

- confidence level;
- horizon;
- scenario count;
- model;
- dataset;
- assumptions;
- estimation error.

### 3.7. Minh bạch về Quantum

Sigma không mặc định:

```text
Quantum = Better
```

Khi benchmark, UI cần cho phép so sánh trực tiếp:

```text
Metric                 Classical    Quantum
Estimate                  ...          ...
Error                     ...          ...
Runtime                   ...          ...
Samples / Queries         ...          ...
Qubits                    —            ...
Depth                     —            ...
Shots                     —            ...
```

Chỉ đưa ra kết luận dựa trên kết quả thực nghiệm.

### 3.8. Decision Support

Sigma hỗ trợ người dùng hiểu và đánh giá risk. Sigma V1 không tự động:

- đặt lệnh;
- rebalance;
- thay đổi leverage;
- hedge position.

UI phải phản ánh rõ ranh giới này.

---

## 4. Người dùng và nhu cầu

### Risk Analyst

Tập trung vào:

- portfolio risk;
- VaR/CVaR;
- stress testing;
- risk contribution;
- scenario analysis.

Workflow:

```text
Risk Overview
    ↓
Risk Drivers
    ↓
Scenario
    ↓
Stress
    ↓
Report
```

### Portfolio Manager

Tập trung vào:

- risk profile;
- downside;
- scenario comparison;
- concentration;
- decision support.

Workflow:

```text
Portfolio
    ↓
Risk
    ↓
Scenario
    ↓
Decision Support
```

### Quant / Risk Researcher

Tập trung vào:

- model assumptions;
- distributions;
- simulation parameters;
- Classical baseline;
- Quantum benchmark;
- resource metrics.

Workflow:

```text
Risk
    ↓
Model Details
    ↓
Benchmark
    ↓
Experiment Evidence
```

### Người dùng Demo / Competition

Mục tiêu:

- nhanh chóng hiểu Sigma;
- chọn hoặc tạo portfolio;
- chạy risk analysis;
- xem risk output;
- xem Classical–Quantum comparison.

Demo phải ngắn và không yêu cầu người dùng hiểu toàn bộ methodology nội bộ.

---

## 5. Cấu trúc thông tin

Navigation V1:

```text
SIGMA
│
├── Dashboard
├── Portfolios
├── Risk Analysis
├── Scenario Lab
├── Stress Testing
├── Quantum Benchmark
└── Reports
```

- **Dashboard:** tổng quan portfolio và risk.
- **Portfolios:** tạo, chọn và kiểm tra portfolio.
- **Risk Analysis:** phân tích risk metrics và risk drivers.
- **Scenario Lab:** khám phá scenarios và loss distribution.
- **Stress Testing:** đánh giá portfolio dưới market shocks.
- **Quantum Benchmark:** so sánh Classical và Quantum estimation.
- **Reports:** tổng hợp và xuất kết quả.

---

## 6. Global Analysis Context

Mỗi risk analysis phải giữ được context:

```text
Portfolio
Dataset
Analysis Date / Period
Risk Horizon
Confidence Level
Scenario Count
Model
```

Ví dụ:

```text
Portfolio: Balanced Growth
Dataset: Market Universe V1
Period: 2018–2025
Horizon: 10D
Confidence: 99%
Scenarios: 100,000
Model: Regime-Aware
```

Người dùng không nên phải nhớ các thiết lập này từ màn hình khác.

---

## 7. Core User Journey

```text
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

---

## 8. Dashboard

### Mục tiêu

Cung cấp snapshot nhanh về trạng thái risk hiện tại.

### Portfolio Summary

- Portfolio name;
- portfolio value;
- number of assets;
- analysis date.

### Risk KPIs

- VaR 95%;
- VaR 99%;
- CVaR 95%;
- CVaR 99%;
- volatility;
- expected loss.

### Risk Distribution

Hiển thị loss distribution cùng:

- VaR threshold;
- CVaR / tail region;
- expected loss khi phù hợp.

### Risk Contributors

```text
Asset
Weight
Risk Contribution
```

Có thể kèm scenario hoặc stress result gần nhất khi có.

---

## 9. Portfolio Explorer

### Mục tiêu

Giúp người dùng hiểu và kiểm tra portfolio trước khi chạy risk analysis.

### Thông tin đầu vào

- asset;
- ticker;
- weight;
- position;
- portfolio value.

### Validation

Cần cảnh báo:

- thiếu asset;
- duplicate asset;
- weight không hợp lệ;
- tổng weight không hợp lệ;
- thiếu market data.

Ví dụ:

```text
Total Weight: 97.0%

[!] Portfolio weights do not sum to 100%.
```

Không tự động sửa dữ liệu mà không thông báo.

### Visualization

Có thể gồm:

- allocation chart;
- weight table;
- asset summary;
- correlation preview khi có mục đích phân tích.

---

## 10. Risk Analysis

Đây là màn hình trung tâm của Sigma.

### 10.1. Cấu hình

```text
Confidence Level
Risk Horizon
Scenario Count
Market Period
Model
```

Thiết lập nâng cao đặt dưới `Advanced Configuration`.

### 10.2. Risk Summary

```text
VaR 95%
VaR 99%
CVaR 95%
CVaR 99%
Volatility
Expected Loss
```

Mỗi metric cần có giá trị, đơn vị và context về confidence/horizon; có thể kèm baseline comparison khi phù hợp.

### 10.3. Loss Distribution

Đây là visualization chính của Risk Analysis.

Nên thể hiện:

```text
Loss Distribution
       │
       ├── VaR Threshold
       ├── Tail Region
       └── CVaR Region
```

Không sử dụng quá nhiều annotation.

### 10.4. Risk Contribution

```text
Asset
Weight
Risk Contribution
Contribution %
```

Có thể dùng horizontal bar chart hoặc sortable table.

### 10.5. Model Context

Hiển thị ngắn gọn:

```text
Volatility Model
Regime Model
Distribution
Scenario Method
Scenario Count
```

Assumptions chi tiết có thể mở rộng khi cần.

---

## 11. Scenario Lab

### Mục tiêu

Cho phép người dùng khám phá phân phối scenario thay vì chỉ xem summary metrics.

### Scenario Distribution

Có thể thể hiện:

- portfolio return;
- portfolio loss;
- tail;
- percentile markers.

### Scenario Table

```text
Scenario ID
Regime
Portfolio Return
Portfolio Loss
Key Driver
```

### Filters

Có thể lọc theo:

- loss percentile;
- regime;
- asset;
- scenario type.

### Scenario Detail

```text
Scenario
    ↓
Portfolio Impact
    ↓
Asset Contributions
    ↓
Market State
```

---

## 12. Stress Testing

### Mục tiêu

Đánh giá portfolio dưới các điều kiện bất lợi có chủ đích.

### Loại scenario

V1 có thể hỗ trợ:

- market shock;
- volatility shock;
- asset shock;
- sector shock;
- historical crisis scenario;
- custom scenario khi methodology hỗ trợ.

### Workflow

```text
Select Scenario
      ↓
Configure Shock
      ↓
Run
      ↓
Compare Baseline vs Stress
```

### Kết quả

```text
Metric          Baseline    Stress    Change

VaR                 ...        ...       ...
CVaR                ...        ...       ...
Loss                ...        ...       ...
Volatility          ...        ...       ...
```

Kèm theo:

- affected assets;
- largest contributors;
- scenario assumptions.

---

## 13. Quantum Benchmark Lab

Đây là màn hình dành cho research và technical analysis, không phải màn hình mặc định của risk workflow.

### 13.1. Thiết lập

```text
Financial Quantity
Confidence Level
Scenario / Distribution
Classical Method
Quantum Method
Quantum Backend
Shots / Queries
Noise Setting
```

### 13.2. So sánh

```text
Metric                    Classical    Quantum
Estimate                     ...          ...
Absolute Error               ...          ...
Relative Error               ...          ...
Runtime                       ...          ...
Samples / Queries             ...          ...
Qubits                        ...          ...
Circuit Depth                 ...          ...
Shots                         ...          ...
State Preparation Cost        ...          ...
Oracle Cost                   ...          ...
```

Chỉ hiển thị metric có ý nghĩa đối với experiment.

### 13.3. Kết luận

Kết luận phải xuất phát từ kết quả thực nghiệm.

Ví dụ:

```text
Query-efficiency improvement observed.

No end-to-end runtime advantage
under the current simulator configuration.
```

hoặc:

```text
Quantum estimator achieved comparable accuracy
with lower query complexity.

Practical advantage remains unverified.
```

Không mặc định sử dụng các kết luận như:

```text
Quantum = Better
Quantum = Faster
Quantum = Superior
```

nếu benchmark không chứng minh điều đó.

---

## 14. Minh bạch về Quantum

Khi người dùng mở Quantum result, có thể xem:

```text
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

Thông tin kỹ thuật có thể đặt trong phần mở rộng:

```text
Quantum Details

Qubits: 8
Depth: 184
Shots: 4096
Backend: Aer Simulator
Noise: Enabled
```

Mục tiêu là giúp người dùng hiểu phép tính lượng tử thay vì biến nó thành black box.

---

## 15. Reports

Report cần tổng hợp:

### Portfolio

- holdings;
- weights;
- portfolio value.

### Market / Model

- dataset;
- period;
- model;
- assumptions.

### Risk

- VaR;
- CVaR;
- volatility;
- expected loss;
- risk contribution.

### Scenarios

- selected stress scenarios;
- loss distribution;
- key scenario results.

### Quantum

- benchmark;
- resource metrics;
- conclusion.

Kết quả cần phân biệt:

```text
Observed / Estimated Result
          vs
Interpretation
          vs
Assumption
```

---

## 16. Nguyên tắc trực quan hóa

### Loss Distribution

Ưu tiên:

- hình dạng phân phối;
- VaR;
- CVaR;
- tail.

### Risk Contribution

Ưu tiên horizontal bar chart hoặc table để dễ đọc tên asset và xếp hạng.

### Correlation

Chỉ hiển thị correlation matrix khi có mục đích phân tích rõ ràng.

### Scenario Comparison

Ưu tiên:

```text
Baseline vs Stress
```

### Benchmark

Classical và Quantum phải được đặt cạnh nhau khi so sánh.

Không yêu cầu người dùng tự nhớ Classical result.

---

## 17. Màu sắc và phân cấp thông tin

Màu sắc phải có ngữ nghĩa nhất quán:

```text
Neutral    → thông tin thông thường
Warning    → risk tăng hoặc model warning
Critical   → severe risk / tail condition
Positive   → cải thiện hoặc giảm risk
Quantum    → lớp kỹ thuật / tính toán
```

Không dùng màu đỏ cho mọi risk metric. Một metric âm không nhất thiết là trạng thái critical.

Hierarchy:

```text
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

Technical metadata không được cạnh tranh với primary risk result.

---

## 18. Trạng thái giao diện

Mọi màn hình có computation cần xử lý:

```text
Idle
Loading
Success
Warning
Error
Empty
```

### Loading

Ví dụ:

```text
Running Risk Analysis...

Modeling market regime
Generating scenarios
Estimating risk
```

Chỉ hiển thị stage khi backend cung cấp thông tin đáng tin cậy. Không giả lập progress.

### Success

Hiển thị timestamp và analysis context khi phù hợp.

### Warning

Ví dụ:

```text
Insufficient historical observations
for reliable regime estimation.
```

Warning cần nói rõ vấn đề, ảnh hưởng và hành động tiếp theo.

### Error

Không hiển thị stack trace cho end user.

```text
Risk analysis could not be completed.

Reason:
Market data is unavailable for 2 assets.

Action:
Review portfolio data and try again.
```

### Empty

```text
No portfolio selected.

Create or select a portfolio
to begin risk analysis.
```

---

## 19. Tác vụ chạy lâu

Một số risk hoặc Quantum computation có thể mất thời gian.

Trạng thái:

```text
Queued
   ↓
Running
   ↓
Completed
   ↓
Failed
```

Nếu backend có progress đáng tin cậy:

```text
Data Preparation       ✓
Risk Modeling          ✓
Scenario Generation    62%
Risk Estimation        —
```

Chỉ hiển thị progress thực tế khi backend cung cấp dữ liệu phù hợp.

---

## 20. Context, Assumptions và Provenance

Mỗi risk result cần có khả năng truy ngược context.

Khu vực `Analysis Context` có thể gồm:

```text
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
Random Seed
```

Mục tiêu:

> **Người dùng phải biết một risk number được tạo ra từ điều kiện nào.**

Nếu dữ liệu đến từ external source, nên thể hiện:

```text
Data Source
Last Updated
Data Period
```

Không để người dùng hiểu historical dataset là real-time data.

---

## 21. Ranh giới API / UI

UI là presentation và client layer.

```text
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

UI không thực hiện business computation và không import trực tiếp:

```text
sigma.risk
sigma.quantum
sigma.modeling
```

UI chỉ:

- thu thập input;
- validation ở mức giao diện;
- gọi API;
- quản lý interaction state;
- hiển thị kết quả.

Business validation và financial calculation thuộc backend/Core.

---

## 22. Product UI và Research UI

Sigma có hai nhóm nhu cầu.

### Product Risk UI

Dành cho Risk Analyst, Portfolio Manager và financial user.

```text
Risk
 ↓
Scenario
 ↓
Explanation
 ↓
Decision Support
```

### Research / Benchmark UI

Dành cho Quant, Quantum Researcher và technical evaluator.

```text
Method
 ↓
Parameters
 ↓
Resources
 ↓
Accuracy
 ↓
Benchmark
```

Hai nhóm có thể dùng cùng application nhưng không nên trộn toàn bộ thông tin vào một dashboard.

---

## 23. Demo Experience

Demo flow:

```text
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

Demo cần thể hiện:

```text
Financial Problem
      ↓
Risk Analysis
      ↓
Quantum Research
      ↓
Measured Result
```

Không biến demo thành:

```text
Quantum Circuit
      ↓
Pretty Animation
```

---

## 24. Display Strategy và khả năng sử dụng

Sigma V1 ưu tiên desktop và màn hình lớn vì cần hiển thị:

- bảng;
- biểu đồ;
- portfolio context;
- benchmark metrics;
- technical information.

Mobile-first không phải ưu tiên của V1.

Về khả năng sử dụng:

- text phải rõ;
- không phụ thuộc hoàn toàn vào màu sắc;
- bảng có header rõ;
- số liệu có đơn vị;
- biểu đồ có title;
- error message có hành động rõ;
- interactive element có trạng thái rõ.

---

## 25. Độc lập với Client

Taipy là reference client V1, không phải identity của Sigma Core.

Design mô tả **trải nghiệm và cấu trúc thông tin**, không phụ thuộc vào một UI framework cụ thể.

```text
              Sigma Core
                  │
               FastAPI
                  │
       ┌──────────┼──────────┐
       │          │          │
     Taipy     Desktop     Other
     Client     Client     Client
```

Các client cần nhất quán về:

- information hierarchy;
- risk terminology;
- result semantics;
- interaction contracts.

---

## 26. Ranh giới của tài liệu

`DESIGN.md` không quyết định:

- module dependency;
- class structure;
- database implementation;
- FastAPI internal architecture;
- Qiskit implementation;
- package configuration;
- infrastructure deployment.

Tài liệu này tập trung vào:

```text
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

---

## 27. Ưu tiên thiết kế V1

### P0 — Core Experience

- Portfolio Explorer;
- Risk Analysis;
- Loss Distribution;
- VaR/CVaR presentation;
- Risk Contribution;
- Scenario / Stress Testing;
- Analysis Context;
- Loading / Error / Empty states.

### P1 — Research & Reporting

- Quantum Benchmark Lab;
- Classical–Quantum comparison;
- resource visualization;
- Reports.

### P2 — Mở rộng

- advanced scenario exploration;
- detailed risk decomposition;
- richer investigation workflows;
- additional clients.

---

## 28. Tiêu chí thành công

### Clarity

Người dùng có thể hiểu portfolio risk mà không cần đọc technical documentation.

### Traceability

Có thể truy ngược:

```text
Risk Result
    ↓
Scenario
    ↓
Model
    ↓
Data
    ↓
Assumption
```

### Comparability

Classical và Quantum có thể được so sánh trực tiếp trên cùng financial quantity.

### Usability

Người dùng hoàn thành core workflow mà không cần hiểu implementation nội bộ.

### Scientific Honesty

UI không exaggerate Quantum performance và không biến research hypothesis thành product claim.

### Product Identity

Sigma phải tạo cảm giác như một **professional risk intelligence system**, không phải một notebook được đưa lên web.

---

## 29. North Star Experience

```text
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
RISK DRIVERS   LOSS DISTRIBUTION
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

Mục tiêu của UI không phải hiển thị càng nhiều thông tin càng tốt.

Mục tiêu là:

> **Giúp người dùng hiểu risk, hiểu nguyên nhân, khám phá các điều kiện bất lợi và đánh giá minh bạch giá trị của Classical và Quantum Computing.**

---

## Design North Star

> **Sigma phải hoạt động như một Risk Intelligence Workstation: có mật độ thông tin cao nhưng rõ ràng, có chiều sâu kỹ thuật nhưng dễ điều tra, và có Quantum nhưng không Quantum-hyped.**

Trải nghiệm cần kết nối:

```text
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
