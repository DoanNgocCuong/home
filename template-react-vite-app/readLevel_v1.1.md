# Hệ Thống Tính Điểm Kinh Nghiệm (XP)

## 1. Cách Tính XP

- 1 điểm kinh nghiệm (XP) = 1000 điểm giá trị
- Ví dụ:
  - Task có giá trị 1000 điểm = 1 XP
  - Task có giá trị 5000 điểm = 5 XP
  - Task có giá trị 100 điểm = 0 XP (làm tròn xuống)

## 2. Công Thức Tính Level

- Level 1: Cần 100 XP
- Level 2: Cần 150 XP (100 * 1.5)
- Level 3: Cần 225 XP (150 * 1.5)
- Level 4: Cần 338 XP (225 * 1.5)
- Level 5: Cần 507 XP (338 * 1.5)
- Và cứ tiếp tục như vậy...

## 3. Ví Dụ Cụ Thể

### Task 1:
- Giá trị: 5000 điểm
- XP nhận được: 5 XP (5000/1000)
- Nếu tag đang có 0 XP:
  - XP mới: 5 XP
  - Level: 0 (chưa đủ 100 XP)

### Task 2:
- Giá trị: 20000 điểm
- XP nhận được: 20 XP (20000/1000)
- Nếu tag đang có 5 XP:
  - XP mới: 25 XP
  - Level: 0 (chưa đủ 100 XP)

### Task 3:
- Giá trị: 100000 điểm
- XP nhận được: 100 XP (100000/1000)
- Nếu tag đang có 25 XP:
  - XP mới: 125 XP
  - Level: 1 (đã đạt 100 XP)
  - XP còn dư: 25 XP (tính cho level tiếp theo)

## 4. Lưu Ý

- XP được làm tròn xuống khi chia cho 1000
- Level chỉ tăng khi đạt đủ XP yêu cầu
- XP dư sẽ được tính cho level tiếp theo
- Mỗi tag có XP và level riêng biệt 