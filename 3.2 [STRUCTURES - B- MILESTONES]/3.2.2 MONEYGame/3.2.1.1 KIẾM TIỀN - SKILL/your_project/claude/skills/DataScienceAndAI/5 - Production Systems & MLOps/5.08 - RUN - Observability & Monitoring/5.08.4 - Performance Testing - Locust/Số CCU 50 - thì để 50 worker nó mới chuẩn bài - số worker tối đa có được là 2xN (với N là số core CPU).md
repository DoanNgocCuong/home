
# 1. Ví dụ: https://github.com/DoanNgocCuong/locust_stresst_Testing


## 1.1 Trường hợp test quên nâng NUMBER_WORKER_UVICORN

Với kết quả test 

![](image/Pasted%20image%2020251203143513.png)

https://github.com/DoanNgocCuong/locust_stresst_Testing/blob/main/3_ContextHandling_Robot/results/report.md

Chẳng hạn như kết quả này thì P95, P99 rất ấn tượng với 340ms . 

Nhưng thật ra đây mới chỉ là nâng : max_connections (100) và bật song song cho RABBITMQ với 2 chỉ số (số workers replicas*số thread)

=> tức đã quên nâng  NUMBER_WORKER_UVICORN