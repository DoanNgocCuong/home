## 1. Vấn đề

Query `WHERE agent_id = 'agent_hobby_general'` trả về rỗng mặc dù data tồn tại trong database.

---

## 2. Nguyên nhân

Có **trailing space** (dấu cách ở cuối) trong giá trị `agent_id`:

|id|agent_id|LENGTH|
|---|---|---|
|7|`'agent_hobby_general '`|20|
|32|`'agent_hobby_general '`|20|
|39|`'agent_hobby_general'`|19 ✓|

Hex `...6c20` → byte `20` = space character

PostgreSQL so sánh chính xác từng byte, nên `'agent_hobby_general'` ≠ `'agent_hobby_general '`

---

## 3. Giải pháp

**Immediate fix:**

```sql
UPDATE agenda_agent_prompting
SET agent_id = TRIM(agent_id)
WHERE agent_id != TRIM(agent_id);
```

**Phòng ngừa:**

```sql
-- Thêm CHECK constraint
ALTER TABLE agenda_agent_prompting
ADD CONSTRAINT agent_id_no_whitespace 
CHECK (agent_id = TRIM(agent_id));
```

Hoặc TRIM khi INSERT trong code Python/Spring.