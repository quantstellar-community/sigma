# Sigma — Sequence Diagram

> **Phiên bản:** 0.1  
> **Trạng thái:** Draft / Internal Baseline  
> **Phạm vi:** Risk analysis request sequence  
> **Sản phẩm:** Sigma Risk Intelligence

---

## 1. Mục đích

Diagram này mô tả **trình tự xử lý của một risk analysis request** từ client đến Sigma và ngược lại.

Trọng tâm:

```text
Request
→ Validation
→ Modeling
→ Scenario
→ Risk Estimation
→ Risk Intelligence
→ Response
```

Diagram không mô tả deployment topology hoặc chi tiết implementation nội bộ.

---

## 2. Risk Analysis Sequence

```mermaid
sequenceDiagram
    actor User as Risk Analyst / Client
    participant UI as Taipy / Client
    participant API as FastAPI
    participant APP as Application
    participant DATA as Data & Validation
    participant MODEL as Financial / Statistical Modeling
    participant SCEN as Scenario Generation
    participant CLASS as Classical Risk Engine
    participant QUANT as Quantum Risk Module
    participant RI as Risk Intelligence

    User->>UI: Cấu hình portfolio & risk analysis
    UI->>API: Gửi risk analysis request
    API->>APP: Validate & xử lý request

    APP->>DATA: Load / validate market & portfolio data
    DATA-->>APP: Validated data

    APP->>MODEL: Build returns / volatility / regime / distribution
    MODEL-->>APP: Modeling outputs

    APP->>SCEN: Generate scenarios
    SCEN-->>APP: Scenario set

    APP->>CLASS: Estimate classical risk
    CLASS-->>APP: VaR / CVaR / risk metrics

    opt Quantum analysis được yêu cầu và khả dụng
        APP->>QUANT: Estimate selected financial quantity
        QUANT-->>APP: Quantum risk result + resource metrics
    end

    APP->>RI: Combine & interpret risk results
    RI-->>APP: Risk Intelligence

    APP-->>API: Analysis result
    API-->>UI: API response
    UI-->>User: Risk Intelligence / Visualization
```

---

## 3. Sequence Stages

### 3.1. Request

```text
User
 ↓
UI / Client
 ↓
FastAPI
```

Request có thể chứa:

```text
Portfolio
Risk Horizon
Confidence Level
Analysis Configuration
Scenario Configuration
Quantum Option
```

---

### 3.2. Validation

```text
FastAPI
 ↓
Application
 ↓
Data & Validation
```

Sigma không chạy risk computation trên dữ liệu chưa được validation.

---

### 3.3. Financial Modeling

```text
Validated Data
 ↓
Returns
 ↓
Volatility
 ↓
Regime
 ↓
Distribution
```

Modeling output trở thành input cho scenario generation.

---

### 3.4. Scenario Generation

```text
Distribution
+
Portfolio Context
 ↓
Scenario Set
```

Scenario method có thể là:

```text
Monte Carlo
Historical Scenario
Stress Scenario
```

tùy analysis.

---

### 3.5. Classical Risk

```text
Scenario Set
 ↓
Portfolio Loss
 ↓
Classical Risk Engine
 ↓
VaR / CVaR / Risk Metrics
```

Classical path luôn là baseline.

---

### 3.6. Quantum Risk

Quantum chỉ được gọi khi:

```text
Quantum Analysis Requested
+
Quantum Backend Available
+
Financial Quantity Formulated
```

Sequence:

```text
Application
 ↓
Quantum Risk Module
 ↓
State Preparation
 ↓
Oracle
 ↓
Quantum Estimation
 ↓
Quantum Result
```

Quantum không thay thế Classical Risk Engine trong sequence V1.

---

### 3.7. Risk Intelligence

```text
Classical Result
        +
Quantum Result (optional)
        ↓
Risk Intelligence
```

Output có thể bao gồm:

```text
Risk Summary
VaR
CVaR
Risk Drivers
Scenario Impact
Stress Impact
Classical–Quantum Comparison
```

---

## 4. Classical-Only Sequence

Nếu Quantum không được yêu cầu hoặc không khả dụng:

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI
    participant APP as Application
    participant DATA as Data & Validation
    participant MODEL as Modeling
    participant SCEN as Scenario Generation
    participant RISK as Classical Risk Engine
    participant RI as Risk Intelligence

    C->>API: Risk analysis request
    API->>APP: Process request
    APP->>DATA: Validate data
    DATA-->>APP: Validated data
    APP->>MODEL: Build risk model
    MODEL-->>APP: Model outputs
    APP->>SCEN: Generate scenarios
    SCEN-->>APP: Scenarios
    APP->>RISK: Estimate risk
    RISK-->>APP: Risk metrics
    APP->>RI: Build risk intelligence
    RI-->>APP: Result
    APP-->>API: Response
    API-->>C: Risk Intelligence
```

Classical Risk Analysis vẫn hoạt động độc lập.

---

## 5. Quantum-Enhanced Sequence

Khi Quantum được kích hoạt:

```text
Classical Modeling
        ↓
Scenario / Financial Quantity
        ↓
Classical Risk Baseline
        +
Quantum Estimation
        ↓
Benchmark / Comparison
        ↓
Risk Intelligence
```

Quantum branch là optional.

---

## 6. Failure / Fallback

Nếu Quantum không khả dụng:

```mermaid
sequenceDiagram
    participant APP as Application
    participant CLASS as Classical Risk
    participant QUANT as Quantum Risk
    participant RI as Risk Intelligence

    APP->>CLASS: Estimate classical risk
    CLASS-->>APP: Classical result

    opt Quantum requested
        APP->>QUANT: Execute quantum estimation
        QUANT-->>APP: Failure / unavailable
    end

    APP->>RI: Use available classical result
    RI-->>APP: Risk Intelligence + limitation metadata
```

Không được tạo hoặc suy diễn Quantum result khi execution thất bại.

---

## 7. Benchmark Sequence

Khi research benchmark được thực hiện:

```mermaid
sequenceDiagram
    participant R as Researcher
    participant APP as Sigma Application
    participant CLASS as Classical Risk
    participant QUANT as Quantum Risk
    participant BENCH as Benchmark
    participant OUT as Research Result

    R->>APP: Define benchmark configuration
    APP->>CLASS: Run classical baseline
    CLASS-->>APP: Classical estimate + resources

    APP->>QUANT: Run quantum estimator
    QUANT-->>APP: Quantum estimate + resources

    APP->>BENCH: Compare results
    BENCH->>BENCH: Accuracy / runtime / resource analysis
    BENCH-->>OUT: Benchmark result

    OUT-->>R: Scientific conclusion
```

Benchmark phải giữ cùng financial problem và context phù hợp.

---

## 8. Sequence Boundaries

```text
Client
  ↓
API
  ↓
Application
  ↓
Core
  ├── Data
  ├── Modeling
  ├── Scenario
  ├── Classical Risk
  └── Quantum Risk
  ↓
Risk Intelligence
```

UI không gọi trực tiếp Core.

Quantum không bypass Application.

Classical Risk không phụ thuộc Quantum.

---

## 9. Sequence Principles

### Validation First

```text
Request
 ↓
Validation
 ↓
Computation
```

### Classical First

```text
Classical Baseline
 ↓
Quantum Comparison
```

### Quantum Optional

```text
Quantum Available?
   ├── No  → Classical
   └── Yes → Classical + Quantum
```

### No Hidden Failure

Nếu một branch thất bại, trạng thái phải được phản ánh trong result metadata.

### No Fake Result

Không sinh kết quả từ một computation chưa thực sự chạy.

---

## 10. North Star

> **Một risk analysis request phải đi qua một sequence có thể truy nguyên từ request → data → model → scenario → risk → intelligence → response.**

```text
Request
  ↓
Validate
  ↓
Model
  ↓
Scenario
  ↓
Risk
  ↓
Benchmark (optional)
  ↓
Risk Intelligence
  ↓
Response
```
