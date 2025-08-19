

Ctrl Shift xuống, Ctrl D


=TRIM(CLEAN(A1))



```
=IF(ISNUMBER(SEARCH("true", M5)), 1, 0)
=IF(ISNUMBER(SEARCH("""F1"": 1", J2)), 1, 0)
=OR(ISNUMBER(SEARCH(A166, F166)), ISNUMBER(SEARCH(A166, G166)), ISNUMBER(SEARCH(A166, H166)))
=IF(ISTEXT(Q2), 1, 0)
=PERCENTILE(P1:P1001, 0.95)
```



```
"{ ""ground_truth"": [] }" => 0 "{ ""ground_truth"": [""AI Research & Model Development""] }" => 1 "{ ""ground_truth"": [""AI Research & Model Development"", ""Machine leanring""] }" => 2 Đếm số phần tử trong list, bằng excel
=IFERROR((LEN(F2) - LEN(SUBSTITUTE(F2, """", "")))/2 - 1, 0)
```

```
=REGEXEXTRACT(D1, "\{[^\}]*ground_truth[^\}]*\]")
```

```
=IF(ISBLANK(A1), 0, 1)
```


| GroundTruth loại       | Tổng mẫu | Phân tích chi tiết                                                                                                                                             | Kết quả chính                                                                     | Lý do                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{}` (rỗng)            | 361      | - Predict `{}`: **148** <br>- Predict GT rỗng: **213**   <br>+, Job Roles: Học sinh = **45 (12.4%)**    <br>+, Còn lại 168: **111 False (30.7%)**, **57 True** | Accuracy = (148+57)/361 = **56.73%**<br><br>Học sinh: 12.4% <br><br>False: 30.7 % | 1. Bổ sung lộ trình cho Role: Học sinh, Sinh viên <br><br>2. Các trường hợp False điền thông tin khiến AI khó Query => AI trả ra lộ trình không quá liên quan đến Job Roles AI đề xuất. Chẳng hạn: <br>- **Noise / chữ vô nghĩa** (_Gbb, Kkk, Beeeeee…_).<br>- **Role không rõ ràng hoặc quá chung chung** (_Nhân viên, Senior, Applicant, Just staff…_).<br>- **Sai domain / mapping lệch** (ví dụ _Đầu bếp → BĐS_).<br>- **Level học tập thay vì nghề** (_Sinh viên, Thực tập sinh, hs, Cấp 2…_). |
| Có **1 phần tử**       | 891      | - Predict True (TP): **849** <br>- Predict False (FN): **42**                                                                                                  | Accuracy ≈ **95.3%**                                                              | - Cần check kỹ để bổ sung vào `description`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Có **≥ 2 phần tử**     | 1706     | - TP ≥1 (ít nhất đúng 1 phần tử): **1436** - TP = 0 (sai hoàn toàn): **270**                                                                                   | TP đạt ≥1: **84.2%**                                                              | Các case này cũng cần check kỹ để bổ sung vào `description`.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ### Accuracy chung<br> |          | 205 + 849 + 1436 = **2489**  <br>=> 83.8%                                                                                                                      |                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
