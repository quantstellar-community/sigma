# ADR-0006: Conditional Volatility Layer (WP-4a)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/modeling/volatility.py` + benchmark trong
`tests/evaluation/`
**Liên quan:** ADR-0001 D7 (horizon), ADR-0002 (float boundary),
ADR-0005 (returns input), SCHEMA.md §8.1–8.2, WORKFLOW.md §5.1,
RULES-001/003/043

---

## 1. Bối cảnh

Returns đã sẵn sàng (WP-3). WP-4a xây tầng volatility — đầu vào bắt buộc
của Regime (WP-4b) và Monte Carlo. Nguyên tắc điều hành: *không tuyên bố
GARCH có giá trị nếu chưa thắng baseline bằng phép đo out-of-sample*.

## 2. Quyết định

### D1 — Thư viện: `arch` (đã có trong runtime deps)

Chuyên môn hẹp đúng bài toán, API ổn định, hỗ trợ Normal/t/skewt/GED.
Zero new dependency (TECH_STACK §22).

### D2 — Benchmark ladder: các ứng viên cùng interface

```text
constant_sigma(returns)                    # baseline 0
rolling_sigma(returns, window=60)          # baseline 1
ewma_sigma(returns, lam=0.94)              # baseline 2 (RiskMetrics)
```

(Các baseline naive này được giữ làm thước đo so sánh trong evaluation
suite. GARCH-per-regime — ứng viên chính — sống trong `regime_garch.py`
theo ADR-0011.)

Mỗi hàm trả `sigma_daily: float` — dự báo 1 bước cho ngày kế tiếp. Interface
thuần float giúp benchmark ghép công bằng và unit test số tay trực tiếp.

### D3 — Distribution chọn bằng phép đo, không mặc định

GARCH-Student-t được chọn so với GARCH-Normal qua VaR coverage ngoài mẫu
(chi tiết trong §6). Không chấp nhận "Student-t vì literature nói vậy"
không có bằng chứng trên dữ liệu của Sigma.

### D4 — Rolling window 1000 ngày giao dịch (~4 năm), refit theo snapshot

Tham số GARCH ước lượng trên 1000 phiên gần nhất; cửa sổ trượt khi snapshot
mới về. Lý do: tham số phải mô tả "thế giới gần đây"; window dài hơn mang
theo cấu trúc thị trường đã chết. Không dùng expanding window.

### D5 — Mean model: Constant

Mỗi asset một mean riêng học từ data. Zero-mean (RiskMetrics 1996) bị loại
vì gán oan equity premium vào cú sốc.

### D6 — Horizon forecast: 1 ngày

Theo ADR-0001 D7. Multi-day hoãn đến khi chốt rebalancing assumption.

### D7 — Diagnostics-first (học từ research/references Vietnam Rice notebook)

`check_arch_effects()` chạy ADF + ARCH-LM **trước** khi fit: nếu dữ liệu
không có heteroskedasticity, báo cáo ngay thay vì fit mô hình cho bệnh
không tồn tại. Notebook đối chứng cũng cảnh báo hai lỗi KHÔNG sao chép:
interpolate giá thiếu (vi phạm §7.5) và gọi in-sample `conditional_volatility`
là "predicted".

### D8 — Benchmark là gate, nằm trong `tests/evaluation/`, dạng `.py`

Out-of-sample expanding window trên snapshot thật; mỗi ngày test mọi ứng
viên dự báo σ chỉ bằng dữ liệu quá khứ; xuất bảng VaR violation rate
(95/99) + MAE vol. Assert chỉ ở mức cấu trúc + biên sanity rộng; quyết định
nghiệp vụ thuộc người đọc bảng. Notebook không được làm thước đo (reproducibility);
notebook sau này chỉ vẽ chart từ kết quả đã xuất.

## 3. Chi tiết kỹ thuật

- EWMA khởi tạo variance = sample variance toàn chuỗi, đệ quy RiskMetrics λ=0.94.
- Rolling std ddof=1 trên `window` phiên gần nhất; yêu cầu đủ `window` điểm.
- Chuỗi <2 điểm → ModelingError.
- (GARCH-per-regime: chi tiết kỹ thuật trong ADR-0011 — fit pooled trên
  percent-scale, carry-over forecast, `_MIN_REGIME_OBS = 100`.)

## 4. Phạm vi

In: 3 baselines naive (constant/rolling/ewma), diagnostics, VolatilityState
entity, evaluation harness.
Out: Regime layer (WP-4b), multi-day forecast, MS-GARCH (research-only theo
ADR-0004 tinh thần). GARCH-per-regime chuyển sang `regime_garch.py`
(ADR-0011) — `garch_sigma` standalone đã bị xóa (quyết định tại ADR-0011 §6:
hybrid là ứng viên chính, không giữ GARCH lẻ kề bên).

## 5. Hệ quả

- Output chưa được coi là đáng tin cho đến khi benchmark chạy xanh.
- Nếu GARCH thua EWMA ngoài mẫu → negative result hợp lệ, baseline rẻ hơn
  được ưu tiên dùng (RULES-043).

---

## 6. Selection Outcome (bổ sung sau benchmark)

Kết quả OOS 250 ngày × 3 assets (chi tiết trong
`tests/evaluation/test_volatility_benchmark.py`):

- Constant baseline thất bại theo hai hướng đối xứng (GLD viol95 = 13.6%
  đánh giá thấp rủi ro; NVDA viol99 = 0% thận trọng quá mức) → xác nhận
  conditional volatility là cần thiết.
- EWMA và GARCH-t hòa ở coverage 1 ngày (khoảng cách nằm trong nhiễu mẫu).

**Quyết định (tại thời điểm WP-4a):** `GARCH(1,1)-Student-t` được chọn làm
volatility model — thắng Normal về tail behavior, cung cấp residuals chuẩn
hóa, tham số diễn giải được (persistence α+β, tail ν).

**Điều kiện ràng buộc:** EWMA giữ vai trò baseline thường trực trong
evaluation suite. Nếu benchmark mở rộng sau này cho thấy GARCH-t kém EWMA
ra ngoài nhiễu thống kê → xem xét lại, không giữ vì cảm tình.

> **Cập nhật 2026-08-24 (ADR-0007):** vai trò của GARCH được điều chỉnh —
> từ "primary model của pipeline" thành **supporting layer + baseline**.
> Định hướng nghiên cứu trung tâm chuyển sang HMM regime layer
> (regime-conditioned GARCH). Code/tests giữ nguyên; ngừng phát triển thêm.
>
> **Cập nhật 2026-08-24 (ADR-0011 §6):** `garch_sigma` standalone bị XÓA
> khỏi code. GARCH-per-regime (hybrid) là ứng viên chính của volatility
> layer; benchmark OOS cho kết quả hỗn hợp (GLD cải thiện, MAE thắng 2/3,
> viol95 SPY/NVDA cao hơn — trong nhiễu mẫu) → giữ baselines naive làm
> thước đo, không giữ GARCH lẻ kề bên hybrid.
