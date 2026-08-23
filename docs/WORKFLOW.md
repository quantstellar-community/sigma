# Sigma --- Workflow

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Product workflow, risk analysis workflow, research
> workflow và Classical--Quantum benchmark workflow\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`WORKFLOW.md` mô tả cách Sigma vận hành từ **financial input → modeling
→ risk estimation → benchmark → decision-support output**.

Tài liệu này trả lời:

> **Một yêu cầu phân tích rủi ro đi qua Sigma như thế nào?**

Đồng thời định nghĩa workflow nghiên cứu để Classical và Quantum được
phát triển và đánh giá theo cùng một financial problem.

Các workflow trong tài liệu này được xây dựng trên định hướng hiện tại
của Sigma: V1 là **Regime-Aware Portfolio Risk Intelligence Engine**,
với pipeline từ market data → returns/features → volatility/regime
modeling → scenario generation → loss distribution → classical/quantum
estimation → VaR/CVaR → API → dashboard. fileciteturn16file13

------------------------------------------------------------------------

# 2. Workflow Philosophy

Sigma không bắt đầu bằng:

``` text
Chọn một Quantum Algorithm
        ↓
Tìm financial problem để áp dụng
```

Sigma bắt đầu bằng:

``` text
Financial Problem
        ↓
Financial Formulation
        ↓
Classical Baseline
        ↓
Quantum Where Justified
        ↓
Fair Benchmark
        ↓
Measured Value
        ↓
Risk Intelligence
```

Đây là nguyên tắc xuyên suốt mọi workflow của Sigma.

------------------------------------------------------------------------

# 3. Product-Level Workflow

Workflow tổng thể:

``` text
Market Data
    ↓
Data Validation & Preprocessing
    ↓
Returns / Features
    ↓
Volatility & Regime Modeling
    ↓
Distribution Modeling
    ↓
Scenario Generation
    ↓
Portfolio P&L / Loss
    ↓
Loss Distribution
    ↓
Risk Estimation
    ├── Classical
    └── Quantum
    ↓
Classical–Quantum Benchmark
    ↓
Risk Intelligence
    ↓
Decision Support
    ↓
API
    ↓
Dashboard / Client
```

Trong đó Quantum là **computational enhancement layer**, không phải một
workflow thay thế toàn bộ financial modeling pipeline.

------------------------------------------------------------------------

# 4. Workflow A --- Data Preparation

## 4.1. Input

Sigma có thể nhận market data từ data provider hoặc dataset đã được
chuẩn bị.

Các dữ liệu quan trọng có thể bao gồm:

``` text
Price History
Volume / Market Variables khi cần
Portfolio Holdings / Weights
Analysis Parameters
```

------------------------------------------------------------------------

## 4.2. Validation

Trước khi modeling, data phải được kiểm tra:

``` text
Asset Identity
Timestamp Ordering
Duplicates
Missing Values
Data Coverage
Frequency
Adjustment Policy
```

Nếu dữ liệu không đạt yêu cầu:

``` text
Data
  ↓
Validation
  ↓
FAIL
  ↓
Không chạy Risk Engine
```

Không được để lỗi data silently đi vào financial model.

------------------------------------------------------------------------

## 4.3. Preprocessing

Workflow:

``` text
Raw Market Data
        ↓
Cleaning
        ↓
Alignment
        ↓
Adjustment / Transformation
        ↓
Validated Dataset
```

Return convention phải được xác định rõ.

Ví dụ:

``` text
Price
  ↓
Simple Return
```

hoặc:

``` text
Price
  ↓
Log Return
```

Không được để các module tự chọn convention khác nhau.

------------------------------------------------------------------------

# 5. Workflow B --- Return & Statistical Modeling

Sau khi data được validation:

``` text
Validated Market Data
        ↓
Returns
        ↓
Volatility
        ↓
Correlation / Covariance
        ↓
Market Dynamics
```

Các output này là nền cho risk modeling.

------------------------------------------------------------------------

## 5.1. Volatility

Sigma có thể sử dụng:

-   historical volatility;
-   conditional volatility;
-   GARCH hoặc methodology phù hợp khác.

Model được lựa chọn dựa trên financial/statistical justification, không
phải mặc định.

------------------------------------------------------------------------

## 5.2. Market Regime

Nếu sử dụng regime-aware methodology:

``` text
Returns / Volatility
        ↓
Regime Model
        ↓
Inferred Market Regime
```

Ví dụ:

``` text
Low Volatility
High Volatility
Stress
```

Regime là **model output**, không được coi là ground truth nếu được suy
ra từ dữ liệu.

------------------------------------------------------------------------

## 5.3. Distribution

Workflow:

``` text
Historical Data
        ↓
Statistical Model
        ↓
Probability Distribution
        ↓
Scenario Inputs
```

Có thể xem xét fat-tail distribution như Student-t khi dữ liệu và
methodology phù hợp.

Nếu distribution phụ thuộc regime:

``` text
P(Return | Regime)
```

thì conditioning theo regime phải được giữ trong workflow.

------------------------------------------------------------------------

# 6. Workflow C --- Portfolio Risk Context

Market distribution chưa phải portfolio risk.

Sigma phải kết hợp:

``` text
Market / Distribution Inputs
+
Portfolio Holdings / Weights
        ↓
Portfolio Return
        ↓
Portfolio P&L
        ↓
Portfolio Loss
```

Portfolio risk analysis phải xác định rõ:

``` text
Portfolio
Currency
Horizon
Confidence Level
Weights / Exposure
Model Configuration
```

------------------------------------------------------------------------

# 7. Workflow D --- Scenario Generation

Scenario generation là cầu nối giữa statistical modeling và risk
estimation.

``` text
Distribution / Market Model
        ↓
Scenario Configuration
        ↓
Scenario Set
```

Scenario có thể đến từ:

``` text
Monte Carlo
Historical Scenarios
Stress Scenarios
Other Explicitly Defined Methods
```

Các scenario phải giữ method và configuration phù hợp để có thể truy
nguyên.

------------------------------------------------------------------------

## 7.1. Monte Carlo

Workflow classical:

``` text
Distribution
      ↓
Random Sampling
      ↓
Simulated Market Scenarios
      ↓
Portfolio P&L
      ↓
Portfolio Loss
```

Số lượng scenarios là modeling parameter và cần được lựa chọn/đánh giá
dựa trên accuracy/convergence, không phải một con số tùy tiện.

------------------------------------------------------------------------

## 7.2. Stress Testing

Stress workflow:

``` text
Base Portfolio
      ↓
Stress Definition
      ↓
Market Shock
      ↓
Revaluation
      ↓
Portfolio Loss
      ↓
Risk Impact
```

Stress scenario phải được phân biệt với stochastic Monte Carlo scenario.

------------------------------------------------------------------------

# 8. Workflow E --- Loss Distribution

Sau khi scenario được tạo:

``` text
Scenario
    ↓
Portfolio Revaluation / P&L
    ↓
Loss
    ↓
Loss Distribution
```

Ví dụ conceptual:

``` text
Scenario 1 → Loss 18,500
Scenario 2 → Gain / negative loss
Scenario 3 → Loss 42,100
...
```

Từ distribution này Sigma có thể tính:

``` text
VaR
CVaR / Expected Shortfall
Expected Loss
Probability of Loss > Threshold
Worst Simulated Loss
Risk Contribution
```

Loss convention phải nhất quán trong toàn workflow.

------------------------------------------------------------------------

# 9. Workflow F --- Classical Risk Estimation

Classical Risk Engine là baseline bắt buộc.

``` text
Portfolio
    +
Scenario Set
        ↓
Portfolio Losses
        ↓
Loss Distribution
        ↓
Classical Risk Estimator
        ↓
VaR / CVaR / Other Metrics
```

Classical engine phải chạy độc lập với Quantum.

Nếu Quantum unavailable:

``` text
Quantum unavailable
        ↓
Classical Risk Analysis
        ↓
Still Functional
```

------------------------------------------------------------------------

# 10. Workflow G --- Quantum Risk Estimation

Quantum không nhận raw financial data trực tiếp.

Workflow:

``` text
Financial Data
      ↓
Financial Modeling
      ↓
Distribution / Scenario Representation
      ↓
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
Measurement / Post-processing
      ↓
Quantum Risk Estimate
```

Ví dụ financial quantity:

``` text
P(Loss > Threshold)
```

hoặc một expected value / tail quantity được formulation rõ ràng.

Quantum chỉ giải computational subproblem phù hợp.

------------------------------------------------------------------------

# 11. Workflow H --- Quantum Architecture Comparison

Sigma không chỉ benchmark:

``` text
Monte Carlo vs QAE
```

mà nên xem xét các architecture có boundary rõ.

## A. Pure Classical

``` text
Historical Data
    ↓
Classical Modeling
    ↓
Classical Scenario Generation
    ↓
Classical Monte Carlo
    ↓
VaR / CVaR
```

Đây là baseline.

------------------------------------------------------------------------

## B. Naive Hybrid

``` text
Historical Data
    ↓
Classical Modeling
    ↓
Classical Scenarios
    ↓
Quantum State Loading
    ↓
QAE / Estimator
    ↓
VaR / CVaR
```

Architecture này đặc biệt quan trọng để kiểm tra
state-preparation/loading overhead.

------------------------------------------------------------------------

## C. Quantum / Co-designed Scenario Architecture

``` text
Historical Data
    ↓
Classical Parameter Estimation
    ↓
Quantum Scenario / Distribution Representation
    ↓
Quantum Estimation
    ↓
VaR / CVaR
```

Architecture này chỉ được sử dụng khi có mathematical và computational
justification.

Mục tiêu không phải chứng minh C luôn tốt hơn A/B.

Mục tiêu là xác định:

> **Trong điều kiện nào quantum speedup có thể tồn tại sau toàn bộ
> financial pipeline?**

Tài liệu nghiên cứu Sigma cũng xác định đây là câu hỏi quan trọng hơn
việc chỉ so sánh circuit-level QAE với Monte Carlo.
fileciteturn16file5

------------------------------------------------------------------------

# 12. Workflow I --- Classical--Quantum Benchmark

Classical và Quantum phải estimate cùng một financial quantity.

``` text
                SAME FINANCIAL PROBLEM
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        Classical                Quantum
             │                       │
             ▼                       ▼
       Risk Estimate            Risk Estimate
             │                       │
             └───────────┬───────────┘
                         ▼
                     Benchmark
```

Phải giữ phù hợp:

``` text
Portfolio
Dataset
Model Context
Risk Quantity
Horizon
Confidence Level
Scenario Context
```

------------------------------------------------------------------------

## 12.1. Accuracy

Có thể ghi nhận:

``` text
Estimate
Absolute Error
Relative Error
Convergence
```

Cùng một metric definition phải được dùng cho hai phương pháp.

------------------------------------------------------------------------

## 12.2. Classical Resource Metrics

Ví dụ:

``` text
Number of Samples
Runtime
Memory
```

------------------------------------------------------------------------

## 12.3. Quantum Resource Metrics

Khi phù hợp:

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

------------------------------------------------------------------------

## 12.4. End-to-End Cost

Benchmark không được chỉ đo:

``` text
QAE circuit runtime
```

mà bỏ qua:

``` text
Data Preparation
+
State Preparation
+
Oracle
+
Quantum Estimation
+
Post-processing
```

Nếu một overhead nằm ngoài benchmark boundary, phải nói rõ.

------------------------------------------------------------------------

# 13. Workflow J --- Scientific Conclusion

Sau benchmark, Sigma phải kết luận dựa trên evidence.

Các outcome đều hợp lệ:

``` text
Quantum Advantage
Quantum No Advantage
Inconclusive
```

Ví dụ:

``` text
Theoretical query advantage observed.
No practical end-to-end runtime advantage
under the tested conditions.
```

Hoặc:

``` text
Classical remains preferable at the evaluated
portfolio scale and backend constraints.
```

Không thay đổi methodology chỉ để tạo Quantum win.

------------------------------------------------------------------------

# 14. Workflow K --- Risk Intelligence

Risk output không dừng ở một con số.

Sigma nên biến:

``` text
Risk Estimate
```

thành:

``` text
Risk Intelligence
```

Bao gồm:

``` text
Risk Summary
Risk Drivers
Scenario Impact
Stress Impact
Classical–Quantum Comparison
Uncertainty / Limitations
```

Ví dụ:

``` text
VaR 95%
CVaR 99%
Volatility
Top Risk Contributors
Worst Scenarios
Quantum Benchmark Status
```

------------------------------------------------------------------------

# 15. Workflow L --- Decision Support

Decision support có thể đưa ra insight rule-based.

Ví dụ:

``` text
Portfolio concentration is high.

NVDA contributes the largest share of tail risk.

CVaR increases materially under the volatility shock.

Quantum estimator uses fewer queries but does not
provide lower end-to-end runtime under the tested setup.
```

Đây là:

``` text
Decision Support
```

không phải:

``` text
Investment Advice
```

Sigma không biến risk analytics thành automatic trading recommendation
trong V1.

------------------------------------------------------------------------

# 16. Workflow M --- Stress Testing

Stress workflow:

``` text
User
 ↓
Select / Define Stress
 ↓
Stress Parameters
 ↓
Scenario Transformation
 ↓
Portfolio Revaluation
 ↓
Loss Distribution / Risk Impact
 ↓
Compare with Base Case
```

UI có thể cho phép custom scenario như:

``` text
Market shock
Volatility shock
Sector shock
Historical crisis scenario
```

Nhưng stress assumptions phải được hiển thị rõ.

------------------------------------------------------------------------

# 17. Workflow N --- API Product Flow

Sau khi Core computation ổn định:

``` text
Client
  ↓
FastAPI
  ↓
Application Layer
  ↓
Sigma Core
  ├── Data
  ├── Modeling
  ├── Scenarios
  ├── Risk
  └── Quantum
  ↓
Risk Result
  ↓
API Response
```

FastAPI chịu trách nhiệm integration boundary, không sở hữu financial
computation.

------------------------------------------------------------------------

# 18. Workflow O --- UI Flow

Taipy là reference client V1.

``` text
User
  ↓
Taipy
  ↓ HTTP / JSON
FastAPI
  ↓
Sigma Application
  ↓
Risk / Scenario / Quantum
  ↓
Result
  ↓
FastAPI
  ↓
Taipy
  ↓
Visualization
```

UI ưu tiên:

``` text
Risk
→ Drivers
→ Scenario
→ Stress
→ Quantum Benchmark
```

Không đặt Quantum lên trước financial risk.

Tài liệu UI của Sigma cũng định hướng một **Risk Intelligence
Workstation** với các khu vực Portfolio, Risk, Scenario, Stress, Quantum
và Classical-vs-Quantum comparison. fileciteturn16file0

------------------------------------------------------------------------

# 19. Workflow P --- Research Lifecycle

Research workflow chính thức:

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
Ablation / Resource Analysis
    ↓
Scientific Conclusion
    ↓
Engineering / Product Evaluation
```

Mỗi bước phải có output rõ.

------------------------------------------------------------------------

## 19.1. Problem

Ví dụ:

> Có thể estimate một tail-risk quantity bằng Quantum với
> computational/resource profile có ý nghĩa hơn Classical trong một điều
> kiện xác định hay không?

------------------------------------------------------------------------

## 19.2. Hypothesis

Ví dụ:

> Quantum amplitude estimation có thể giảm sample/query complexity cho
> một risk estimation problem cụ thể, nhưng practical benefit phụ thuộc
> mạnh vào state preparation, oracle và backend constraints.

Hypothesis không được trình bày như fact.

------------------------------------------------------------------------

## 19.3. Mathematical Formulation

Phải xác định:

``` text
Input
Quantity
Distribution
Threshold
Estimator
Assumptions
```

------------------------------------------------------------------------

## 19.4. Classical Baseline

Phải xây Classical baseline trước.

Ví dụ:

``` text
Monte Carlo
```

với configuration được ghi nhận.

------------------------------------------------------------------------

## 19.5. Quantum Method

Sau baseline mới triển khai:

``` text
State Preparation
Oracle
QAE / IAE / MLAE
```

theo formulation đã xác định.

------------------------------------------------------------------------

## 19.6. Fair Benchmark

Classical và Quantum phải được đánh giá trên cùng financial problem.

------------------------------------------------------------------------

## 19.7. Resource Analysis

Phải xem xét:

``` text
Accuracy
Runtime
Queries
Qubits
Depth
Shots
State Preparation
Oracle Cost
Noise
Scalability
```

------------------------------------------------------------------------

## 19.8. Scientific Conclusion

Kết luận phải trả lời:

``` text
Hypothesis supported?
Under which conditions?
What overhead dominates?
What remains uncertain?
```

------------------------------------------------------------------------

## 19.9. Product Evaluation

Cuối cùng:

``` text
Research Result
      ↓
Practical Utility
      ↓
Product Relevance
```

Một research result tốt không nhất thiết trở thành production feature.

------------------------------------------------------------------------

# 20. Workflow Q --- Research → Production

Research và production không chạy cùng boundary.

``` text
research/
    ↓
Explore
    ↓
Experiment
    ↓
Validate
    ↓
Stabilize
    ↓
Test
    ↓
src/sigma/
```

Không:

``` text
Notebook
    ↓
Copy-paste
    ↓
API
```

Research notebook có thể fail, thử nhiều phương pháp và chứa exploratory
code.

Production Core phải có:

``` text
Clear Interface
Tests
Documentation
Reproducibility
```

------------------------------------------------------------------------

# 21. Workflow R --- Error Handling

Nếu lỗi xảy ra:

``` text
Input Validation Error
        ↓
Return actionable API error
```

Nếu modeling không thể chạy:

``` text
Model Failure
        ↓
Do not produce misleading Risk Result
```

Nếu Quantum backend unavailable:

``` text
Quantum Failure
        ↓
Classical Risk Still Available
```

Nếu benchmark incomplete:

``` text
Incomplete Benchmark
        ↓
Mark as Inconclusive
```

Không biến missing result thành fabricated result.

------------------------------------------------------------------------

# 22. Workflow S --- Reproducibility

Một analysis quan trọng phải có context:

``` text
Code Version
Dataset Version
Configuration
Model
Parameters
Seed
Quantum Backend
Noise Configuration
```

khi các thông tin đó áp dụng.

Workflow:

``` text
Analysis Request
      ↓
Resolved Configuration
      ↓
Execution
      ↓
Result
      ↓
Metadata / Artifact
```

Mục tiêu là có thể truy nguyên:

``` text
Result
  ↓
Analysis
  ↓
Configuration
  ↓
Dataset / Model
```

------------------------------------------------------------------------

# 23. Workflow T --- Benchmark Artifact

Một benchmark result không được chỉ là:

``` text
Classical = 0.047
Quantum = 0.049
```

Artifact nên giữ context:

``` text
Problem
Dataset
Configuration
Classical Method
Quantum Method
Accuracy
Resource Metrics
Backend
Noise
Conclusion
```

Điều này giúp benchmark có scientific value thay vì chỉ là một bảng số.

------------------------------------------------------------------------

# 24. Workflow U --- End-to-End Example

Một analysis điển hình:

``` text
1. User selects portfolio
        ↓
2. User selects time horizon / confidence level
        ↓
3. Data is loaded
        ↓
4. Data validation
        ↓
5. Returns calculated
        ↓
6. Volatility / regime modeled
        ↓
7. Distribution constructed
        ↓
8. Scenarios generated
        ↓
9. Portfolio loss distribution calculated
        ↓
10. Classical VaR / CVaR estimated
        ↓
11. Quantum estimator optionally executed
        ↓
12. Classical–Quantum benchmark
        ↓
13. Risk intelligence generated
        ↓
14. API returns result
        ↓
15. Taipy displays risk / scenario / benchmark
```

------------------------------------------------------------------------

# 25. What Does Not Belong in the Core Workflow

Sigma V1 không đưa các hoạt động sau vào core workflow nếu chưa có
requirement:

``` text
Dynamic Volatility Targeting
Automatic Rebalancing
Dynamic Leverage
Trading Execution
Autonomous Portfolio Optimization
```

Các capability này thuộc decision/strategy layer rộng hơn và không phải
core risk measurement workflow.

------------------------------------------------------------------------

# 26. Workflow Boundaries

### Data

``` text
Source
→ Validation
→ Modeling Input
```

### Modeling

``` text
Returns
→ Volatility
→ Regime
→ Distribution
```

### Scenarios

``` text
Distribution
→ Scenario
```

### Risk

``` text
Scenario
→ Loss
→ Risk Metrics
```

### Quantum

``` text
Financial Quantity
→ Quantum Representation
→ Estimation
```

### Product

``` text
Risk Result
→ API
→ Client
```

Các boundary này phải được giữ ổn định khi implementation phát triển.

------------------------------------------------------------------------

# 27. Workflow Ownership

  Workflow                        Primary Owner                       Collaborators
  ------------------------------- ----------------------------------- -------------------
  Data Validation                 Data & Statistical Modeling         Quant
  Return / Statistical Modeling   Data & Statistical Modeling         Quant
  Financial Formulation           Quantitative Finance                Team Lead
  Scenario Generation             Classical Risk Engine               Data + Quant
  Classical Risk                  Classical Risk Engine               Quant
  Quantum Estimation              Quantum Computing                   Quant + Classical
  Benchmark                       Team Lead + Classical + Quantum     Quant
  API Integration                 Backend / Product                   Core Owners
  UI Flow                         Backend / Product                   Team
  Research Methodology            Team Lead + relevant domain owner   Team
  Product Evaluation              Team Lead + Backend / Product       Domain Owners

------------------------------------------------------------------------

# 28. Workflow Integrity Rules

Mọi workflow quan trọng phải tuân thủ:

``` text
No Unvalidated Data
No Hidden Financial Assumptions
No Unverified Strong Claims
No Quantum-Only Baseline
No Hidden State Preparation Cost
No Direct UI → Core Coupling
No Research Notebook → Production Copy-Paste
```

Các rule chi tiết nằm trong `RULES.md`.

------------------------------------------------------------------------

# 29. Workflow Decision Tree

Khi thêm một computation mới:

``` text
Is there a financial problem?
        │
       No
        ↓
      Defer
        │
       Yes
        ↓
Is financial formulation explicit?
        │
       No
        ↓
    Formulate
        │
       Yes
        ↓
Is there a Classical baseline?
        │
       No
        ↓
   Build baseline
        │
       Yes
        ↓
Does Quantum provide a justified contribution?
        │
       No ─────────→ Classical
        │
       Yes
        ↓
Can it be benchmarked fairly?
        │
       No
        ↓
   Refine protocol
        │
       Yes
        ↓
Benchmark
        ↓
Measure end-to-end cost
        ↓
Evaluate product utility
```

------------------------------------------------------------------------

# 30. Final Workflow

Workflow chuẩn của Sigma có thể rút gọn thành:

``` text
                 SIGMA WORKFLOW

Market Data
     ↓
Data Validation
     ↓
Returns / Features
     ↓
Volatility
     ↓
Market Regime
     ↓
Regime-Aware Distribution
     ↓
Scenario Generation
     ↓
Portfolio Loss Distribution
     ↓
┌───────────────────────────────┐
│                               │
▼                               ▼
Classical Risk              Quantum Risk
MC / VaR / CVaR             State / Oracle / QAE
│                               │
└───────────────┬───────────────┘
                ▼
       Classical–Quantum
           Benchmark
                ↓
         Risk Intelligence
                ↓
         Decision Support
                ↓
              API
                ↓
        Taipy / Other Client
```

------------------------------------------------------------------------

# 31. Final Research Workflow

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

Đây là workflow nghiên cứu chuẩn của Sigma.

------------------------------------------------------------------------

# 32. North Star

> **Sigma không tối ưu cho việc tạo ra một Quantum result. Sigma tối ưu
> cho việc tạo ra một Risk Intelligence result đáng tin cậy và đo lường
> được giá trị của Quantum khi Quantum thực sự có lý do để xuất hiện.**

Do đó:

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
Measured Value
        ↓
Risk Intelligence
        ↓
Product
```

→ **SIGMA WORKFLOW**
