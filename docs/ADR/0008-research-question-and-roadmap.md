# ADR-0008: Research Question & Roadmap — Regime-Aware Quantum Risk Estimation

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Khóa câu hỏi nghiên cứu trung tâm, kiến trúc nghiên cứu và
roadmap 3 tầng của Sigma
**Liên quan:** ADR-0007, RULES-001/003/043, PRD.md §3/§13, WORKFLOW.md §10–12,
README.md §5.8–5.9

---

## 1. Câu hỏi nghiên cứu trung tâm

Sigma không nghiên cứu "quantum có nhanh hơn classical không", cũng không
nghiên cứu "MS-GARCH có tốt hơn GARCH không".

Câu hỏi trung tâm của Sigma:

> **When, if ever, does quantum risk estimation provide practical value for
> financial tail-risk estimation under different market regimes?**

```text
Market Regime
      ↓
Risk Distribution
      ↓
Portfolio Loss Distribution
      ↓
Tail Risk
      ↓
Classical MC  vs  Quantum Risk Estimation
      ↓
VaR / CVaR
      ↓
Practical Quantum Value
```

Hypothesis có thể falsify (KHÔNG phải là claim):

> The practical value of quantum risk estimation may depend on the
> statistical characteristics of the underlying financial regime and loss
> distribution.

Kết quả khả dĩ đều hợp lệ: QAE tốt hơn một số regime, ngang bằng, tệ hơn,
hoặc MC thắng mọi regime — tất cả đều là kết quả khoa học có giá trị nếu
experimental design đủ rigorous.

## 2. Vì sao cần HMM

Thị trường không phải một distribution cố định. Ta kỳ vọng các giai đoạn:

```text
Regime 1 → Calm / low-volatility
Regime 2 → Volatile / transition
Regime 3 → Crisis / stressed
```

có statistical characteristics khác nhau, nhưng **không biết trước ngày nào
thuộc regime nào**. HMM infer latent market regimes từ financial observations:

```text
Historical Market Data → Returns → HMM → P(S_t = k | r_{1:t}) → Hidden Regimes
```

Đây là điểm khác biệt so với paper dùng Markov states *observable* (vd
NBER chronology — chính paper đã thừa nhận observable-state là simplification).
Sigma **infer regime từ data**, không giả định từ bên ngoài.

## 3. HMM không phải research endpoint

Ta không làm HMM chỉ để có ba cái label. HMM phải tạo ra các
**financially distinct risk environments**. Sau fit, phải kiểm tra
`R₁ ≠ R₂ ≠ R₃` theo các đặc điểm tài chính có ý nghĩa:

- volatility;
- return distribution;
- skewness;
- kurtosis;
- tail probability;
- dependence/correlation nếu portfolio multi-asset.

Tên Calm / Volatile / Crisis **chỉ được gán SAU khi characterise từ data**,
không hard-code từ trước.

## 4. Regime-specific GARCH — hai tầng, terminology đã khóa

```text
HMM → infer regimes → R₁/R₂/R₃ → GARCH₁/GARCH₂/GARCH₃ → σ²₁,ₜ/σ²₂,ₜ/σ²₃,ₜ
```

- Gọi là **two-stage regime-specific / regime-conditioned GARCH approach**.
- KHÔNG gọi là formal MS-GARCH. MS-GARCH là extension chặt chẽ hơn
  (regime-switching và GARCH dynamics trong một switching volatility model
  thống nhất) — **future advanced extension, không phải requirement của
  Paper 1**.

Tách bạch vai trò:

```text
HMM     → WHICH regime?
GARCH_k → HOW volatility behaves within regime k?
```

Mô tả (vd: R₁ persistent low vol, R₂ elevated/changing, R₃ high persistent
vol) là **hypothesis cần kiểm tra**, không được assume trước.

## 5. Regime-conditioned distribution

```text
R₁ + GARCH₁ → Distribution₁
R₂ + GARCH₂ → Distribution₂
R₃ + GARCH₃ → Distribution₃
```

Student-t là candidate do tail behavior, nhưng **không được mặc định luôn
đúng** — phải kiểm tra theo financial evidence. Core chain:

```text
Regime → Return Distribution → Portfolio Loss Distribution
```

## 6. Portfolio Loss Distribution là trung tâm

Không dừng ở asset return. Ta đi tới:

```text
L = −wᵀr   (hoặc formulation tương ứng horizon/scenario của Sigma)

Regime-specific return distribution
    → portfolio scenarios
    → portfolio returns
    → portfolio loss
    → loss distribution
```

Đây là object mà Classical MC và Quantum Risk Estimation cuối cùng phải
estimate.

## 7. Classical Monte Carlo là baseline bắt buộc

```text
Loss Distribution → Classical MC → VaR / CVaR
```

Cần đo: estimation error, confidence interval, số samples, runtime,
convergence, accuracy. Không có Classical MC thì quantum comparison vô nghĩa.

## 8. Quantum side: QMC + QAE

Giữ terminology:

- **QAE** = algorithm.
- **QMC** = broader quantum Monte Carlo / quantum risk-estimation approach.

Không nói "mỗi regime chạy một QAE" — mà nói:

> Mỗi regime tạo thành một **regime-conditioned quantum risk estimation
> experiment**.

```text
Loss Distribution → State Preparation → Oracle / payoff / loss encoding
    → Amplitude → QAE / IQAE → VaR / CVaR-related quantity
```

## 9. Research matrix (experimental design backbone)

| Dimension | Regime 1 | Regime 2 | Regime 3 |
|---|---|---|---|
| Volatility | ? | ? | ? |
| Skewness | ? | ? | ? |
| Kurtosis | ? | ? | ? |
| Tail probability | ? | ? | ? |
| Distribution | ? | ? | ? |
| Loss distribution | ? | ? | ? |
| Classical MC | ✓ | ✓ | ✓ |
| QAE/QMC | ✓ | ✓ | ✓ |
| VaR | ✓ | ✓ | ✓ |
| CVaR/ES | ✓ | ✓ | ✓ |
| Quantum error | ✓ | ✓ | ✓ |
| Resource cost | ✓ | ✓ | ✓ |
| Noise sensitivity | ✓ | ✓ | ✓ |

Câu hỏi cuối cùng của research matrix:

> Does quantum risk estimation behave differently across regimes?

## 10. Precedent và warning (paper Ghysels et al., 2311.00825v1)

- **Precedent:** regime-switching financial models có thể đưa vào quantum
  risk/pricing algorithms (credit risk, derivative pricing). Good regime →
  lower risk params; Bad regime → higher risk params; → quantum estimation.
- **Warning (rất quý):** theoretical QAE speedup ≠ practical quantum
  advantage. Trong practical example, canonical QAE quá lớn cho hardware
  hiện tại → họ chuyển sang Iterative QAE; còn báo cáo circuit-depth /
  connectivity constraints chưa khai thác được scaling advantage.

Đây chính xác là thứ Sigma phải **đo**.

## 11. Evaluation: hai nhóm dimension

### Financial / statistical
VaR, CVaR/ES, tail probability, estimation error, backtesting,
distributional fit, **regime stability**.

### Quantum / computational
Qubits, circuit depth, two-qubit gates, shots, state-preparation cost,
oracle cost, noise sensitivity, runtime, estimation error, end-to-end cost.

Đặc biệt, toàn bộ **pipeline** (input preparation + state preparation +
oracle + quantum estimation + measurement + classical post-processing) được
xem như một pipeline — không lấy asymptotic QAE complexity rồi tuyên bố
quantum advantage.

## 12. Roadmap 3 tầng

### Phase 1 — Core Research (Paper 1 core)

```text
Market Data → Returns → HMM → 3-ish regimes → Regime characterization
    → Regime-conditioned distribution → Portfolio loss
    → Classical MC vs QAE/QMC → VaR/CVaR
```

### Phase 2 — Volatility enhancement

```text
HMM → R₁/R₂/R₃ → GARCH₁/₂/₃ → Regime-specific distributions → MC vs QAE
```

Đưa GARCH per regime vào một cách có kiểm soát.

### Phase 3 — Advanced research

```text
Formal MS-GARCH → regime-dependent volatility → richer distribution
    → quantum risk estimation
```

Và xa hơn: **quantum regime-transition encoding** (lấy cảm hứng từ quantum
Markov-chain construction trong paper Ghysels et al.).

## 13. Architecture research cuối cùng

```text
                    SIGMA
          REGIME-AWARE QUANTUM RISK INTELLIGENCE

                Market Data → Returns → HMM
                → Hidden Market Regimes (R₁/R₂/R₃)
                → GARCH₁/₂/₃ → Regime-specific distributions
                → Portfolio Loss Distribution
                → Classical MC | QMC + QAE
                → VaR / CVaR
                → Accuracy / Risk / Resources
                → Regime-dependent Quantum Value
```

Không phải trading bot, không phải stock-price prediction, không phải
"Quantum vì Quantum". Mà là:

> Financial regime modeling → regime-conditioned risk → classical baseline →
> quantum risk estimation → rigorous comparison.

Khớp North Star: **Classical First → Quantum Where Justified → Fair
Benchmark → Measure Real Value → Decision Intelligence.**

## 14. Điều KHÔNG được phép tuyên bố

- Không tuyên bố "quantum thắng" nếu chưa có bằng chứng đo được.
- Không gọi HMM + GARCH₁/₂/₃ + QAE là "final locked mathematical model"
  ngay hôm nay — chỉ là architecture direction.
- Không gọi research distinction (infer regime từ data thay vì quan sát)
  là novelty cho đến khi hoàn thành systematic literature review.

## 15. Trước khi code Paper 1 — 4 điều cần formalize

1. **HMM emission model** — Gaussian vs Student-t, cấu hình cụ thể.
2. **Cách xác định số regime k** — BIC + economic interpretability +
   stability, không chỉ AIC/BIC.
3. **Cách GARCH được fit sau regime inference** — two-stage protocol,
   window, refit.
4. **Chính xác quantity nào QAE estimate** để lấy VaR/CVaR.

Khi 4 điều này được khóa, Sigma sẽ có một **experimental framework defend
được trước reviewer**, không chỉ là "ý tưởng hay".