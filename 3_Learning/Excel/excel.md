

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