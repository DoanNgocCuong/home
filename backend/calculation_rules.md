# 📊 Cách Tính XP & Streak

## 🎯 XP (Experience Points)

- **Base XP**: 100 điểm/bài viết
- **Word Bonus**: 1 điểm/10 từ
- **Công thức**: `XP = (số bài × 100) + (tổng từ ÷ 10)`
- **Ví dụ**: 5 bài, 5000 từ → XP = 500 + 500 = 1000

## 📈 Level Progression

- **Level 1**: 1000 XP
- **Level 2**: 1500 XP (1000 × 1.5)
- **Level 3**: 2250 XP (1500 × 1.5)
- **Level n**: 1000 × (1.5^(n-1)) XP

## 🔥 Streak (Chuỗi ngày liên tiếp)

- **Current Streak**: Số ngày liên tiếp có bài viết (từ gần nhất về quá khứ)
- **Max Streak**: Chuỗi dài nhất trong lịch sử
- **Flexible**: Không bắt buộc viết hôm nay để duy trì streak

## 📅 Total Days

- Tổng số ngày từ bài viết đầu tiên đến hiện tại

## 📁 Folder Cha (Parent Folder)

### XP & Level
- **XP**: Tổng XP của tất cả files trong folder + tất cả subfolders
- **Level**: Tính từ tổng XP (cùng công thức như trên)
- **Ví dụ**: Folder A có 1000 XP + Subfolder B có 500 XP = 1500 XP total

### Streak
- **Current Streak**: Tổng hợp tất cả ngày hoạt động từ folder + subfolders
- **Max Streak**: Chuỗi dài nhất trong toàn bộ cây folder
- **Logic**: Nếu có bài viết ở bất kỳ đâu trong cây → ngày đó được tính

### Metrics
- **Task Count**: Tổng số files trong toàn bộ cây
- **Total Words**: Tổng từ của tất cả files
- **Last Activity**: Ngày hoạt động gần nhất trong toàn bộ cây

---

*Công thức được thiết kế để khuyến khích viết đều đặn và chất lượng nội dung*
