

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


|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
|20/08/2025|GroundTruth loại|Tổng mẫu|Phân tích chi tiết|Kết quả chính|% Accuracy so với Loại|% Accuracy so với Tổng|Lý do|
|Cường bé|{} (rỗng)|361|- Predict {}: 148  <br>- Predict GT rỗng: 213  <br>• Học sinh = 45 (12.4%)  <br>• Còn lại 168: 111 False (30.7%), 57 True|Accuracy = (148+57)/361 = 205/361|56.70%|6.91%|1. Bổ sung lộ trình cho Role: Học sinh, Sinh viên. 2. Trường hợp False chủ yếu do:  <br>- Noise / chữ vô nghĩa (Gbb, Kkk, Beeeeee…)  <br>- Role không rõ hoặc quá chung chung (Nhân viên, Senior, Applicant…)  <br>- Sai domain / mapping lệch (Đầu bếp → BĐS)  <br>- Level học tập thay vì nghề (Sinh viên, Thực tập sinh, hs, Cấp 2…).|
||Có 1 phần tử|891|- Predict True (TP): 849  <br>- Predict False (FN): 42|Accuracy ≈ 849/891|95.30%|28.61%|Cần check kỹ để bổ sung thêm vào description.|
||Có ≥ 2 phần tử|1706|- TP ≥ 1 (đúng ≥ 1 phần tử): 1436  <br>- TP = 0 (sai hoàn toàn): 270|TP ≥ 1 đúng = 1436/1706|84.20%|48.38%|Các case này cũng cần check kỹ để bổ sung vào description.|
||Tổng hợp chung|2968|Đúng = 205 + 849 + 1436 = 2489|Accuracy chung = 2489/2968|83.80%|83.89%|—|
