# Sigma — Quy tắc Kỹ thuật & Nghiên cứu

**Phiên bản:** 0.2  
**Trạng thái:** Draft / Internal Baseline  
**Phạm vi:** Kỹ thuật, nghiên cứu, mô hình tài chính, Quantum, benchmark và product development  
**Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

`RULES.md` định nghĩa các nguyên tắc và ràng buộc mà Sigma phải tuân thủ trong nghiên cứu, phát triển, kiểm thử và productization.

Nếu:

```text
PRD.md
→ What / Why

DESIGN.md
→ User Experience

ARCHITECTURE.md
→ System Structure

SCHEMA.md
→ Data Meaning

RULES.md
→ Constraints & Guardrails
```

thì `RULES.md` trả lời:

> **Chúng ta phải xây dựng và đánh giá Sigma theo những nguyên tắc nào?**

Rules là **guardrails**, không phải implementation detail và không được dùng để tạo thêm abstraction hoặc infrastructure không cần thiết.

---

## 2. Thứ tự ưu tiên

Khi các yêu cầu xung đột, ưu tiên:

```text
Financial Correctness
        ↓
Scientific Validity
        ↓
Architectural Integrity
        ↓
Reproducibility
        ↓
Product Utility
        ↓
Engineering Convenience
```

Không hy sinh financial/scientific correctness chỉ để:

- code nhanh hơn;
- UI đẹp hơn;
- benchmark đẹp hơn;
- Quantum result nổi bật hơn;
- architecture trông enterprise hơn.

---

# 3. Nguyên tắc cốt lõi

## RULE-001 — Classical First

Classical methodology phải được xây dựng và kiểm chứng trước khi dùng Quantum.

```text
Financial Problem
      ↓
Classical Formulation
      ↓
Classical Baseline
      ↓
Quantum Formulation
      ↓
Fair Benchmark
```

Quantum không phải starting point chỉ vì bài toán có thể chạy trên quantum computer.

---

## RULE-002 — Quantum Where Justified

Mỗi Quantum component phải trả lời được:

1. Financial problem là gì?
2. Quantity cần tính là gì?
3. Classical baseline là gì?
4. Quantum đóng góp ở đâu?
5. Quantum overhead là gì?
6. Điều kiện nào có thể tạo ra practical value?

Nếu chưa trả lời được, không đưa Quantum vào pipeline chính.

---

## RULE-003 — Không giả định Quantum Advantage

Không được kết luận:

```text
Quantum is faster.
Quantum is better.
Quantum has advantage.
```

nếu chưa có evidence phù hợp.

Có thể có:

```text
Theoretical Query Advantage
```

nhưng điều đó không đồng nghĩa với:

```text
End-to-End Practical Advantage
```

---

## RULE-004 — Đánh giá toàn bộ pipeline

Mọi claim về computational advantage phải xem xét toàn bộ pipeline liên quan:

```text
Data Preparation
      +
Model / Distribution Construction
      +
State Preparation
      +
Oracle Construction
      +
Quantum Estimation
      +
Measurement / Post-processing
```

Nếu Classical và Quantum sử dụng pipeline khác nhau, phải ghi rõ.

Không benchmark một quantum circuit cô lập rồi dùng kết quả đó để kết luận về toàn hệ thống.

---

# 4. Quy tắc mô hình tài chính

## RULE-005 — Financial Semantics phải rõ ràng

Mọi financial quantity phải có định nghĩa thống nhất:

```text
Return
Loss
P&L
VaR
CVaR
Expected Loss
Volatility
Risk Contribution
```

Không để hai module dùng cùng một tên nhưng khác semantics.

---

## RULE-006 — Return Convention phải nhất quán

Sigma phải xác định rõ sử dụng:

```text
Simple Return
```

hoặc:

```text
Log Return
```

Nếu cần chuyển đổi, conversion phải được thực hiện và ghi nhận rõ.

Không để một module ngầm dùng log return trong khi module khác giả định simple return.

---

## RULE-007 — Loss Convention phải nhất quán

Trong từng risk workflow, phải có một loss convention rõ ràng.

Ví dụ:

```text
Loss > 0
→ Tổn thất
```

Nếu representation nội bộ dùng:

```text
P&L < 0
```

thì conversion sang loss phải explicit.

Không trộn hai convention trong cùng calculation path mà không có transformation rõ ràng.

---

## RULE-008 — Risk Result phải đi kèm Context

`VaR = X` chưa phải một result đầy đủ nếu thiếu context quan trọng.

Risk result phải có khả năng truy nguyên tới:

```text
Portfolio
Dataset
Analysis Period
Risk Horizon
Confidence Level
Model
Scenario Configuration
Method
```

---

## RULE-009 — Model Assumptions phải rõ

Mọi model quan trọng phải ghi nhận assumptions, chẳng hạn:

```text
Return Model
Volatility Model
Regime Model
Distribution
Correlation Assumption
Scenario Assumption
```

Không giấu assumptions trong implementation.

---

## RULE-010 — Model phải có Financial Justification

Không chọn model chỉ vì:

- phổ biến;
- dễ code;
- chạy nhanh;
- có sẵn trong library;
- “quant thường dùng”.

Model phải phù hợp với problem và data.

GARCH, HMM, Student-t, Monte Carlo hoặc phương pháp khác chỉ được dùng khi có statistical/financial justification.

---

# 5. Quy tắc dữ liệu

## RULE-011 — Data Provenance là bắt buộc với kết quả quan trọng

Analysis/experiment quan trọng phải biết:

```text
Source
Dataset Version
Time Range
Frequency
Adjustment Policy
Collection Time
```

Khi cần reproducibility, bổ sung metadata phù hợp như checksum hoặc snapshot identity.

---

## RULE-012 — Không tự tạo dữ liệu bị thiếu

Nếu data provider không cung cấp một field:

```text
Unavailable
```

Không tự tạo dữ liệu giả chỉ để pipeline chạy.

Nếu sử dụng preprocessing để xử lý missing data, phải ghi nhận method.

---

## RULE-013 — Chính sách Adjusted Price phải rõ

Nếu sử dụng adjusted price, phải ghi rõ:

- field được dùng;
- adjustment convention;
- data provider;
- khoảng thời gian.

Không mặc định `Close` và `Adjusted Close` là tương đương.

---

## RULE-014 — Validation trước Modeling

Không chạy risk model trực tiếp trên raw data chưa validation.

Tối thiểu kiểm tra:

```text
Asset Identity
Timestamp Ordering
Duplicates
Missing Values
Data Coverage
Portfolio Weight Validity
```

---

## RULE-015 — Demo Data và Research Data dùng cùng Data Contract

Demo dataset có thể nhỏ hơn research dataset nhưng phải tuân theo cùng logical data contract.

Không xây một pipeline giả chỉ dành cho demo nếu pipeline đó khác bản chất với research/production workflow.

---

# 6. Quy tắc Portfolio

## RULE-016 — Portfolio và Market Data là hai khái niệm riêng

Portfolio biểu diễn exposure.

Market Data biểu diễn observation.

Không trộn hai loại dữ liệu trong cùng abstraction chỉ vì đều chứa asset identifier.

---

## RULE-017 — Portfolio Weights phải được kiểm tra

Trước analysis:

```text
Weights
   ↓
Validate
   ↓
Normalize
```

Chỉ normalize khi được cấu hình rõ.

Không tự động normalize mà không thông báo hoặc ghi nhận configuration.

---

## RULE-018 — Portfolio Value và Currency phải rõ

Mọi monetary risk output phải có currency.

Không trả về:

```text
VaR = 42,000
```

mà không biết đơn vị tiền tệ.

---

# 7. Quy tắc Risk Engine

## RULE-019 — Classical Risk Engine phải độc lập

Classical Risk Analysis phải chạy được khi Quantum backend không khả dụng.

```text
Quantum Unavailable
        ↓
Classical Risk Analysis
        ↓
Still Functional
```

Quantum failure không được làm hỏng core risk capability.

---

## RULE-020 — Risk Concept độc lập với Estimator

`VaR`, `CVaR`, `Expected Loss` và các financial concepts không thuộc riêng Classical hay Quantum.

Estimator chỉ là phương pháp tính quantity.

```text
Risk Quantity
    ├── Classical Estimator
    └── Quantum Estimator
```

---

## RULE-021 — VaR và CVaR phải cùng Context

Khi so sánh VaR và CVaR, phải đảm bảo phù hợp về:

```text
Portfolio
Dataset
Horizon
Confidence Level
Scenario Context
```

---

## RULE-022 — Tail Risk phải được định lượng rõ

Khi phân tích CVaR / Expected Shortfall, phải xác định:

- tail definition;
- confidence level;
- loss convention;
- sample/scenario context.

Không dùng “tail risk” như một khái niệm không định lượng.

---

# 8. Quy tắc Scenario Generation

## RULE-023 — Scenario phải ghi rõ Method

Scenario phải phân biệt nguồn/method:

```text
Monte Carlo
Historical
Stress
Other
```

Không trộn simulated scenario và historical scenario mà không phân biệt.

---

## RULE-024 — Scenario Configuration phải tái lập được

Nếu stochastic simulation yêu cầu reproducibility, seed phải được lưu.

Cùng configuration và cùng seed phải cho phép tái lập behavior ở mức phù hợp với implementation.

---

## RULE-025 — Scenario Count là Modeling Parameter

Scenario count không được chọn tùy tiện.

Phải được xem như parameter liên quan đến accuracy/convergence.

Nếu benchmark thay đổi scenario count, phải ghi nhận thay đổi đó.

---

## RULE-026 — Scenario Generation phải có khả năng truy nguyên

Risk result phải có khả năng truy ngược, khi cần:

```text
Distribution
    ↓
Scenario Configuration
    ↓
Scenario Set
```

---

# 9. Quy tắc Regime & Distribution

## RULE-027 — Regime là Model Output

Market regime không được coi là ground truth nếu nó được suy ra bởi model.

Ví dụ:

```text
HMM
→ Inferred Regime
```

phải được phân biệt với:

```text
Historical Event Label
```

---

## RULE-028 — Regime-Aware Distribution phải giữ Conditioning

Nếu distribution phụ thuộc regime:

```text
P(Return | Regime)
```

thì regime condition phải được giữ trong model/scenario context.

Không flatten regime information mà không có justification.

---

## RULE-029 — Distribution Parameters phải truy nguyên được

Các distribution parameters quan trọng phải có thể truy nguyên tới:

```text
Model
Dataset
Fit Window
Regime
```

khi cần.

---

# 10. Quy tắc Quantum

## RULE-030 — Quantum không nhận Raw Financial Data mặc định

Quantum layer không tự nhận raw market data để “tự làm finance”.

Pipeline phải là:

```text
Raw Data
   ↓
Financial Modeling
   ↓
Financial Quantity
   ↓
Quantum Formulation
   ↓
Quantum Estimation
```

---

## RULE-031 — Quantum Problem phải có Financial Quantity

Mỗi quantum experiment phải xác định rõ quantity cần estimate.

Ví dụ:

```text
P(Loss > Threshold)
```

hoặc một expected value / tail-related quantity có formulation rõ ràng.

Không benchmark “QAE” một cách trừu tượng mà không có financial target.

---

## RULE-032 — State Preparation là một phần của Cost

Không loại state preparation khỏi cost analysis chỉ vì nó xảy ra trước circuit.

Nếu state preparation cần computational resources đáng kể, phải ghi nhận.

---

## RULE-033 — Oracle Construction là một phần của Cost

Oracle không phải free abstraction.

Nếu oracle thực hiện:

```text
Scenario
   ↓
Portfolio Loss
   ↓
Threshold Check
```

chi phí construction và execution phải được xem xét trong resource analysis.

---

## RULE-034 — Qubits, Depth và Shots phải được ghi nhận

Quantum benchmark nên ghi nhận khi phù hợp:

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

Không chỉ ghi “Quantum Estimate”.

---

## RULE-035 — Phân biệt Simulator và Hardware

Không gọi simulator result là hardware result.

Phải ghi rõ:

```text
Simulator
```

hoặc:

```text
Quantum Hardware
```

và backend cụ thể khi cần.

---

## RULE-036 — Noise phải được ghi rõ

Nếu benchmark sử dụng noise model, phải ghi nhận noise model.

Nếu không có noise:

```text
Noise: None / Ideal
```

phải được thể hiện rõ.

---

# 11. Quy tắc Classical–Quantum Benchmark

## RULE-037 — Cùng một Financial Problem

Classical và Quantum phải estimate cùng một target quantity:

```text
Same Portfolio
Same Dataset
Same Model Context
Same Quantity
Same Risk Definition
```

---

## RULE-038 — Accuracy phải Comparable

Accuracy metrics phải dùng cùng definition.

Ví dụ:

```text
Absolute Error
Relative Error
```

không được định nghĩa khác nhau giữa hai estimator.

---

## RULE-039 — Resource Metrics là First-Class Metrics

Benchmark phải xem xét:

```text
Accuracy
    +
Computational Cost
    +
Quantum Resources
    +
End-to-End Runtime
```

Không dùng runtime duy nhất.

---

## RULE-040 — Benchmark Architecture phải rõ

### Pure Classical

```text
Historical Data
      ↓
Classical Scenario Generation
      ↓
Classical Monte Carlo
```

### Naive Hybrid

```text
Historical Data
      ↓
Classical Scenarios
      ↓
Quantum State Loading
      ↓
QAE
```

### Quantum / Co-designed Architecture

```text
Historical Data
      ↓
Classical Parameter Estimation
      ↓
Quantum Scenario Distribution
      ↓
Quantum Estimation
```

Các architecture này phải được phân biệt rõ, không trộn thành một pipeline mơ hồ.

---

## RULE-041 — Không che giấu State Preparation Overhead

Nếu Classical scenario generation tạo distribution rồi Quantum load distribution vào state, chi phí đó phải được tính hoặc ít nhất báo cáo rõ trong benchmark boundary.

---

## RULE-042 — Không kết luận từ Theoretical Complexity בלבד

Ví dụ:

```text
QAE theoretical complexity = O(1/N)
MC complexity = O(1/√N)
```

không đủ để kết luận:

```text
Sigma has practical quantum advantage.
```

Cần evidence về implementation, resources và end-to-end behavior.

---

## RULE-043 — Negative Results vẫn là Valid Results

Các kết quả như:

```text
Quantum has lower query count
but higher end-to-end runtime.
```

hoặc:

```text
Classical outperforms Quantum
under current hardware/noise constraints.
```

đều là valid research outcomes.

Không thay đổi methodology chỉ để tạo quantum win.

---

# 12. Quy tắc Nghiên cứu

## RULE-044 — Hypothesis trước Experiment

Experiment quan trọng phải có:

```text
Problem
   ↓
Hypothesis
   ↓
Method
   ↓
Baseline
   ↓
Metrics
   ↓
Experiment
   ↓
Conclusion
```

Không bắt đầu bằng “chạy model xem có gì”.

---

## RULE-045 — Research và Production tách biệt

Research có thể fail, branch, thử nhiều model và chứa temporary code.

Production Core thì không.

Promotion flow:

```text
Research
   ↓
Validate
   ↓
Stabilize
   ↓
Test
   ↓
Core
```

---

## RULE-046 — Notebook không phải Production Module

Không đưa notebook trực tiếp vào runtime API.

Không copy-paste notebook logic vào nhiều nơi.

Logic reusable phải được chuyển vào `src/sigma/`.

---

## RULE-047 — Experiment phải có Configuration

Experiment quan trọng nên có configuration rõ:

```text
Dataset
Model
Parameters
Seed
Backend
Noise
Scenario Count
```

Không hard-code toàn bộ trong notebook.

---

## RULE-048 — Research Claim phải dựa trên Evidence

Phải phân biệt:

```text
Observed
Inferred
Hypothesized
```

Không trình bày hypothesis như empirical fact.

---

# 13. Quy tắc Reproducibility

## RULE-049 — Kết quả quan trọng phải tái lập được

Một result quan trọng phải có đủ metadata để người khác tái tạo experiment ở mức phù hợp.

Tối thiểu:

```text
Code Version
Dataset Version
Configuration
Model
Parameters
Seed (if applicable)
```

---

## RULE-050 — Benchmark Artifact phải giữ Context

Benchmark result không được tồn tại như một bảng số không có:

```text
Problem
Configuration
Backend
Method
Dataset
```

---

## RULE-051 — Randomness phải được kiểm soát khi cần

Randomness phải được:

- seed;
- record;
- hoặc giải thích tại sao không thể deterministic.

---

# 14. Quy tắc Kiến trúc

## RULE-052 — Modular Monolith cho V1

Sigma V1 sử dụng Modular Monolith.

Không tạo microservice chỉ để phân chia folder.

---

## RULE-053 — Domain độc lập với Framework

Domain không phụ thuộc:

```text
FastAPI
Taipy
Qiskit
UI Framework
```

nếu không có lý do kiến trúc bắt buộc.

---

## RULE-054 — UI không truy cập Core trực tiếp

Luồng chính:

```text
Taipy
   ↓
FastAPI
   ↓
Application
   ↓
Core
```

Không:

```text
Taipy
   ↓
sigma.risk
```

---

## RULE-055 — API không chứa Financial Computation

FastAPI chịu trách nhiệm:

- routing;
- request/response;
- validation;
- serialization;
- dependency wiring.

Financial computation thuộc Core.

---

## RULE-056 — Application điều phối, Engine tính toán

Application layer điều phối workflow.

Engine/module thực hiện computation.

Không để application service trở thành “god class” chứa toàn bộ financial logic.

---

## RULE-057 — Risk không phụ thuộc Quantum

Risk concepts và Classical Risk Engine phải tồn tại độc lập.

Quantum có thể cung cấp estimator phù hợp, nhưng Risk layer không được trở thành Quantum-dependent.

---

## RULE-058 — Research không trở thành Runtime Dependency

Production path:

```text
UI
   ↓
API
   ↓
Application
   ↓
Core
```

không được yêu cầu:

```text
research/
notebooks/
```

để chạy.

---

# 15. Quy tắc API

## RULE-059 — API Contract phải rõ

Request/response phải có schema rõ.

Không expose internal Python object representation một cách ngẫu nhiên.

---

## RULE-060 — API là Integration Boundary

External clients phải sử dụng API.

Ví dụ:

```text
Taipy
CLI
Future Web Client
Financial Institution Client
```

đều có thể sử dụng cùng API.

---

## RULE-061 — API trả về Product-Relevant Results

Không trả internal debugging structure cho end user chỉ vì dễ implement.

API result phải phản ánh product contract.

---

# 16. Quy tắc UI

## RULE-062 — Risk First

UI ưu tiên:

```text
Risk
  ↓
Drivers
  ↓
Scenarios
  ↓
Stress
  ↓
Quantum Benchmark
```

Không ưu tiên Quantum trước risk.

---

## RULE-063 — Không Quantum Hype trong UI

Không sử dụng:

```text
Quantum = Better
Quantum = Faster
Quantum = Superior
```

nếu benchmark không chứng minh.

---

## RULE-064 — Technical Details dùng Progressive Disclosure

UI chính chỉ hiển thị thông tin cần thiết.

Technical details có thể nằm trong:

```text
Advanced
Details
Benchmark Metadata
```

---

## RULE-065 — Error phải có hành động rõ

Error message nên trả lời:

```text
What happened?
Why?
What can the user do?
```

Không expose stack trace cho end user.

---

# 17. Quy tắc Testing & Evaluation

## RULE-066 — Test là một phần của Product

Functionality quan trọng chưa được coi là hoàn thành nếu thiếu verification phù hợp.

---

## RULE-067 — Financial Invariants phải được kiểm thử

Ví dụ:

```text
Portfolio Weights
Return Calculations
Loss Convention
VaR Ordering
CVaR Tail Relationship
Scenario Dimensions
```

---

## RULE-068 — Classical Baseline phải được kiểm thử trước Quantum Benchmark

Không benchmark Quantum trên một Classical implementation chưa được kiểm chứng.

---

## RULE-069 — Quantum Test phải tách Logic khỏi Backend

Khi có thể, kiểm tra riêng:

```text
Financial Formulation
Oracle Logic
State Preparation
Estimator
```

Không để toàn bộ correctness phụ thuộc vào một hardware/backend.

---

## RULE-070 — Evaluation khác Unit Testing

Unit tests trả lời:

> **Code có hoạt động đúng theo contract không?**

Evaluation trả lời:

> **Method có tạo ra kết quả có ý nghĩa và đáng tin không?**

Sigma cần cả hai.

---

# 18. Quy tắc Code & Dependency

## RULE-071 — Tránh Abstraction quá sớm

Không tạo:

```text
Factory
Manager
Repository
Adapter
Service
Utils
```

nếu abstraction chưa giải quyết một vấn đề thực tế.

---

## RULE-072 — Mỗi Module có một Responsibility rõ

Không tạo `utils.py` khổng lồ chỉ để chứa những thứ chưa biết đặt ở đâu.

---

## RULE-073 — Interface phải Explicit

Nếu module cần interface, contract phải rõ.

Không dùng implicit coupling thông qua global state.

---

## RULE-074 — Không Circular Dependency

Dependency cycle trong Core là architectural defect.

---

## RULE-075 — Không đưa UI Logic vào Core

Core không được biết:

```text
Taipy page
Widget
Chart
Session State
```

---

# 19. Quy tắc Configuration & Environment

## RULE-076 — Configuration không phải Business Logic

Configuration chứa parameters, không chứa algorithm implementation.

---

## RULE-077 — Secret không được vào Source Control

Không commit:

```text
API Keys
Tokens
Passwords
Credentials
```

---

## RULE-078 — Environment Differences phải rõ

Khi phù hợp, phân biệt:

```text
Local
Research
Demo
Production
```

Không hard-code environment-specific behavior trong Core.

---

# 20. Quy tắc Documentation

## RULE-079 — Documentation phải khớp Architecture

Docs phải phản ánh system thực tế.

Không để documentation mô tả một architecture mà code không tuân theo.

---

## RULE-080 — Mỗi Concern có một Source of Truth

```text
PRD
→ What / Why

DESIGN
→ Experience

ARCHITECTURE
→ Structure

SCHEMA
→ Data

RULES
→ Constraints

TECH_STACK
→ Technology

TEAM / ROLES
→ Ownership

WORKFLOW
→ Collaboration
```

Không duplicate cùng một decision ở nhiều file nếu không cần.

---

## RULE-081 — Claim phải truy nguyên được

Đối với research/scientific claim quan trọng:

```text
Claim
  ↓
Evidence
  ↓
Experiment / Source
```

---

# 21. Quy tắc Git & Thay đổi

## RULE-082 — Change phải tôn trọng Boundary

Thay đổi ảnh hưởng đến:

```text
Schema
API Contract
Architecture
Financial Methodology
Benchmark Protocol
```

phải được review ở đúng concern.

---

## RULE-083 — Không trộn các thay đổi không liên quan

Tránh gộp:

```text
Financial Model Change
+
UI Redesign
+
Dependency Migration
```

trong một change nếu không có lý do.

---

## RULE-084 — Architecture Change phải đi kèm Documentation

Nếu architecture thay đổi đáng kể, các tài liệu liên quan phải được cập nhật cùng change.

---

# 22. Quy tắc Product Scope

## RULE-085 — V1 phải tập trung

V1 tập trung:

```text
Regime-Aware Portfolio Risk
```

Không thêm feature chỉ vì “có thể làm”.

---

## RULE-086 — Feature phải có Financial Purpose

Mỗi feature mới phải trả lời:

```text
Financial Problem?
User Value?
Scientific / Technical Justification?
```

Nếu không, defer.

---

## RULE-087 — Infrastructure phải có Workload

Không thêm:

```text
Kafka
Kubernetes
Microservices
Distributed Queues
```

chỉ vì chúng phổ biến.

Infrastructure chỉ xuất hiện khi workload hoặc product requirement cần.

---

# 23. Quy tắc Quyết định

## RULE-088 — Assumption phải được nêu rõ

Khi dữ liệu hoặc requirement chưa đủ, phải ghi rõ assumption.

---

## RULE-089 — Uncertainty phải được gắn nhãn

Khi kết luận chưa được kiểm chứng, dùng nhãn phù hợp:

```text
[Giả thuyết]
[Chưa xác minh]
[Suy luận]
```

---

## RULE-090 — Strong Claim phải có Evidence

Đặc biệt với:

- quantum advantage;
- risk model superiority;
- financial performance;
- scalability;
- production readiness.

Không claim mạnh hơn evidence.

---

# 24. Definition of Done

Một feature hoặc research component quan trọng chỉ được xem là hoàn thành khi:

```text
Requirement
    ↓
Implementation
    ↓
Validation
    ↓
Tests / Evaluation
    ↓
Documentation
```

Tùy loại công việc, Definition of Done có thể cần:

- code;
- tests;
- evaluation nếu là research;
- documentation;
- reproducibility metadata.

---

# 25. Rule Exceptions

Rules có thể có exception khi có lý do chính đáng.

Exception phải:

1. được ghi nhận;
2. giải thích lý do;
3. xác định phạm vi;
4. không âm thầm phá vỡ architecture.

“Deadline gấp” không phải lý do đủ để hy sinh financial hoặc scientific correctness.

---

# 26. Khi cần quyết định nhanh

Ưu tiên:

```text
1. Không làm sai financial meaning.
2. Không làm sai scientific conclusion.
3. Không che giấu benchmark overhead.
4. Không phá architectural boundaries.
5. Không làm mất reproducibility.
6. Không over-engineer.
7. Sau đó mới tối ưu convenience.
```

---

# 27. Research Integrity

Sigma phải chấp nhận cả ba kết quả:

```text
Quantum Advantage
Quantum No Advantage
Inconclusive
```

Một research result tốt không nhất thiết là:

```text
Quantum wins.
```

Ví dụ một kết quả hợp lệ:

```text
Quantum provides theoretical query advantage,
but state preparation and oracle costs dominate
under the evaluated conditions.
```

Hoặc:

```text
Classical remains preferable under the tested
portfolio scale and hardware constraints.
```

Giá trị của Sigma nằm ở **đo lường và giải thích kết quả**, không phải ép kết quả theo narrative.

---

# 28. Nguyên tắc Kỹ thuật

> **Build the smallest system that can produce a scientifically defensible result.**

Không xây infrastructure trước khi có workload.

Không xây Quantum trước khi có financial formulation.

Không xây UI trước khi hiểu risk output.

Không benchmark Quantum trước khi có Classical baseline.

Không claim advantage trước khi có evidence.

---

# 29. Nguyên tắc Nghiên cứu

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

Đây là research loop chuẩn của Sigma.

---

# 30. Nguyên tắc Sản phẩm

> **Financial Problem First. Computational Method Second. Product Value Third.**

Sigma không xây Quantum để chứng minh Quantum.

Sigma xây Financial Risk Intelligence và sử dụng Quantum ở những nơi Quantum có thể tạo ra giá trị được đo lường.

---

# 31. North Star

```text
Financial Correctness
        +
Scientific Rigor
        +
Architectural Discipline
        +
Reproducibility
        +
Measured Quantum Value
        +
Product Utility
        ↓
SIGMA
```

> **Không hype. Không over-engineer. Không giả định advantage. Đo lường, kiểm chứng và xây dựng giá trị thực.**
