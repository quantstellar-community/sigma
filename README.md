# Sigma

## Hybrid Quantum-Classical Risk Intelligence

Sigma là một dự án nghiên cứu và kỹ thuật nhằm xây dựng **Financial Risk
Intelligence Engine** kết hợp mô hình tài chính, phương pháp thống kê,
tính toán cổ điển và tính toán lượng tử.

Mục tiêu của Sigma không phải sử dụng Quantum chỉ vì Quantum, mà là xây
dựng một hệ thống phân tích rủi ro có khả năng:

``` text
Dữ liệu tài chính
        ↓
Mô hình hóa tài chính
        ↓
Sinh kịch bản
        ↓
Phân phối lãi/lỗ của danh mục
        ↓
VaR / CVaR / Stress Testing
        ↓
Đánh giá Classical – Quantum
        ↓
Risk Intelligence
        ↓
Hỗ trợ ra quyết định
```

> **Triết lý:** Classical First → Quantum Where Justified → Fair
> Benchmark → Measure Real Value

**Trạng thái:** Sigma đang ở giai đoạn phát triển nền tảng và nghiên
cứu. Kiến trúc, quy trình phân tích và các thành phần cốt lõi được phát
triển từng bước hướng tới một hệ thống có thể kiểm chứng, mở rộng và
tích hợp.

------------------------------------------------------------------------

## Tổng quan

Tài chính là bài toán ra quyết định dưới điều kiện không chắc chắn.
Sigma tập trung vào việc biến dữ liệu thị trường và thông tin danh mục
thành những chỉ số và phân tích rủi ro có thể giải thích được.

Sigma hướng tới việc giúp trả lời các câu hỏi như:

-   Danh mục hiện đang chịu những loại rủi ro nào?
-   Những kịch bản nào có thể tạo ra tổn thất lớn?
-   Rủi ro ở phần đuôi của phân phối lớn đến mức nào?
-   Những tài sản hoặc yếu tố nào đóng góp nhiều nhất vào rủi ro?
-   Phương pháp Classical và Quantum khác nhau thế nào về độ chính xác,
    chi phí tính toán và tính khả thi thực tế?

Quantum được xem là **lớp tăng cường tính toán**, không phải bản chất
duy nhất của sản phẩm.

------------------------------------------------------------------------

## Mục tiêu và nguyên tắc

Sigma được phát triển theo các nguyên tắc sau.

### Classical First

Mọi phương pháp Quantum phải có phương pháp Classical phù hợp để làm cơ
sở so sánh.

### Quantum Where Justified

Quantum chỉ được sử dụng khi có một bài toán tài chính rõ ràng và có lý
do hợp lý để nghiên cứu đóng góp của Quantum.

### Fair Benchmark

Classical và Quantum phải được đánh giá trên cùng bài toán tài chính, dữ
liệu, danh mục, mức tin cậy, thời hạn và các điều kiện thực nghiệm phù
hợp.

### Không tuyên bố Quantum Advantage khi chưa đủ bằng chứng

Không coi theoretical speedup hoặc kết quả ở cấp độ mạch lượng tử là
bằng chứng cho quantum advantage của toàn bộ hệ thống.

Khi đánh giá Quantum, cần xem xét cả:

-   Độ chính xác
-   Thời gian chạy
-   Chi phí lấy mẫu hoặc truy vấn
-   Chi phí chuẩn bị trạng thái
-   Chi phí oracle
-   Số qubit
-   Độ sâu mạch
-   Số shots
-   Ảnh hưởng của nhiễu
-   Khả năng mở rộng

### Tái lập được

Kết quả nghiên cứu và kết quả phân tích rủi ro cần có đủ thông tin để
truy nguyên về:

``` text
Dữ liệu
   ↓
Mô hình
   ↓
Cấu hình
   ↓
Phiên bản mã nguồn
   ↓
Thí nghiệm
```

### Giá trị thực tế

Một phương pháp chỉ có ý nghĩa đối với sản phẩm khi nó tạo ra giá trị
thực tế có thể đo lường, không chỉ tạo ra một minh họa kỹ thuật.

------------------------------------------------------------------------

# Sigma V1

## Regime-Aware Portfolio Risk Intelligence Engine

Phạm vi chính của Sigma V1 là xây dựng một **Regime-Aware Portfolio Risk
Intelligence Engine**.

Hệ thống tập trung vào phân tích rủi ro danh mục, mô phỏng các kịch bản
thị trường và ước lượng các đại lượng rủi ro như VaR và CVaR.

### Quy trình tổng quát

``` text
Dữ liệu thị trường + Danh mục
            ↓
       Kiểm tra dữ liệu
            ↓
      Returns / Features
            ↓
  Mô hình hóa Volatility
       và Market Regime
            ↓
   Phân phối theo Regime
            ↓
      Sinh kịch bản
            ↓
   Phân phối lãi/lỗ danh mục
            ↓
    ┌────────┴────────┐
    ↓                 ↓
Classical          Quantum
Risk Engine        Risk Module
    ↓                 ↓
    └────────┬────────┘
             ↓
  Đánh giá Classical – Quantum
             ↓
 VaR / CVaR / Stress / Risk Intelligence
             ↓
            API
             ↓
       Taipy / Client
```

### Đầu vào

Sigma V1 có thể sử dụng:

-   Dữ liệu giá hoặc lợi suất lịch sử;
-   Mã tài sản và thời gian;
-   Vị thế hoặc tỷ trọng danh mục;
-   Ngày định giá;
-   Thời hạn rủi ro;
-   Mức tin cậy;
-   Cấu hình sinh kịch bản;
-   Cấu hình mô hình.

### Đầu ra

Sigma V1 tập trung vào:

-   Phân phối lãi/lỗ của danh mục;
-   VaR;
-   CVaR / Expected Shortfall;
-   Expected Loss;
-   Kết quả stress testing;
-   Risk Contribution;
-   Phân tích kịch bản;
-   Thông tin mô hình và cấu hình;
-   Kết quả đánh giá Classical -- Quantum khi có áp dụng.

------------------------------------------------------------------------

# Kiến trúc

Sigma V1 được tổ chức theo hướng **modular monolith** và **API-first**.

``` mermaid
flowchart LR
    A["Market Data + Portfolio"] --> B["Data Validation"]
    B --> C["Financial Modeling"]
    C --> D["Regime-Aware Distribution"]
    D --> E["Scenario Generation"]
    E --> F["Classical Risk Engine"]
    E --> G["Quantum Risk Module"]
    F --> H["Risk Intelligence"]
    G --> H
    H --> I["FastAPI"]
    I --> J["Taipy / Client"]
```

Ranh giới chính:

``` text
Taipy / Client
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
```

Một số nguyên tắc kiến trúc quan trọng:

-   Giao diện không chứa logic tài chính cốt lõi.
-   FastAPI là ranh giới tích hợp của hệ thống.
-   Classical Risk Engine có thể hoạt động độc lập với Quantum.
-   Quantum layer không tự định nghĩa các khái niệm tài chính.
-   Logic tài chính và tính toán được tách khỏi lớp trình bày.

------------------------------------------------------------------------

# Quy trình phân tích rủi ro

Sigma chuyển dữ liệu tài chính thành thông tin rủi ro theo chuỗi:

``` text
Market Data
    ↓
Validated Data
    ↓
Returns
    ↓
Volatility
    ↓
Market Regime
    ↓
Distribution
    ↓
Scenarios
    ↓
Portfolio P&L / Loss
    ↓
Loss Distribution
    ↓
Risk Estimation
```

Các đại lượng rủi ro trọng tâm gồm:

``` text
VaR
CVaR / Expected Shortfall
Expected Loss
Stress Loss
Risk Contribution
```

Quy ước về lãi/lỗ và bối cảnh tính toán rủi ro phải được xác định rõ
trong từng phân tích.

------------------------------------------------------------------------

# Classical Risk Engine

Classical Risk Engine là **baseline bắt buộc** và là nền tảng tính toán
của Sigma V1.

Nó chịu trách nhiệm cho:

-   Xử lý kịch bản;
-   Tính P&L và loss của danh mục;
-   Monte Carlo;
-   Xây dựng phân phối lãi/lỗ;
-   VaR;
-   CVaR;
-   Stress Testing;
-   Risk Contribution.

Classical Risk Engine phải có khả năng hoạt động độc lập:

``` text
Quantum không khả dụng
        ↓
Classical Risk Analysis
        ↓
Hệ thống vẫn hoạt động
```

Điều này giúp Sigma duy trì khả năng phân tích rủi ro ngay cả khi
Quantum chưa phù hợp, chưa khả dụng hoặc không tạo ra lợi ích rõ ràng.

------------------------------------------------------------------------

# Quantum Research Layer

Quantum được xem là **lớp tăng cường tính toán** cho các bài toán phù
hợp.

Hướng nghiên cứu ưu tiên của Sigma V1 là:

``` text
Quantum Monte Carlo
        +
Quantum Amplitude Estimation
```

Một quy trình Quantum điển hình có thể được biểu diễn như:

``` text
Đại lượng tài chính cần ước lượng
            ↓
Công thức hóa bài toán Quantum
            ↓
Chuẩn bị trạng thái
            ↓
Oracle
            ↓
Amplitude Estimation
            ↓
Ước lượng rủi ro
```

Quantum không nhận dữ liệu tài chính thô và tự thay thế toàn bộ quy
trình mô hình hóa tài chính.

Ví dụ, một đại lượng mục tiêu có thể được xây dựng dưới dạng:

``` text
P(Loss > Threshold)
```

hoặc một kỳ vọng được công thức hóa rõ ràng.

### Các hướng kiến trúc

**Classical thuần túy**

``` text
Data
  ↓
Classical Modeling
  ↓
Classical Scenarios
  ↓
Classical Risk
```

**Hybrid cơ bản**

``` text
Data
  ↓
Classical Modeling
  ↓
Classical Scenarios
  ↓
Quantum State Preparation
  ↓
QAE
  ↓
Risk Estimate
```

**Kiến trúc đồng thiết kế Classical -- Quantum**

``` text
Data
  ↓
Classical Parameter Estimation
  ↓
Quantum Distribution / Scenario Representation
  ↓
Quantum Estimation
  ↓
Risk Estimate
```

Không có kiến trúc nào được mặc định là tốt nhất. Việc lựa chọn phải dựa
trên bài toán, chi phí tính toán và kết quả thực nghiệm.

------------------------------------------------------------------------

# Classical -- Quantum Benchmark

Mọi so sánh phải đặt Classical và Quantum trên **cùng một bài toán tài
chính**.

Các điều kiện quan trọng gồm:

``` text
Cùng danh mục
Cùng dữ liệu
Cùng đại lượng rủi ro
Cùng thời hạn
Cùng mức tin cậy
Cùng bối cảnh mô hình phù hợp
```

Các tiêu chí đánh giá có thể bao gồm:

-   Độ chính xác;
-   Sai số tuyệt đối / tương đối;
-   Thời gian chạy;
-   Chi phí lấy mẫu / truy vấn;
-   Số qubit;
-   Độ sâu mạch;
-   Số shots;
-   Chi phí oracle;
-   Chi phí chuẩn bị trạng thái;
-   Ảnh hưởng của nhiễu;
-   Khả năng mở rộng.

Kết quả benchmark có thể cho thấy:

``` text
Quantum Advantage
```

nhưng cũng có thể cho thấy:

``` text
Quantum No Advantage
```

hoặc:

``` text
Inconclusive
```

Một kết quả Quantum không vượt Classical vẫn là một kết quả nghiên cứu
có giá trị nếu thí nghiệm được thiết kế và đánh giá đúng.

------------------------------------------------------------------------

# Quy trình nghiên cứu

Các đóng góp nghiên cứu quan trọng của Sigma nên đi theo:

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
Resource / Ablation Analysis
   ↓
Scientific Conclusion
   ↓
Product Evaluation
```

Sigma không bắt đầu bằng câu hỏi:

> "Có Quantum algorithm nào để dùng không?"

Mà bắt đầu bằng:

> "Bottleneck tài chính nào đáng giải quyết, và Quantum có thể đóng góp
> gì?"

------------------------------------------------------------------------

# Công nghệ

Sigma V1 sử dụng Python làm hệ sinh thái tính toán chính.

Các công nghệ chính:

``` text
Python 3.12
uv
FastAPI
Taipy
NumPy
pandas
SciPy
statsmodels / scikit-learn
Qiskit
Qiskit Aer
pytest
Ruff
Pyright
Git
```

Danh sách công nghệ có thể thay đổi khi yêu cầu kỹ thuật thay đổi. Việc
bổ sung một thư viện hoặc hạ tầng mới cần có lý do thực tế và phù hợp
với phạm vi của dự án.

------------------------------------------------------------------------

# Cấu trúc dự án

Sigma được phát triển theo hướng modular monolith trong V1.

Cấu trúc khái quát:

``` text
sigma/
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
├── src/
│   └── sigma/
│       ├── data/
│       ├── modeling/
│       ├── scenarios/
│       ├── risk/
│       ├── quantum/
│       ├── application/
│       └── api/
├── tests/
├── research/
└── examples/
```

Cấu trúc có thể tiếp tục được điều chỉnh trong quá trình phát triển,
nhưng các ranh giới kiến trúc cốt lõi cần được duy trì ổn định.

------------------------------------------------------------------------

# Lộ trình phát triển

## Giai đoạn 0 --- Nền tảng

-   Hoàn thiện cấu trúc dự án;
-   Thiết lập môi trường Python/uv;
-   Hoàn thiện tài liệu;
-   Xác định schema và quy ước;
-   Thiết lập nền tảng kiểm thử.

## Giai đoạn 1 --- Classical Risk Core

-   Ingestion dữ liệu thị trường;
-   Kiểm tra và xử lý dữ liệu;
-   Tính returns;
-   Mô hình hóa volatility và regime;
-   Xây dựng phân phối;
-   Sinh kịch bản;
-   Monte Carlo;
-   VaR/CVaR;
-   Stress Testing.

## Giai đoạn 2 --- API và giao diện

-   FastAPI;
-   Application layer;
-   Risk API;
-   Taipy reference client;
-   Trực quan hóa kết quả phân tích.

## Giai đoạn 3 --- Quantum Benchmark

-   Công thức hóa đại lượng tài chính;
-   Chuẩn bị trạng thái;
-   Xây dựng oracle;
-   Thực nghiệm QAE/QMC;
-   Classical baseline;
-   Benchmark công bằng;
-   Phân tích tài nguyên.

## Giai đoạn 4 --- Nghiên cứu nâng cao

-   Phân phối nâng cao;
-   Mô hình hóa uncertainty;
-   Learned distributions;
-   Advanced portfolio risk;
-   Một số bài toán optimization phù hợp;
-   Các phương pháp Quantum khác khi có cơ sở.

## Giai đoạn 5 --- Productization

-   Data connectors ổn định;
-   Persistence;
-   Authentication / Authorization;
-   Observability;
-   Auditability;
-   Deployment;
-   Model Governance.

------------------------------------------------------------------------

# Phạm vi của Sigma

## Sigma là

-   Financial Risk Intelligence Engine;
-   Nền tảng nghiên cứu Classical -- Quantum;
-   Hệ thống phân tích rủi ro theo hướng risk-first;
-   Hệ thống mô phỏng kịch bản và phân tích tail risk;
-   Môi trường nghiên cứu có thể benchmark;
-   Nền tảng API cho decision support.

## Sigma không phải

-   Hệ thống giao dịch tự động;
-   Sản phẩm dự báo giá cổ phiếu;
-   Nền tảng ngân hàng production;
-   Hệ thống thay thế các risk system tổ chức;
-   Công cụ được xây dựng chỉ để chứng minh quantum advantage;
-   Cố vấn đầu tư tự động.

------------------------------------------------------------------------

# Sử dụng có trách nhiệm

Sigma là một dự án nghiên cứu và kỹ thuật. Các kết quả rủi ro phải luôn
được xem xét trong bối cảnh của:

``` text
Dữ liệu
Mô hình
Giả định
Kịch bản
Mức tin cậy
Phương pháp
Giới hạn
```

Kết quả của Sigma không phải là tư vấn tài chính và không bảo đảm hiệu
quả đầu tư.

Việc sử dụng Sigma trong môi trường tài chính thực tế sẽ cần thêm các
yêu cầu phù hợp, bao gồm:

-   Independent Validation;
-   Data Governance;
-   Security;
-   Model Governance;
-   Domain Expertise;
-   Regulatory / Compliance Review.

------------------------------------------------------------------------

## Định hướng

> **Sigma không xây Quantum để chứng minh Quantum.**
>
> Sigma xây dựng **Financial Risk Intelligence** và sử dụng Quantum ở
> những nơi Quantum thực sự tạo ra giá trị có thể đo lường.
