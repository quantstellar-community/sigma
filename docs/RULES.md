# Sigma --- Engineering & Research Rules

> **Phiên bản:** 0.1\
> **Trạng thái:** Draft / Internal Baseline\
> **Phạm vi:** Engineering, Research, Financial Modeling, Quantum
> Benchmarking và Product Development\
> **Sản phẩm:** Sigma Risk Intelligence

------------------------------------------------------------------------

## 1. Mục đích

`RULES.md` định nghĩa các nguyên tắc và ràng buộc mà mọi phần của Sigma
phải tuân thủ trong quá trình nghiên cứu, phát triển, kiểm thử và
productization.

Nếu `PRD.md` trả lời **Sigma cần làm gì và tại sao**, `DESIGN.md` trả
lời **người dùng trải nghiệm Sigma như thế nào**, `ARCHITECTURE.md` trả
lời **hệ thống được cấu trúc ra sao**, và `SCHEMA.md` trả lời **dữ liệu
có ý nghĩa gì**, thì `RULES.md` trả lời:

> **Chúng ta phải xây dựng và đánh giá Sigma theo những nguyên tắc
> nào?**

Rules trong tài liệu này là các **guardrails**. Chúng không thay thế
implementation detail và không được dùng để tạo thêm abstraction không
cần thiết.

------------------------------------------------------------------------

# 2. Rule Hierarchy

Khi các yêu cầu xung đột, ưu tiên theo thứ tự:

``` text
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

Không được hy sinh financial/scientific correctness chỉ để:

-   code nhanh hơn;
-   UI đẹp hơn;
-   benchmark đẹp hơn;
-   Quantum result nổi bật hơn;
-   architecture trông enterprise hơn.

------------------------------------------------------------------------

# 3. Core Philosophy

## RULE-001 --- Classical First

Classical methodology phải được xây dựng và kiểm chứng trước khi dùng
Quantum để mở rộng bài toán.

``` text
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

Quantum không được là starting point chỉ vì bài toán có thể được biểu
diễn trên quantum computer.

------------------------------------------------------------------------

## RULE-002 --- Quantum Where Justified

Mỗi Quantum component phải trả lời được:

1.  Financial problem là gì?
2.  Quantity cần tính là gì?
3.  Classical baseline là gì?
4.  Quantum contribution nằm ở đâu?
5.  Overhead của Quantum là gì?
6.  Điều kiện nào có thể tạo ra practical value?

Nếu không trả lời được các câu hỏi trên, không đưa Quantum vào
production/research pipeline chính.

------------------------------------------------------------------------

## RULE-003 --- No Assumed Quantum Advantage

Không được viết hoặc trình bày:

``` text
Quantum is faster.
Quantum is better.
Quantum has advantage.
```

nếu chưa có evidence phù hợp.

Có thể có:

``` text
Theoretical query advantage
```

nhưng điều đó không đồng nghĩa:

``` text
End-to-end practical advantage
```

------------------------------------------------------------------------

## RULE-004 --- Measure the Whole Pipeline

Mọi claim về computational advantage phải xem xét toàn bộ pipeline liên
quan.

Tối thiểu phải cân nhắc:

``` text
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

Nếu Classical và Quantum dùng các pipeline khác nhau, phải ghi rõ sự
khác biệt.

Không được benchmark chỉ một quantum circuit rồi dùng kết quả đó để kết
luận về toàn hệ thống.

------------------------------------------------------------------------

# 4. Financial Modeling Rules

## RULE-005 --- Financial Semantics Must Be Explicit

Mọi financial quantity phải có định nghĩa rõ.

Ví dụ:

``` text
Return
Loss
P&L
VaR
CVaR
Expected Loss
Volatility
Risk Contribution
```

Không được để hai module sử dụng cùng một tên nhưng khác semantics.

------------------------------------------------------------------------

## RULE-006 --- Return Convention Must Be Consistent

Sigma phải xác định rõ return convention:

``` text
Simple Return
```

hoặc:

``` text
Log Return
```

Nếu methodology yêu cầu chuyển đổi, conversion phải explicit.

Không được để một module ngầm sử dụng log return trong khi module khác
giả định simple return.

------------------------------------------------------------------------

## RULE-007 --- Loss Convention Must Be Consistent

Sigma phải định nghĩa một loss convention duy nhất trong từng risk
workflow.

Ví dụ:

``` text
Loss > 0
```

được hiểu là tổn thất.

Nếu representation nội bộ sử dụng P&L:

``` text
P&L < 0
```

thì conversion sang loss phải explicit.

Không được trộn hai convention trong cùng calculation path mà không có
transformation rõ ràng.

------------------------------------------------------------------------

## RULE-008 --- Risk Result Must Carry Context

Không được coi:

``` text
VaR = X
```

là một result đầy đủ nếu thiếu context quan trọng.

Risk result phải có khả năng truy nguyên tới:

``` text
Portfolio
Dataset
Analysis
Risk Horizon
Confidence Level
Model
Scenario Configuration
Method
```

------------------------------------------------------------------------

## RULE-009 --- Model Assumptions Must Be Explicit

Mọi model quan trọng phải ghi nhận assumptions.

Ví dụ:

``` text
Return Model
Volatility Model
Regime Model
Distribution
Correlation Assumption
Scenario Assumption
```

Không giấu assumptions trong implementation.

------------------------------------------------------------------------

## RULE-010 --- Model Choice Requires Financial Justification

Không chọn model chỉ vì:

-   phổ biến;
-   dễ code;
-   chạy nhanh;
-   có sẵn trong library;
-   "quant thường dùng".

Model phải phù hợp với problem và data.

GARCH, HMM, Student-t, Monte Carlo hoặc model khác chỉ được dùng khi có
statistical/financial justification.

------------------------------------------------------------------------

# 5. Data Rules

## RULE-011 --- Data Provenance Is Mandatory for Important Results

Các analysis/experiment quan trọng phải biết:

``` text
Source
Dataset Version
Time Range
Frequency
Adjustment Policy
Collection Time
```

Khi cần reproducibility, phải có thêm metadata phù hợp như checksum hoặc
snapshot identity.

------------------------------------------------------------------------

## RULE-012 --- Do Not Invent Missing Data

Nếu data provider không cung cấp một field:

``` text
Unavailable
```

không được tự tạo dữ liệu giả để làm pipeline chạy.

Nếu một preprocessing step được sử dụng để xử lý missing data, method
phải được ghi nhận.

------------------------------------------------------------------------

## RULE-013 --- Adjusted Price Policy Must Be Explicit

Nếu sử dụng adjusted price, phải ghi rõ:

-   field nào được dùng;
-   adjustment convention;
-   data provider;
-   khoảng thời gian.

Không được ngầm hiểu `Close` và `Adjusted Close` là tương đương.

------------------------------------------------------------------------

## RULE-014 --- Data Validation Before Modeling

Không chạy risk model trực tiếp trên raw data chưa validation.

Tối thiểu kiểm tra:

``` text
Asset Identity
Timestamp Ordering
Duplicates
Missing Values
Data Coverage
Portfolio Weight Validity
```

------------------------------------------------------------------------

## RULE-015 --- Demo Data and Research Data Share the Same Contract

Demo dataset có thể nhỏ hơn research dataset, nhưng phải tuân theo cùng
logical data contract.

Không xây một pipeline giả chỉ dành cho demo nếu pipeline đó khác bản
chất production/research workflow.

------------------------------------------------------------------------

# 6. Portfolio Rules

## RULE-016 --- Portfolio and Market Data Are Separate Concepts

Portfolio biểu diễn exposure.

Market Data biểu diễn observation.

Không trộn hai loại dữ liệu trong cùng abstraction chỉ vì chúng đều chứa
asset identifiers.

------------------------------------------------------------------------

## RULE-017 --- Portfolio Weights Must Be Validated

Trước khi analysis:

``` text
weights
→ validate
→ normalize only if explicitly configured
```

Không tự động normalize weights mà không thông báo hoặc ghi nhận
configuration.

------------------------------------------------------------------------

## RULE-018 --- Portfolio Value and Currency Must Be Explicit

Monetary risk outputs phải có currency.

Không được trả về:

``` text
VaR = 42,000
```

mà không biết 42,000 là USD, EUR hay currency khác.

------------------------------------------------------------------------

# 7. Risk Engine Rules

## RULE-019 --- Classical Risk Engine Must Stand Alone

Classical Risk Analysis phải chạy được mà không cần Quantum backend.

``` text
Quantum unavailable
        ↓
Classical Risk Analysis
        ↓
Still functional
```

Quantum failure không được làm hỏng core risk capability.

------------------------------------------------------------------------

## RULE-020 --- Risk Concepts Are Independent of Estimator Implementation

`VaR`, `CVaR`, `Expected Loss` và các financial concepts không thuộc
riêng Classical hay Quantum.

Estimator chỉ là phương pháp tính quantity.

``` text
Risk Quantity
    ├── Classical Estimator
    └── Quantum Estimator
```

------------------------------------------------------------------------

## RULE-021 --- VaR and CVaR Must Share the Same Context

Nếu VaR và CVaR được so sánh, phải đảm bảo:

``` text
Portfolio
Dataset
Horizon
Confidence Level
Scenario Context
```

phù hợp.

------------------------------------------------------------------------

## RULE-022 --- Tail Risk Must Be Represented Explicitly

Khi phân tích CVaR/Expected Shortfall, phải xác định rõ:

-   tail definition;
-   confidence level;
-   loss convention;
-   sample/scenario context.

Không dùng từ "tail risk" như một khái niệm không định lượng.

------------------------------------------------------------------------

# 8. Scenario Generation Rules

## RULE-023 --- Scenario Generation Must Be Method-Specific

Scenario phải ghi nhận nguồn/method:

``` text
Monte Carlo
Historical
Stress
Other
```

Không trộn simulated scenario và historical scenario mà không phân biệt.

------------------------------------------------------------------------

## RULE-024 --- Scenario Configuration Must Be Reproducible

Nếu stochastic simulation sử dụng random seed và reproducibility là
requirement, seed phải được lưu.

Cùng configuration và cùng seed phải cho phép tái lập behavior ở mức phù
hợp với implementation.

------------------------------------------------------------------------

## RULE-025 --- Scenario Count Is a Modeling Parameter

Không chọn scenario count tùy tiện.

Scenario count phải được xem như một parameter của accuracy/convergence
analysis.

Nếu benchmark thay đổi scenario count, phải ghi nhận sự thay đổi.

------------------------------------------------------------------------

## RULE-026 --- Scenario Generation Must Not Be Hidden

Risk result phải có khả năng truy ngược về:

``` text
Distribution
→ Scenario Configuration
→ Scenario Set
```

khi analysis cần explainability/reproducibility.

------------------------------------------------------------------------

# 9. Regime & Distribution Rules

## RULE-027 --- Regime Is a Model Output

Market regime không được coi là ground truth nếu nó được suy ra bởi
model.

Ví dụ:

``` text
HMM
→ inferred regime
```

phải được phân biệt với:

``` text
Historical event label
```

------------------------------------------------------------------------

## RULE-028 --- Regime-Aware Distribution Must Preserve Conditioning

Nếu distribution phụ thuộc regime:

``` text
P(Return | Regime)
```

thì regime condition phải được giữ trong model/scenario context.

Không được flatten regime information mà không có justification.

------------------------------------------------------------------------

## RULE-029 --- Distribution Parameters Must Be Traceable

Các distribution parameters quan trọng phải có thể truy nguyên tới:

``` text
Model
Dataset
Fit Window
Regime
```

khi cần.

------------------------------------------------------------------------

# 10. Quantum Rules

## RULE-030 --- Quantum Does Not Receive Raw Financial Data by Default

Quantum layer không tự nhận raw market CSV để "tự làm finance".

Pipeline phải là:

``` text
Raw Data
→ Financial Modeling
→ Financial Quantity
→ Quantum Formulation
→ Quantum Estimation
```

------------------------------------------------------------------------

## RULE-031 --- Quantum Problem Must Have a Financial Quantity

Mỗi quantum experiment phải xác định rõ quantity.

Ví dụ:

``` text
P(Loss > Threshold)
```

hoặc một expected value / tail-related quantity có formulation rõ ràng.

Không benchmark "QAE" một cách trừu tượng mà không có financial target.

------------------------------------------------------------------------

## RULE-032 --- State Preparation Is Part of the Cost

Không được loại state preparation khỏi cost analysis chỉ vì nó nằm
"trước circuit".

Nếu state preparation cần computational resources đáng kể, phải ghi
nhận.

------------------------------------------------------------------------

## RULE-033 --- Oracle Construction Is Part of the Cost

Oracle không phải free abstraction.

Khi oracle thực hiện:

``` text
Scenario
→ Portfolio Loss
→ Threshold Check
```

chi phí construction và execution phải được xem xét trong resource
analysis.

------------------------------------------------------------------------

## RULE-034 --- Shots, Qubits and Depth Must Be Recorded

Quantum benchmark nên ghi nhận khi phù hợp:

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

Không chỉ ghi "Quantum estimate".

------------------------------------------------------------------------

## RULE-035 --- Hardware and Simulator Results Must Be Distinguished

Không được gọi simulator result là hardware result.

Phải ghi rõ:

``` text
Simulator
```

hoặc:

``` text
Quantum Hardware
```

và backend cụ thể khi cần.

------------------------------------------------------------------------

## RULE-036 --- Noise Must Be Explicit

Nếu benchmark sử dụng noise model:

``` text
Noise Model
```

phải được ghi nhận.

Nếu noise-free:

``` text
Noise: None / Ideal
```

phải được thể hiện rõ.

------------------------------------------------------------------------

# 11. Classical--Quantum Benchmark Rules

## RULE-037 --- Same Financial Problem

Classical và Quantum phải estimate cùng một target quantity.

``` text
Same Portfolio
Same Dataset
Same Model Context
Same Quantity
Same Risk Definition
```

------------------------------------------------------------------------

## RULE-038 --- Comparable Accuracy

Accuracy metrics phải được tính theo cùng definition.

Ví dụ:

``` text
Absolute Error
Relative Error
```

không được định nghĩa khác nhau giữa hai estimator.

------------------------------------------------------------------------

## RULE-039 --- Resource Metrics Are First-Class Metrics

Benchmark phải xem xét cả:

``` text
Accuracy
+
Computational Cost
+
Quantum Resources
+
End-to-End Runtime
```

Không dùng runtime duy nhất.

------------------------------------------------------------------------

## RULE-040 --- Benchmark Architecture Must Be Explicit

Nếu benchmark sử dụng:

### Pure Classical

``` text
Historical Data
→ Classical Scenario Generation
→ Classical Monte Carlo
```

phải ghi rõ.

### Naive Hybrid

``` text
Historical Data
→ Classical Scenarios
→ Quantum State Loading
→ QAE
```

phải ghi rõ.

### Quantum / Co-designed Scenario Architecture

``` text
Historical Data
→ Classical Parameter Estimation
→ Quantum Scenario Distribution
→ Quantum Estimation
```

phải ghi rõ.

Các architecture này không được trộn thành một pipeline mơ hồ.

------------------------------------------------------------------------

## RULE-041 --- Do Not Hide State-Preparation Overhead

Nếu Classical scenario generation tạo ra distribution rồi Quantum load
distribution vào state, cost đó phải được tính hoặc ít nhất được báo cáo
rõ trong benchmark boundary.

------------------------------------------------------------------------

## RULE-042 --- Do Not Claim Advantage from Theoretical Complexity Alone

Ví dụ:

``` text
QAE theoretical complexity = O(1/N)
MC complexity = O(1/√N)
```

không đủ để kết luận:

``` text
Sigma has practical quantum advantage.
```

Cần evidence về implementation/resource/end-to-end behavior.

------------------------------------------------------------------------

## RULE-043 --- Negative Results Are Valid Results

Các kết quả như:

``` text
Quantum has lower query count
but higher end-to-end runtime.
```

hoặc:

``` text
Classical outperforms Quantum
under current hardware/noise constraints.
```

đều là valid research outcomes.

Không được thay đổi methodology chỉ để tạo một quantum win.

------------------------------------------------------------------------

# 12. Research Rules

## RULE-044 --- Hypothesis Before Experiment

Experiment quan trọng phải có:

``` text
Problem
→ Hypothesis
→ Method
→ Baseline
→ Metrics
→ Experiment
→ Conclusion
```

Không bắt đầu bằng "chạy model xem có gì".

------------------------------------------------------------------------

## RULE-045 --- Research and Production Are Separate

Research có thể:

-   fail;
-   branch;
-   thử nhiều model;
-   chứa temporary code.

Production Core thì không.

Promotion flow:

``` text
Research
→ Validate
→ Stabilize
→ Test
→ Core
```

------------------------------------------------------------------------

## RULE-046 --- Notebooks Are Not Production Modules

Không đưa notebook trực tiếp vào runtime API.

Không copy-paste notebook logic vào nhiều nơi.

Logic reusable phải được chuyển vào `src/sigma/`.

------------------------------------------------------------------------

## RULE-047 --- Experiments Must Be Configurable

Experiment quan trọng nên có configuration rõ:

``` text
Dataset
Model
Parameters
Seed
Backend
Noise
Scenario Count
```

Không hard-code toàn bộ trong notebook.

------------------------------------------------------------------------

## RULE-048 --- Research Claims Must Be Evidence-Based

Phải phân biệt:

``` text
Observed
```

với:

``` text
Inferred
```

và:

``` text
Hypothesized
```

Không trình bày hypothesis như empirical fact.

------------------------------------------------------------------------

# 13. Reproducibility Rules

## RULE-049 --- Important Results Must Be Reproducible

Một result quan trọng phải có đủ metadata để người khác tái tạo
experiment ở mức phù hợp.

Tối thiểu:

``` text
Code Version
Dataset Version
Configuration
Model
Parameters
Seed (if applicable)
```

------------------------------------------------------------------------

## RULE-050 --- Benchmark Artifacts Must Preserve Context

Benchmark result không được tồn tại như một bảng số không có:

``` text
Problem
Configuration
Backend
Method
Dataset
```

------------------------------------------------------------------------

## RULE-051 --- Randomness Must Be Controlled When Required

Randomness phải được:

-   seed;
-   record;
-   hoặc giải thích tại sao không thể deterministic.

------------------------------------------------------------------------

# 14. Architecture Rules

## RULE-052 --- Modular Monolith for V1

Sigma V1 sử dụng Modular Monolith.

Không tạo microservice chỉ để phân chia folder.

------------------------------------------------------------------------

## RULE-053 --- Domain Must Remain Framework-Agnostic

Domain không phụ thuộc:

``` text
FastAPI
Taipy
Qiskit
UI framework
```

nếu không có lý do architectural bắt buộc.

------------------------------------------------------------------------

## RULE-054 --- UI Must Not Access Core Directly

Luồng chính:

``` text
Taipy
→ FastAPI
→ Application
→ Core
```

Không:

``` text
Taipy
→ sigma.risk
```

------------------------------------------------------------------------

## RULE-055 --- API Must Not Contain Financial Computation

FastAPI layer chịu trách nhiệm:

-   routing;
-   request/response;
-   validation;
-   serialization;
-   dependency wiring.

Financial computation thuộc Core.

------------------------------------------------------------------------

## RULE-056 --- Application Orchestrates; Engines Compute

Application layer điều phối.

Engine/module thực hiện computation.

Không để application service trở thành một "god class" chứa toàn bộ
financial logic.

------------------------------------------------------------------------

## RULE-057 --- Risk Must Not Depend on Quantum

Risk concepts và Classical Risk Engine phải tồn tại độc lập.

Quantum có thể cung cấp estimator/computational implementation phù hợp,
nhưng Risk layer không được trở thành Quantum-dependent.

------------------------------------------------------------------------

## RULE-058 --- Research Must Not Become a Runtime Dependency

Production path:

``` text
UI
→ API
→ Application
→ Core
```

không được yêu cầu:

``` text
research/
notebooks/
```

để chạy.

------------------------------------------------------------------------

# 15. API Rules

## RULE-059 --- API Contracts Must Be Explicit

Request/response phải có schema rõ.

Không expose internal Python object representation một cách ngẫu nhiên.

------------------------------------------------------------------------

## RULE-060 --- API Is the Integration Boundary

External clients phải sử dụng API.

Ví dụ:

``` text
Taipy
CLI
Future Web Client
Financial Institution Client
```

đều có thể sử dụng cùng API.

------------------------------------------------------------------------

## RULE-061 --- API Should Return Product-Relevant Results

Không trả internal debugging structure cho end user chỉ vì dễ implement.

API result phải phản ánh product contract.

------------------------------------------------------------------------

# 16. UI Rules

## RULE-062 --- Risk First

UI phải ưu tiên:

``` text
Risk
→ Drivers
→ Scenarios
→ Stress
→ Quantum Benchmark
```

không ưu tiên Quantum trước risk.

------------------------------------------------------------------------

## RULE-063 --- No Quantum Hype in UI

Không sử dụng:

``` text
Quantum = Better
Quantum = Faster
Quantum = Superior
```

nếu benchmark không chứng minh.

------------------------------------------------------------------------

## RULE-064 --- Technical Details Use Progressive Disclosure

UI chính chỉ hiển thị information cần thiết.

Technical details có thể nằm trong:

``` text
Advanced
Details
Benchmark Metadata
```

------------------------------------------------------------------------

## RULE-065 --- Errors Must Be Actionable

Error message phải nói:

``` text
What happened
Why
What user can do
```

Không expose stack trace cho end user.

------------------------------------------------------------------------

# 17. Testing Rules

## RULE-066 --- Tests Are Part of the Product

Code không được coi là hoàn thành nếu functionality quan trọng không có
verification phù hợp.

------------------------------------------------------------------------

## RULE-067 --- Financial Invariants Must Be Tested

Ví dụ:

``` text
Portfolio weights
Return calculations
Loss convention
VaR ordering
CVaR tail relationship
Scenario dimensions
```

------------------------------------------------------------------------

## RULE-068 --- Classical Baseline Must Be Tested Before Quantum Benchmark

Không benchmark Quantum trên một Classical implementation chưa được kiểm
chứng.

------------------------------------------------------------------------

## RULE-069 --- Quantum Tests Must Separate Logic from Backend

Có thể kiểm tra:

``` text
Financial formulation
Oracle logic
State preparation
Estimator
```

riêng biệt khi có thể.

Không để toàn bộ correctness phụ thuộc vào một hardware/backend.

------------------------------------------------------------------------

## RULE-070 --- Evaluation Is Not the Same as Unit Testing

Unit tests trả lời:

> Code có hoạt động đúng theo contract không?

Evaluation trả lời:

> Method có tạo ra kết quả có ý nghĩa và đáng tin không?

Sigma cần cả hai.

------------------------------------------------------------------------

# 18. Dependency & Code Quality Rules

## RULE-071 --- Avoid Premature Abstraction

Không tạo:

``` text
Factory
Manager
Repository
Adapter
Service
Utils
```

nếu abstraction chưa giải quyết một vấn đề thật.

------------------------------------------------------------------------

## RULE-072 --- One Responsibility Per Module

Module phải có responsibility rõ.

Không tạo `utils.py` khổng lồ chứa mọi thứ không biết đặt đâu.

------------------------------------------------------------------------

## RULE-073 --- Prefer Explicit Interfaces

Nếu module cần interface, contract phải rõ.

Không dùng implicit coupling thông qua global state.

------------------------------------------------------------------------

## RULE-074 --- No Circular Dependencies

Dependency cycle trong Core phải được coi là architectural defect.

------------------------------------------------------------------------

## RULE-075 --- No UI Logic in Core

Core không được biết:

``` text
Taipy page
widget
chart
session state
```

------------------------------------------------------------------------

# 19. Configuration & Environment Rules

## RULE-076 --- Configuration Is Not Business Logic

Config chứa parameters, không chứa algorithm implementation.

------------------------------------------------------------------------

## RULE-077 --- Secrets Never Enter Source Control

Không commit:

``` text
API Keys
Tokens
Passwords
Credentials
```

------------------------------------------------------------------------

## RULE-078 --- Environment Differences Must Be Explicit

Phải phân biệt khi phù hợp:

``` text
Local
Research
Demo
Production
```

Không hard-code environment-specific behavior trong Core.

------------------------------------------------------------------------

# 20. Documentation Rules

## RULE-079 --- Documentation Must Follow the Architecture

Docs phải phản ánh system thực tế.

Không để:

``` text
ARCHITECTURE.md
```

mô tả một architecture mà code hoàn toàn không tuân theo.

------------------------------------------------------------------------

## RULE-080 --- One Source of Truth per Concern

``` text
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

------------------------------------------------------------------------

## RULE-081 --- Claims Must Be Traceable

Đối với research/scientific claim quan trọng, phải biết:

``` text
Claim
→ Evidence
→ Experiment / Source
```

------------------------------------------------------------------------

# 21. Git & Change Rules

## RULE-082 --- Changes Must Respect Boundaries

Một change làm thay đổi:

``` text
Schema
API contract
Architecture
Financial methodology
Benchmark protocol
```

phải được review ở đúng concern.

------------------------------------------------------------------------

## RULE-083 --- Avoid Mixing Unrelated Changes

Không gộp:

``` text
Financial model change
+
UI redesign
+
Dependency migration
```

trong một change nếu không có lý do.

------------------------------------------------------------------------

## RULE-084 --- Documentation Changes Accompany Significant Architecture Changes

Nếu architecture thay đổi đáng kể, documentation liên quan phải được cập
nhật cùng change.

------------------------------------------------------------------------

# 22. Product Scope Rules

## RULE-085 --- V1 Must Stay Focused

V1 tập trung:

``` text
Regime-Aware Portfolio Risk
```

Không thêm feature chỉ vì "có thể làm".

------------------------------------------------------------------------

## RULE-086 --- No Feature Without Financial Purpose

Mỗi feature mới phải trả lời:

``` text
Financial problem?
User value?
Scientific/technical justification?
```

Nếu không, defer.

------------------------------------------------------------------------

## RULE-087 --- No Infrastructure Without Workload

Không thêm:

``` text
Kafka
Kubernetes
Microservices
Distributed queues
```

chỉ vì chúng phổ biến.

Infrastructure phải xuất hiện khi workload/product requirement cần.

------------------------------------------------------------------------

# 23. Decision Rules

## RULE-088 --- Explicit Assumptions

Khi dữ liệu hoặc requirement chưa đủ, phải ghi rõ assumption.

------------------------------------------------------------------------

## RULE-089 --- Uncertainty Must Be Labeled

Nếu một kết luận chưa được kiểm chứng:

``` text
[Giả thuyết]
[Chưa xác minh]
[Suy luận]
```

phải được sử dụng khi phù hợp với mức độ certainty.

------------------------------------------------------------------------

## RULE-090 --- Strong Claims Require Evidence

Đặc biệt với:

-   quantum advantage;
-   risk model superiority;
-   financial performance;
-   scalability;
-   production readiness.

Không được claim mạnh hơn evidence.

------------------------------------------------------------------------

# 24. Definition of Done

Một feature/research component quan trọng chỉ được xem là hoàn thành
khi:

``` text
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

Tùy loại work, Definition of Done phải bao gồm:

-   code;
-   tests;
-   evaluation nếu là research;
-   documentation;
-   reproducibility metadata nếu cần.

------------------------------------------------------------------------

# 25. Rule Exceptions

Rules có thể có exception khi có lý do chính đáng.

Exception phải:

1.  được ghi nhận;
2.  giải thích lý do;
3.  xác định phạm vi;
4.  không âm thầm phá vỡ architecture.

Không được dùng:

> "Deadline gấp"

làm lý do duy nhất để phá vỡ financial/scientific correctness.

------------------------------------------------------------------------

# 26. Priority of Rules

Nếu cần quyết định nhanh:

``` text
1. Không làm sai financial meaning.
2. Không làm sai scientific conclusion.
3. Không che giấu benchmark overhead.
4. Không phá architectural boundaries.
5. Không làm mất reproducibility.
6. Không over-engineer.
7. Sau đó mới tối ưu convenience.
```

------------------------------------------------------------------------

# 27. Sigma Research Integrity

Sigma phải chấp nhận cả ba kết quả:

``` text
Quantum Advantage
Quantum No Advantage
Inconclusive
```

Một research result tốt không nhất thiết là:

``` text
Quantum wins.
```

Một research result tốt có thể là:

``` text
Quantum provides theoretical query advantage,
but state preparation and oracle costs dominate
under the evaluated conditions.
```

Hoặc:

``` text
Classical remains preferable under the tested
portfolio scale and hardware constraints.
```

Giá trị của Sigma nằm ở việc **đo và giải thích** kết quả, không phải ép
kết quả theo narrative.

------------------------------------------------------------------------

# 28. Final Engineering Principle

> **Build the smallest system that can produce a scientifically
> defensible result.**

Không xây infrastructure trước khi có workload.

Không xây Quantum trước khi có financial formulation.

Không xây UI trước khi hiểu risk output.

Không benchmark Quantum trước khi có Classical baseline.

Không claim advantage trước khi có evidence.

------------------------------------------------------------------------

# 29. Final Research Principle

> **Problem → Hypothesis → Mathematical Formulation → Classical Baseline
> → Quantum Method → Fair Benchmark → Resource Analysis → Scientific
> Conclusion → Product Evaluation**

Đây là research loop chuẩn của Sigma.

------------------------------------------------------------------------

# 30. Final Product Principle

> **Financial Problem First. Computational Method Second. Product Value
> Third.**

Sigma không xây Quantum để chứng minh Quantum.

Sigma xây Financial Risk Intelligence và sử dụng Quantum tại những nơi
Quantum có thể tạo ra giá trị được đo lường.

------------------------------------------------------------------------

# 31. North Star

``` text
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

> **Không hype. Không over-engineer. Không giả định advantage. Đo lường,
> kiểm chứng và xây dựng giá trị thực.**
