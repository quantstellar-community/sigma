# ADR-0009: HMM Regime Layer (WP-4b)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/modeling/regime.py` — HMM regime detection,
characterization, labeling, protocol chọn k
**Liên quan:** ADR-0007 (Hybrid direction), ADR-0008 (research question),
SCHEMA.md §8.2–8.4, WORKFLOW.md §5.2, RULES-043

---

## 1. Bối cảnh

WP-4b là bước đầu tiên của Hybrid (ADR-0007 D2): HMM infer latent market
regimes từ returns. Đây là **trung tâm nghiên cứu của Sigma** — regime
chính là điều kiện cho mọi thứ phía sau (regime-conditioned GARCH, quantum
risk estimation per regime).

## 2. Quyết định

### D1 — Gaussian emission trước (hmmlearn.GaussianHMM)

`hmmlearn` chỉ hỗ trợ Gaussian emission native. Bắt đầu với Gaussian, sau đó
**đo** (characterization) xem từng regime có fat tails thật không — chỉ
thêm Student-t emission nếu có bằng chứng (ADR-0008 §5: không mặc định
Student-t). Lưu ý: tách regime tự nó đã bắt phần lớn fat tails (Crisis state
có variance cao), giảm nhu cầu Student-t.

### D2 — Input: log returns

Theo ADR-0005: log returns là derived representation cho HMM/regime.
`to_log(ReturnMatrix)` đã có sẵn.

### D3 — Output: `RegimeFit` + `RegimeCharacterization` + labels

- `RegimeFit`: state probabilities (filtered), Viterbi path, emissions
  (mu/sigma mỗi state), transition matrix, dataset_id — full provenance.
- `RegimeCharacterization`: annualized vol, mean, skewness, duration
  (từ transition matrix) mỗi state — đo SAU fit.
- `label_regimes`: map state → nhãn DỰA TRÊN đặc tính đo được:
  vol thấp nhất + mean ≈ 0 → "Calm"; trung bình → "Volatile"; cao nhất
  + đuôi nặng → "Crisis". Quy tắc rõ ràng, có test — không hard-code trước.

### D4 — Protocol chọn k: `select_k(candidates=(2, 3))`

Không áp đặt k=3. Chọn theo:

```text
BIC (statistical fit)
+ regime stability (labels giữ nguyên nghĩa khi fit lại trên cửa sổ khác)
+ economic interpretability (các state có nghĩa tài chính)
```

Stability test: fit trên 2 nửa chuỗi, so sánh labels — đây là tiêu chí
reviewer sẽ hỏi, phải đo trước.

### D5 — Determinism

`hmmlearn` fit có khởi tạo ngẫu nhiên → dùng seed cố định để reproducible
(RULES-001). Mọi fit trong cùng input phải ra cùng kết quả.

### D6 — Lỗi: `ModelingError`

Chuỗi quá ngắn / k không hợp lệ → ModelingError, không trả về kết quả mập mờ.

## 3. Phạm vi

In: fit, characterization, labeling, select_k protocol, tests synthetic +
integration trên snapshot thật.
Out: GARCH per regime (WP-4b.5 — cần regime ổn định trước), regime-
conditioned distribution (WP-5), Student-t emission (chỉ khi có bằng chứng).

## 4. Hệ quả

- Regime là model output được HMM suy ra từ data — có thể đo được tính ổn
  định, giải thích được.
- Nếu k=3 không ổn định trên data thật → k=2 là kết quả hợp lệ (RULES-043).
- Đây là nền tảng cho regime-conditioned GARCH và quantum per regime.

---

## 5. Measurement Outcome (bổ sung sau khi chạy trên snapshot thật)

Đo trên SPY, 11.6 năm (2026-08-24):

### k=2 characterization

```text
Crisis : vol 31.4%/năm, mean −0.0012%/ngày, kurtosis 7.5, duration ~19 ngày
Calm   : vol 10.8%/năm, mean +0.0010%/ngày, kurtosis 3.8, duration ~70 ngày
```

Ngày Crisis theo năm khớp các sự kiện thật: 2018 Q4 selloff, 2020 COVID,
2022 bear market — HMM tự học đúng các giai đoạn khủng hoảng, không ai dạy.

### select_k (SPY)

```text
k=2: BIC -19188.2, stability 100%
k=3: BIC -19362.8, stability 100%   ← BIC tốt hơn rõ rệt → chọn k=3
```

### Bằng chứng quan trọng cho WP-5

Crisis state có **kurtosis 7.5** — fat tails CÒN LẠI ngay cả sau khi đã tách
regime (Calm gần Gaussian: 3.8). Hàm ý:

- Gaussian emission **đủ** cho mục đích nhận diện regime (segmentation dựa
  chủ yếu trên vol/mean, không nhạy với hình dạng đuôi);
- NHƯNG distribution layer (WP-5) phải xét **Student-t cho Crisis regime**
  khi sinh scenario — quyết định sẽ được chốt ở WP-5 kèm benchmark,
  không phải mặc định trước (ADR-0008 §5).