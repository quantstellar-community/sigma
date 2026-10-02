# ADR-0007: Hybrid HMM Regime Detection + Regime-Conditioned GARCH (WP-4b)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Định hướng nghiên cứu trung tâm của Sigma — regime layer
**Liên quan:** ADR-0005/0006, SCHEMA.md §8.2–8.3, WORKFLOW.md §5.2/§10–11,
PRD.md §13, README.md §5.8

---

## 1. Bối cảnh

Sau khi thống nhất về HMM (latent regimes), GARCH (volatility layer) và vai
trò Quantum (enhancement layer), đội chốt một định hướng nghiên cứu rõ ràng
cho Sigma. Điểm khác biệt quan trọng so với các paper regime-switching + 
quantum risk hiện có: phần lớn paper **quan sát/giả định** regime từ bên
ngoài (vd NBER business-cycle chronology), còn Sigma **infer regime từ dữ
liệu thị trường bằng HMM**.

## 2. Quyết định

### D1 — HMM là cốt lõi của định hướng nghiên cứu

```text
Historical Market Data → Returns → HMM → Hidden Regimes
                                            ↓
                         R₁ Calm · R₂ Volatile · R₃ Crisis   (gán nhãn SAU khi
                         ↓        ↓            ↓               thống kê characteristics)
                    GARCH₁   GARCH₂       GARCH₃
                         ↓        ↓            ↓
                    Dist₁    Dist₂        Dist₃
                         ↓        ↓            ↓
                  MC vs QAE  MC vs QAE    MC vs QAE
                         ↓        ↓            ↓
                   VaR/CVaR  VaR/CVaR    VaR/CVaR
```

### D2 — Hybrid (two-stage): HMM infer regimes → GARCH theo từng regime

- Stage 1: HMM infer latent regimes từ returns (gán nhãn từng ngày).
- Stage 2: fit GARCH riêng trong từng regime subsample (regime-conditioned).

Gọi rõ ràng là **Hybrid: HMM regime detection + regime-conditioned GARCH
(two-stage)**.

Phân biệt thuật ngữ (để tránh lẫn):
- **MS-GARCH (thuần)**: HMM trực tiếp quản lý GARCH variance, fit hợp nhất —
  toán nặng, path-dependent, khó hội tụ. **Hoãn**, chỉ nghiên cứu khi có
  bằng chứng cần thiết.
- **Regime-Conditioned GARCH (thuần)**: chia regime bằng biến điều kiện
  tường minh (observable, vd quy tắc vol > 5%) — KHÔNG dùng HMM. Không phải
  hướng của Sigma.
- **Hybrid (chọn)**: HMM giúp nhãn regime thông minh, GARCH chạy sau trên
  từng nhãn — nhanh, dễ hội tụ, tránh path-dependence của MS-GARCH.

### D3 — GARCH(1,1)-t hiện tại = supporting layer + baseline

- Vai trò báo cáo: vol 1 ngày hiển thị trên Risk Summary (DESIGN.md).
- Vai trò baseline: là thước đo cho Hybrid regime-conditioned GARCH
  benchmark sau này.
- Ngừng phát triển thêm; giữ code + tests nguyên vẹn.

### D4 — Research distinction (chưa tuyên bố là novelty)

> "Infer regime từ market data bằng HMM, rồi đánh giá quantum risk
> estimation trong từng inferred regime" — khác với "quan sát regime từ
> external chronology".

Phải thực hiện **systematic literature review** trước khi gọi đây là novelty.

### D5 — Ưu tiên thời gian: research & core trước, application hoãn

Không phát triển Taipy UI / FastAPI tích hợp trong giai đoạn này. Kiến trúc
đã cô lập UI/API khỏi core — de-emphasize là quyết định phân bổ nỗ lực,
không cần sửa docs hay xóa code.

## 3. Các bước tiếp theo (WP-4b)

1. HMM regime layer: transition model + emission model, k regimes.
2. Gán nhãn regime từ statistical characteristics (sau fit).
3. Kiểm chứng stability (fit trên nhiều cửa sổ, labels ổn định).
4. Hybrid: regime-conditioned GARCH (fit GARCH riêng từng regime) +
   benchmark vs baseline GARCH.

## 4. Hệ quả

- HMM là trung tâm; GARCH là lớp phụ trợ có vai trò rõ ràng.
- Mọi claims khoa học phải qua fair benchmark OOS (RULES-001/003).
- Negative result (Hybrid regime-conditioned GARCH không hơn baseline) là
  kết quả hợp lệ, vẫn giữ giá trị.