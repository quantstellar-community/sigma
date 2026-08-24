# ADR-0005: Asset Returns Computation (WP-3)

**Trạng thái:** Accepted
**Ngày:** 2026-08-24
**Phạm vi:** `src/sigma/modeling/returns.py` — phép tính tài chính đầu tiên
của Sigma
**Liên quan:** ADR-0001 (return convention), ADR-0002 (Decimal/float
boundary), SCHEMA.md §7.3, §18, ARCHITECTURE.md §6.3, WORKFLOW.md §4.2

---

## 1. Bối cảnh

Snapshot giá đã sẵn sàng (WP-2, 35,112 observations). WP-3 biến giá thành
chuỗi return — đầu vào của toàn bộ modeling phía sau. Đây là lần đầu tiên
ranh giới Decimal→float (ADR-0002) đi vào hoạt động.

## 2. Quyết định

### D1 — Compute-on-demand, không persist returns

Returns là **derived data** (SCHEMA §7.3): sinh từ source bất biến thì luôn
giống nhau; lưu thêm chỉ tạo bản sao phải đồng bộ version với snapshot.
Chỉ **source** mới xứng đáng là artifact có checksum.

### D2 — Vị trí: `modeling/returns.py`

Theo đúng bản đồ ARCHITECTURE §6.3: `Market Data → Returns → Volatility →
...`. Data layer giữ prices; Modeling layer bắt đầu tại returns.

### D3 — Alignment: inner join trên ngày chung của TẤT CẢ assets

Ma trận giá được align trước (mỗi ngày = giao các ngày có mặt ở mọi asset),
returns tính dọc lưới đó. Kết quả: ma trận return không bao giờ chứa NaN,
`wᵀR` và covariance dùng được ngay. Việc drop bị **báo cáo bắt buộc** qua
`AlignmentReport` — pattern "được phép drop, không được phép im lặng".

### D4 — Ranh giới Decimal→float tập trung tại đây

```python
price_to_float(Decimal) -> float   # helper DUY NHẤT, có test riêng
```

Input domain (Decimal) → output modeling (float matrix). Không nơi nào khác
trong modeling tự convert.

### D5 — Công thức canonical

```text
R_t = adjusted_close_t / adjusted_close_{t-1} − 1     (SIMPLE, canonical)
r_t = ln(1 + R_t)                                     (LOG, derived explicit)
to_log() / inverse expm1() round-trip chính xác
```

### D6 — Output: frozen `ReturnMatrix`

```python
@dataclass(frozen=True)
class ReturnMatrix:
    values: pd.DataFrame  # index UTC dates × columns asset_ids, float
    method: str  # "SIMPLE" | "LOG"
    dataset_id: str  # provenance về snapshot nguồn
    meta: AlignmentReport
```

pandas sống trong modeling layer (TECH_STACK chỉ cấm pandas vào domain).
Metadata đi kèm để mọi kết quả phía sau mang provenance từ tầng thấp nhất.

### D7 — Lỗi: `ModelingError(ValueError)`

Danh mục lỗi WORKFLOW §21 ("Modeling Failure"). Hai trường hợp raise:
observations trộn nhiều `dataset_id`; một asset còn <2 dòng sau alignment.

## 3. Chính sách edge cases

| Trường hợp | Xử lý |
|---|---|
| Ngày đầu mỗi chuỗi | Drop, báo cáo trong AlignmentReport |
| Gap bất thường giữa ngày | **Đã chặn từ đầu vào**: validation gate kiểm tra NYSE calendar completeness bằng QuantLib — ngày giao dịch bị thiếu → `DataValidationError`, pipeline dừng (cập nhật sau phiên đánh giá ban đầu) |
| Asset <2 dòng sau align | Raise ModelingError |

## 4. Phạm vi

In: simple/log returns, alignment + report, boundary helper, tests
hand-computed. Out: volatility/regime (WP-4), portfolio aggregation `wᵀR`
(cần Portfolio domain), persistence (đã loại theo D1).

## 5. Hệ quả

- Mọi model phía sau nhận đầu vào float sạch, aligned, có provenance.
- RULES-006 trở thành code kiểm chứng được, không còn là chữ trong doc.
