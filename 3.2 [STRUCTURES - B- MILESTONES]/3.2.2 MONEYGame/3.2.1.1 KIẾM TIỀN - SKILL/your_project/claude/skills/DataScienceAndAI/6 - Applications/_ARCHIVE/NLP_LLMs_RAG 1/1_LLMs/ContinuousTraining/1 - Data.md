# GIAI ĐOẠN CHƯA CÓ REAL DATA MÀ MUỐN FINETUNING: 1 cách phổ biến là dùng AI để gen data samples 

```
Oke, giúp mình chuẩn bị 1 file excel : input là: Các đoạn gồm 2 câu của robot - output là 1 trong 5 nhãn ở trên. (mỗi nhãn 40 dòng data). Đây là bộ data gen để finetuning. 

Phong cách giống Pika nhất có thể.

Oke, cho mình 5 loại, mỗi loại 1 samples để mình confirm rồi bạn tạo hàng loạt sau nhé
```


---

Mình đã tạo xong 5 mẫu theo phong cách Pika. Bạn xem qua và xác nhận xem đã đúng ý chưa nhé, sau đó mình sẽ tiến hành tạo hàng loạt.

### 5 Mẫu Dữ liệu Finetuning (Phong cách Pika)

Dưới đây là 5 mẫu, mỗi mẫu gồm một cặp câu của Pika và nhãn cảm xúc tương ứng cho câu thứ hai.

| Input (Câu 1. Câu 2)                                                                             | Output (Nhãn) |
| ------------------------------------------------------------------------------------------------ | ------------- |
| Tớ có một ý tưởng này hay lắm! Hay là mình cùng nhau vẽ một bức tranh về vũ trụ nhé?             | `thinking`    |
| Cậu vẽ đẹp quá! Bức tranh của cậu thật nhiều màu sắc và sống động.                               | `achievement` |
| Woa, nhìn kìa! Một ngôi sao băng vừa vụt qua.                                                    | `surprised`   |
| Tớ biết đôi khi thử thách có thể hơi khó một chút. Không sao đâu, tớ sẽ luôn ở đây bên cạnh cậu. | `calm`        |
| Yeah! Chúng mình đã hoàn thành thử thách rồi! Tớ vui quá đi mất!                                 | `happy`       |