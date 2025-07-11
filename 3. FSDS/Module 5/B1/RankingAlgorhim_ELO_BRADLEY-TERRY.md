Thuật toán đánh giá: ELO và BRADLEY-TERRY (BT)

Giả sử chúng ta có ba mô hình LLM A, B, C vừa được đưa vào Chatbot Arena. Trong một buổi thử nghiệm ngắn, cộng đồng đã tạo ra 12 trận “đối kháng mù” (ẩn tên). Kết quả được ghi lại như sau:

Cặp đấu

A thắng

B thắng

Hòa

A vs B

4

2

0

A vs C

1

3

0

B vs C

2

0

0

Như vậy tổng cộng ta có:
• 4 + 2 + 1 + 3 + 2 = 12 trận có phân thắng–thua, không có hòa.
Dưới đây là cách hai hệ thống Elo và Bradley-Terry (BT) xử lý đúng bộ dữ liệu này.

Elo: cập nhật động sau từng trận

Khởi tạo mỗi mô hình với cùng điểm $$R_0 = 1000$$.

Chọn hệ số cập nhật $$K = 32$$ (giá trị “vừa” trong thực hành).

Duyệt trận một cách tuần tự (thứ tự phát sinh trong thực tế). Sau mỗi trận tính:

$$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$
$$R_A \leftarrow R_A + K (S_A - E_A)$$

trong đó $$S_A = 1$$ nếu A thắng, $$0$$ nếu thua.

Giả sử 6 trận A vs B diễn ra liền nhau, ta sẽ thấy: • Sau trận 1 (A thắng): A tăng lên 1016, B giảm xuống 984.
• Sau trận 2 (B thắng): A rớt 17 điểm, B cộng 17 điểm…
… Và cứ thế các điểm “nhảy” liên tục.

Khi xử lý xong 12 trận, ta có một bộ điểm cuối (số tương đối, ví dụ):

Mô hình

Điểm Elo cuối

A

1008

B

1020

C

972

Lưu ý:
• Nếu ta đảo thứ tự 12 trận (chạy B vs C trước chẳng hạn) thì kết quả cuối có thể khác vài chục điểm.
• Mô hình mới thêm vào giữa chừng cũng sẽ lập tức được cộng/trừ điểm nhờ công thức online.

Bradley-Terry: ước lượng toàn cục bằng Maximum Likelihood

BT giả định sức mạnh mỗi mô hình là hằng số $$R_i$$ trong suốt chuỗi trận. Xác suất một mô hình thắng được mô hình hoá là:

P(i > j) = \frac{R_i}{R_i + R_j}

Với bộ đếm thắng–thua ở trên, ta cần tìm $$R_A, R_B, R_C$$ tối đa hoá hàm hợp lý

L(R_A,R_B,R_C) = \prod_{i>j} P(i>j)^{w_{ij}} \, (1-P(i>j))^{l_{ij}}

trong đó $$w_{ij}$$, $$l_{ij}$$ là số trận i thắng, thua trước j.

• Không có công thức đóng, song ta giải nhanh bằng lặp minorization:

import numpy as np
wins = {('A','B'):4, ('B','A'):2,
        ('A','C'):1, ('C','A'):3,
        ('B','C'):2, ('C','B'):0}
names = ['A','B','C']
R = dict(zip(names, [1.0, 1.0, 1.0]))  # khởi tạo

for _ in range(50):                    # vài chục vòng là hội tụ
    for i in names:
        numer = sum(wins.get((i,j),0) for j in names if j!=i)
        denom = sum(
            (wins.get((i,j),0)+wins.get((j,i),0)) /
            (R[i] + R[j]) for j in names if j!=i)
        R[i] = numer / denom
# Chuẩn hoá để xem như “điểm”
scale = 400/np.log(10)
elo_bt = {i: np.log(R[i])*scale + 1500 for i in names}
print(elo_bt)

Kết quả (xấp xỉ):

Mô hình

Hệ số $$R_i$$

Quy đổi sang “điểm”

A

0.94

1490

B

1.15

1515

C

0.72

1455

Đặc điểm đáng chú ý:
• BT sử dụng đồng thời tất cả 12 trận, bất kể thứ tự. Bạn shuffle dữ liệu, chạy lại → kết quả không đổi.
• Nếu ngày mai bổ sung thêm 20 trận mới, ta tính lại từ đầu trên 32 trận, nên điểm dao động ít – ổn định hơn Elo.
• Từ $$R_i$$ có thể diễn giải xác suất trực tiếp: $$P(B > A) = 1.15/(1.15+0.94) ≈ 55%$$.

Khi nào nên dùng cách nào?

• Elo lý tưởng cho môi trường “trực tuyến” (cờ vua, game) – bạn không thể biết toàn bộ lịch sử; người chơi cũng mạnh dần theo thời gian.
• Bradley-Terry hợp hơn khi:
– Lịch sử đầy đủ, dễ truy cập (Arena lưu trữ mọi vote).
– Sức mạnh mô hình tương đối cố định (một snapshot model không tự học).
– Bạn muốn xếp hạng ổn định và có thể kèm khoảng tin cậy thống kê.

Chatbot Arena vì vậy đã chuyển sang Bradley-Terry: vẫn dựa trên cặp đôi thắng–thua giống Elo, nhưng tận dụng hết dữ liệu để cho điểm “mượt” và dễ lặp lại.