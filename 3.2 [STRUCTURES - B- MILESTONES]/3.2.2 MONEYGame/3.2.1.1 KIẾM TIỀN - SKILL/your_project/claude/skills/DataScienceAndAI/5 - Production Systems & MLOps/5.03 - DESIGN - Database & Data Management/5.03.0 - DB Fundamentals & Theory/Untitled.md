SQL Server

ALTER insert DB bị treo 2h 
Huỷ cục đi => vẫn đang bị roll back 
Temp DB tăng 1.5T


![](image/Pasted%20image%2020251204125323.png)


### Insert chục tiếng, Rollback vài tiếng -> 
Khi kill insert => qua rollback bị treo (rollback là thứ ko xử lý được)
Khi restart thì nó là restart rollback

+, Insert trên nhiều DB dùng DB Ling, trong quá trình rollback nó treo luôn. 
Với bài làm nhiều DB => Rollback xảy ra ở nhiều nơi 
