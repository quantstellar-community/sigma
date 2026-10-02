# ADR-0012: Scenario Distribution Family in Hybrid = GARCH Innovation (Student-t)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** Làm rõ quyết định family phân phối cho scenario generation
trong pipeline Hybrid
**Liên quan:** ADR-0006 (GARCH-t), ADR-0007 (Hybrid), ADR-0009 (HMM
emission), ADR-0011 (regime-partitioned GARCH), WORKFLOW.md §5.3

---

## 1. Bối cảnh

Có ba "phân phối" khác nhau trong pipeline, dễ bị trộn lẫn:

```text
① HMM emission family     → Gaussian (đã chốt ADR-0009)   — TÌM regime
② GARCH innovation family → Student-t (đã chốt ADR-0006)  — ĐO vol
③ Scenario distribution   → ?                             — SINH kịch bản
```

Trước đây có quan điểm cho rằng WP-5 sẽ phải "quyết định lại Gaussian vs
Student-t" cho ③. Quan điểm này SAI đối với đường Hybrid — cần ghi rõ.

## 2. Quyết định

### D1 — Trong Hybrid, ③ = ②: scenario dùng GARCH innovation (Student-t)

Pipeline Hybrid sinh scenario bằng `simulate_regime_paths` (ADR-0011 D4):

```text
Mỗi ngày: rút ε ~ Student-t(ν[regimeₜ])     ← family của GARCH
          σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁       ← recursion của GARCH
```

→ Không có lựa chọn family riêng cho scenario: family của scenario
CHÍNH LÀ family innovation của GARCH — **Student-t, đã chốt từ ADR-0006**,
với ν học riêng cho từng regime (quan sát nu Calm 7.5 / Crisis 20.4).

### D2 — Đường "chọn lại family" (Gaussian/Student-t/empirical cho returns regime) chỉ là FALLBACK

Chỉ tồn tại nếu benchmark OOS (WP-4b.5b) kết luận GARCH per regime KHÔNG
đáng dùng (thua baseline) → khi đó mới fit distribution trực tiếp trên
returns của từng regime như Phase 1 đơn giản. Đây là phương án dự phòng,
không phải đường chính.

### D3 — Việc còn lại của WP-5

Không phải "chọn family" mà là:

- nối `simulate_regime_paths` vào scenario engine (portfolio gộp wᵀr);
- chọn regime khởi đầu + transition matrix cho mô phỏng (từ HMM);
- benchmark end-to-end: hybrid scenarios → VaR coverage OOS vs baseline.

## 3. Hệ quả

- Dọn sạch mơ hồ: family phân phối đã được chốt bằng chuỗi quyết định
  ADR-0006 → 0011 → 0012, không cần "quyết định lại".
- WP-5 tập trung vào tích hợp + benchmark, không phải lựa chọn family.
- Bằng chứng thực nghiệm (nu theo regime, kurtosis 7.5) được ghi nhận là
  thông tin mô tả, không làm đảo quyết định family.