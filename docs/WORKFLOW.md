# Sigma — Quy trình Vận hành

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Phạm vi:** Product workflow, risk analysis, research và Classical–Quantum benchmark  
**Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

`WORKFLOW.md` mô tả cách một yêu cầu đi qua Sigma:

```text
Financial Input
      ↓
Data Validation
      ↓
Modeling
      ↓
Scenario Generation
      ↓
Risk Estimation
      ↓
Classical / Quantum Benchmark
      ↓
Risk Intelligence
      ↓
Decision Support
      ↓
API / Client
```

Tài liệu cũng định nghĩa research workflow để Classical và Quantum được phát triển, benchmark và đánh giá trên cùng một financial problem.

Sigma V1 tập trung vào **Regime-Aware Portfolio Risk Intelligence Engine**.

---

# 2. Nguyên tắc Workflow

Sigma không bắt đầu bằng việc chọn Quantum algorithm.

```text
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

Quantum là **computational enhancement layer**, không thay thế toàn bộ financial modeling pipeline.

---

# 3. Product Workflow

Workflow tổng thể:

```text
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

---

# 4. Data Preparation

## 4.1. Input

Sigma có thể nhận market data từ data provider hoặc dataset đã chuẩn bị.

Dữ liệu chính có thể gồm:

```text
Price History
Volume / Market Variables khi cần
Portfolio Holdings / Weights
Analysis Parameters
```

## 4.2. Validation

Trước modeling, kiểm tra:

```text
Asset Identity
Timestamp Ordering
Duplicates
Missing Values
Data Coverage
Frequency
Adjustment Policy
```

Nếu validation thất bại:

```text
Data
 ↓
Validation
 ↓
FAIL
 ↓
Không chạy Risk Engine
```

Không để lỗi dữ liệu silently đi vào financial model.

## 4.3. Preprocessing

```text
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

Return convention phải được xác định rõ:

```text
Price
  ↓
Simple Return
```

hoặc:

```text
Price
  ↓
Log Return
```

Các module phải dùng cùng convention.

---

# 5. Return & Statistical Modeling

Sau validation:

```text
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

## 5.1. Volatility

Có thể sử dụng historical volatility, conditional volatility, GARCH hoặc methodology phù hợp khác.

Model phải có financial/statistical justification.

## 5.2. Market Regime

Nếu sử dụng regime-aware methodology:

```text
Returns / Volatility
      ↓
Regime Model
      ↓
Inferred Market Regime
```

Ví dụ:

```text
Low Volatility
High Volatility
Stress
```

Regime là **model output**, không phải ground truth nếu được suy ra từ dữ liệu.

## 5.3. Distribution

```text
Historical Data
      ↓
Statistical Model
      ↓
Probability Distribution
      ↓
Scenario Inputs
```

Có thể sử dụng fat-tail distribution như Student-t khi phù hợp.

Nếu distribution phụ thuộc regime:

```text
P(Return | Regime)
```

thì conditioning theo regime phải được giữ trong workflow.

---

# 6. Portfolio Risk Context

Market distribution chưa phải portfolio risk.

```text
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

Mỗi analysis phải xác định rõ:

```text
Portfolio
Currency
Horizon
Confidence Level
Weights / Exposure
Model Configuration
```

---

# 7. Scenario Generation

Scenario generation là cầu nối giữa statistical modeling và risk estimation.

```text
Distribution / Market Model
      ↓
Scenario Configuration
      ↓
Scenario Set
```

Scenario có thể đến từ:

```text
Monte Carlo
Historical Scenarios
Stress Scenarios
Other Explicitly Defined Methods
```

Method và configuration phải được lưu để có thể truy nguyên.

## 7.1. Monte Carlo

```text
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

Scenario count là modeling parameter và phải được lựa chọn/đánh giá dựa trên accuracy hoặc convergence.

## 7.2. Stress Testing

```text
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

---

# 8. Loss Distribution

```text
Scenario
    ↓
Portfolio Revaluation / P&L
    ↓
Loss
    ↓
Loss Distribution
```

Từ loss distribution, Sigma có thể tính:

```text
VaR
CVaR / Expected Shortfall
Expected Loss
Probability of Loss > Threshold
Worst Simulated Loss
Risk Contribution
```

Loss convention phải nhất quán trong toàn workflow.

---

# 9. Classical Risk Estimation

Classical Risk Engine là baseline bắt buộc.

```text
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

```text
Quantum unavailable
      ↓
Classical Risk Analysis
      ↓
Still Functional
```

---

# 10. Quantum Risk Estimation

Quantum không nhận raw financial data trực tiếp.

```text
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

```text
P(Loss > Threshold)
```

hoặc expected value / tail quantity được formulation rõ ràng.

Quantum chỉ giải computational subproblem phù hợp.

---

# 11. Quantum Architecture Comparison

Sigma cần phân biệt rõ các architecture.

## A. Pure Classical

```text
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

## B. Naive Hybrid

```text
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

Architecture này dùng để đánh giá state-preparation/loading overhead.

## C. Quantum / Co-designed Scenario Architecture

```text
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

Chỉ sử dụng khi có mathematical và computational justification.

Mục tiêu không phải chứng minh C luôn tốt hơn A/B, mà xác định:

> **Trong điều kiện nào quantum speedup có thể tồn tại sau toàn bộ financial pipeline?**

---

# 12. Classical–Quantum Benchmark

Classical và Quantum phải estimate cùng một financial quantity.

```text
            SAME FINANCIAL PROBLEM
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      Classical              Quantum
          │                     │
          ▼                     ▼
     Risk Estimate         Risk Estimate
          │                     │
          └──────────┬──────────┘
                     ▼
                 Benchmark
```

Phải giữ phù hợp:

```text
Portfolio
Dataset
Model Context
Risk Quantity
Horizon
Confidence Level
Scenario Context
```

## 12.1. Accuracy

Có thể ghi nhận:

```text
Estimate
Absolute Error
Relative Error
Convergence
```

Metric definition phải giống nhau giữa hai phương pháp.

## 12.2. Classical Resources

Ví dụ:

```text
Number of Samples
Runtime
Memory
```

## 12.3. Quantum Resources

Khi phù hợp:

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

## 12.4. End-to-End Cost

Không chỉ đo quantum circuit runtime.

Phải xem xét:

```text
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

---

# 13. Scientific Conclusion

Kết luận phải dựa trên evidence.

Ba outcome đều hợp lệ:

```text
Quantum Advantage
Quantum No Advantage
Inconclusive
```

Ví dụ:

```text
Theoretical query advantage observed.

No practical end-to-end runtime advantage
under the tested conditions.
```

hoặc:

```text
Classical remains preferable at the evaluated
portfolio scale and backend constraints.
```

Không thay đổi methodology chỉ để tạo Quantum win.

---

# 14. Risk Intelligence

Risk output không dừng ở một con số.

```text
Risk Estimate
      ↓
Risk Intelligence
```

Có thể gồm:

```text
Risk Summary
Risk Drivers
Scenario Impact
Stress Impact
Classical–Quantum Comparison
Uncertainty / Limitations
```

Ví dụ:

```text
VaR 95%
CVaR 99%
Volatility
Top Risk Contributors
Worst Scenarios
Quantum Benchmark Status
```

---

# 15. Decision Support

Decision support có thể đưa ra insight rule-based, ví dụ:

```text
Portfolio concentration is high.

NVDA contributes the largest share of tail risk.

CVaR increases materially under the volatility shock.

Quantum estimator uses fewer queries but does not
provide lower end-to-end runtime under the tested setup.
```

Đây là:

```text
Decision Support
```

không phải:

```text
Investment Advice
```

Sigma V1 không biến risk analytics thành automatic trading recommendation.

---

# 16. Stress Testing

```text
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

Có thể hỗ trợ:

```text
Market Shock
Volatility Shock
Sector Shock
Historical Crisis Scenario
```

Stress assumptions phải được hiển thị rõ.

---

# 17. API Product Flow

Sau khi Core computation ổn định:

```text
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

FastAPI là integration boundary, không sở hữu financial computation.

---

# 18. UI Flow

Taipy là reference client V1.

```text
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

```text
Risk
  ↓
Drivers
  ↓
Scenario
  ↓
Stress
  ↓
Quantum Benchmark
```

Không đặt Quantum lên trước financial risk.

---

# 19. Research Lifecycle

Research workflow chính thức:

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
Ablation / Resource Analysis
    ↓
Scientific Conclusion
    ↓
Engineering / Product Evaluation
```

## 19.1. Problem

Ví dụ:

> Có thể estimate một tail-risk quantity bằng Quantum với computational/resource profile có ý nghĩa hơn Classical trong một điều kiện xác định hay không?

## 19.2. Hypothesis

Ví dụ:

> Quantum amplitude estimation có thể giảm sample/query complexity cho một risk estimation problem cụ thể, nhưng practical benefit phụ thuộc mạnh vào state preparation, oracle và backend constraints.

Hypothesis không được trình bày như fact.

## 19.3. Mathematical Formulation

Phải xác định:

```text
Input
Quantity
Distribution
Threshold
Estimator
Assumptions
```

## 19.4. Classical Baseline

Phải xây Classical baseline trước, ví dụ Monte Carlo với configuration được ghi nhận.

## 19.5. Quantum Method

Sau baseline mới triển khai:

```text
State Preparation
Oracle
QAE / IAE / MLAE
```

theo formulation đã xác định.

## 19.6. Fair Benchmark

Classical và Quantum phải được đánh giá trên cùng financial problem.

## 19.7. Resource Analysis

Xem xét:

```text
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

## 19.8. Scientific Conclusion

Phải trả lời:

```text
Hypothesis supported?
Under which conditions?
What overhead dominates?
What remains uncertain?
```

## 19.9. Product Evaluation

```text
Research Result
      ↓
Practical Utility
      ↓
Product Relevance
```

Research result tốt không nhất thiết trở thành production feature.

---

# 20. Research → Production

Research và production có boundary khác nhau.

```text
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

```text
Notebook
    ↓
Copy-paste
    ↓
API
```

Production Core phải có:

```text
Clear Interface
Tests
Documentation
Reproducibility
```

---

# 21. Error Handling

## Input Validation Error

```text
Input Validation Error
      ↓
Actionable API Error
```

## Modeling Failure

```text
Model Failure
      ↓
Do not produce misleading Risk Result
```

## Quantum Failure

```text
Quantum Failure
      ↓
Classical Risk Still Available
```

## Incomplete Benchmark

```text
Incomplete Benchmark
      ↓
Mark as Inconclusive
```

Không biến missing result thành fabricated result.

---

# 22. Reproducibility

Analysis quan trọng phải có context phù hợp:

```text
Code Version
Dataset Version
Configuration
Model
Parameters
Seed
Quantum Backend
Noise Configuration
```

Workflow:

```text
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

Mục tiêu:

```text
Result
  ↓
Analysis
  ↓
Configuration
  ↓
Dataset / Model
```

---

# 23. Benchmark Artifact

Benchmark result không nên chỉ là:

```text
Classical = 0.047
Quantum = 0.049
```

Artifact nên giữ:

```text
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

Benchmark vì vậy có scientific value thay vì chỉ là một bảng số.

---

# 24. End-to-End Example

Một analysis điển hình:

```text
1. User selects portfolio
        ↓
2. User selects horizon / confidence level
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

---

# 25. Không thuộc Core Workflow

Sigma V1 không đưa các capability sau vào core workflow nếu chưa có requirement:

```text
Dynamic Volatility Targeting
Automatic Rebalancing
Dynamic Leverage
Trading Execution
Autonomous Portfolio Optimization
```

Đây là strategy/decision capabilities rộng hơn, không phải core risk measurement workflow.

---

# 26. Workflow Boundaries

### Data

```text
Source
  ↓
Validation
  ↓
Modeling Input
```

### Modeling

```text
Returns
  ↓
Volatility
  ↓
Regime
  ↓
Distribution
```

### Scenarios

```text
Distribution
  ↓
Scenario
```

### Risk

```text
Scenario
  ↓
Loss
  ↓
Risk Metrics
```

### Quantum

```text
Financial Quantity
  ↓
Quantum Representation
  ↓
Estimation
```

### Product

```text
Risk Result
  ↓
API
  ↓
Client
```

Các boundary này phải được giữ ổn định khi implementation phát triển.

---

# 27. Workflow Ownership

| Workflow | Primary Owner | Collaborators |
|---|---|---|
| Data Validation | Data & Statistical Modeling | Quantum |
| Return / Statistical Modeling | Data & Statistical Modeling | Quantum |
| Financial Formulation | Quantitative Finance | Team Lead |
| Scenario Generation | Classical Risk Engine | Data + Quant |
| Classical Risk | Classical Risk Engine | Quantum |
| Quantum Estimation | Quantum Computing | Quant + Classical |
| Benchmark | Team Lead + Classical + Quantum | Quant |
| API Integration | Backend / Product | Core Owners |
| UI Flow | Backend / Product | Team |
| Research Methodology | Team Lead + domain owner | Team |
| Product Evaluation | Team Lead + Backend / Product | Domain Owners |

---

# 28. Workflow Integrity Rules

Mọi workflow quan trọng phải tuân thủ:

```text
No Unvalidated Data
No Hidden Financial Assumptions
No Unverified Strong Claims
No Quantum-Only Baseline
No Hidden State Preparation Cost
No Direct UI → Core Coupling
No Research Notebook → Production Copy-Paste
```

Chi tiết nằm trong `RULES.md`.

---

# 29. Workflow Decision Tree

Khi thêm một computation mới:

```text
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

---

# 30. Sigma Workflow

```text
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
┌──────────────────────────────┐
│                              │
▼                              ▼
Classical Risk             Quantum Risk
MC / VaR / CVaR            State / Oracle / QAE
│                              │
└──────────────┬───────────────┘
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

---

# 31. Research Workflow

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

Đây là research workflow chuẩn của Sigma.

---

# 32. North Star

> **Sigma không tối ưu cho việc tạo ra một Quantum result. Sigma tối ưu cho việc tạo ra một Risk Intelligence result đáng tin cậy và đo lường được giá trị của Quantum khi Quantum thực sự có lý do để xuất hiện.**

```text
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
