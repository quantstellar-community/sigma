# Contributing to Sigma

Cảm ơn bạn đã đóng góp cho **Sigma Risk Intelligence**.

Sigma là một hệ thống Financial Risk Intelligence kết hợp Classical
Computing, Statistical Modeling, Machine Learning và Quantum Computing.
Mọi đóng góp cần ưu tiên tính đúng đắn về tài chính, tính rõ ràng của
architecture, khả năng tái lập và giá trị thực tế.

------------------------------------------------------------------------

## 1. Nguyên tắc đóng góp

Mọi thay đổi nên tuân theo:

``` text
Requirement
→ Design
→ Implementation
→ Test
→ Review
→ Documentation
```

Không thêm technology, model hoặc complexity chỉ vì chúng mới hoặc thú
vị.

Đặc biệt:

``` text
Financial Problem
→ Classical Baseline
→ Quantum Where Justified
→ Fair Benchmark
→ Measured Value
```

Quantum không được mặc định là phương án tốt hơn Classical.

------------------------------------------------------------------------

## 2. Trước khi bắt đầu

Trước khi thay đổi code, hãy đọc các tài liệu liên quan:

``` text
docs/
├── PRD.md
├── DESIGN.md
├── ARCHITECTURE.md
├── SCHEMA.md
├── RULES.md
├── TECH_STACK.md
├── TEAM.md
├── ROLES.md
└── WORKFLOW.md
```

Nếu thay đổi ảnh hưởng đến architecture, schema, rules hoặc workflow,
tài liệu tương ứng phải được cập nhật cùng thay đổi.

------------------------------------------------------------------------

## 3. Development Environment

Sigma sử dụng:

``` text
Python 3.12.x
uv
Git
```

Cài dependencies:

``` bash
uv sync
```

Chạy command trong environment:

``` bash
uv run <command>
```

Không commit:

``` text
.venv/
cache/
secrets/
API keys
local credentials
generated temporary files
```

------------------------------------------------------------------------

## 4. Branching

Khuyến nghị sử dụng branch riêng cho mỗi thay đổi:

``` text
feature/<name>
fix/<name>
research/<name>
docs/<name>
refactor/<name>
```

Không phát triển trực tiếp trên branch chính nếu thay đổi có ảnh hưởng
đáng kể.

------------------------------------------------------------------------

## 5. Code Structure

Tôn trọng các architectural boundaries của Sigma:

``` text
UI
 ↓
FastAPI
 ↓
Application
 ↓
Sigma Core
```

Không đưa financial business logic vào:

``` text
Taipy
FastAPI route
UI callbacks
```

Quantum implementation cũng phải nằm trong đúng computational boundary.

------------------------------------------------------------------------

## 6. Financial & Research Changes

Nếu thay đổi methodology, cần mô tả:

-   Problem;
-   Assumption;
-   Method;
-   Classical baseline;
-   Expected effect;
-   Evaluation method.

Đối với Quantum research, cần xem xét khi phù hợp:

``` text
State Preparation
Oracle Cost
Qubits
Circuit Depth
Shots
Noise
Runtime
Scalability
End-to-End Cost
```

Không claim **Quantum Advantage** nếu evidence chưa đủ.

Negative result là kết quả hợp lệ.

------------------------------------------------------------------------

## 7. Data Changes

Mọi thay đổi liên quan đến data phải làm rõ khi cần:

``` text
Source
Time Range
Frequency
Adjustment Policy
Data Transformation
Provenance
```

Không để data preprocessing silently thay đổi financial semantics.

------------------------------------------------------------------------

## 8. Testing

Mỗi thay đổi cần có test phù hợp.

Chạy test:

``` bash
uv run pytest
```

Các thay đổi quan trọng nên được kiểm tra ở mức:

``` text
Unit
Integration
Evaluation
```

Đặc biệt với risk calculations, cần kiểm tra cả numerical correctness và
financial interpretation.

------------------------------------------------------------------------

## 9. Code Quality

Trước khi tạo Pull Request, chạy:

``` bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

Nếu một command không áp dụng cho thay đổi hiện tại, ghi rõ trong Pull
Request.

------------------------------------------------------------------------

## 10. Documentation

Cập nhật documentation khi thay đổi:

-   public behavior;
-   API contract;
-   schema;
-   architecture;
-   workflow;
-   methodology;
-   technology;
-   team responsibility.

Documentation phải phản ánh implementation thực tế.

Không để docs và code tồn tại với hai phiên bản sự thật khác nhau.

------------------------------------------------------------------------

## 11. Commit

Commit nên nhỏ, rõ nghĩa và tập trung vào một thay đổi.

Ví dụ:

``` text
feat: add classical CVaR estimator
fix: correct portfolio loss convention
research: add QAE benchmark
docs: update risk workflow
refactor: separate scenario generation
test: add VaR edge cases
```

Không cần tuân thủ tuyệt đối một convention khác nếu repository đã thống
nhất convention riêng.

------------------------------------------------------------------------

## 12. Pull Request

Một Pull Request nên mô tả ngắn gọn:

``` text
What changed?
Why?
How was it tested?
What remains uncertain?
```

Nếu là research:

``` text
Hypothesis
Method
Baseline
Benchmark
Result
Conclusion
```

Nếu có trade-off hoặc limitation, phải ghi rõ thay vì che giấu.

------------------------------------------------------------------------

## 13. Review

Reviewer nên ưu tiên:

1.  Correctness
2.  Financial validity
3.  Architecture
4.  Tests
5.  Reproducibility
6.  Maintainability
7.  Product relevance

Code review không chỉ kiểm tra code có chạy hay không.

------------------------------------------------------------------------

## 14. Research Contributions

Research code có thể exploratory và chưa production-ready.

Tuy nhiên, khi một kết quả được đưa vào production/core, cần:

``` text
Experiment
→ Validation
→ Stable Interface
→ Tests
→ Documentation
→ Integration
```

Không copy-paste trực tiếp từ notebook vào production.

------------------------------------------------------------------------

## 15. Keep It Simple

Không thêm:

``` text
Microservice
Database
Queue
Orchestrator
Cloud Infrastructure
```

chỉ vì chúng có vẻ enterprise.

Một dependency hoặc infrastructure component mới cần có requirement thực
tế và justification rõ ràng.

------------------------------------------------------------------------

## 16. Final Principle

Mọi contributor đều giúp Sigma đạt cùng một mục tiêu:

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
```

> **Build clearly. Validate honestly. Keep the system simple. Measure
> real value.**
