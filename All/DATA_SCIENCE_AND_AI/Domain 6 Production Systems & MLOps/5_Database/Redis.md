

Redis là một hệ thống lưu trữ dữ liệu dạng key-value hoạt động chủ yếu trên bộ nhớ RAM, nổi bật với tốc độ truy xuất cực nhanh và được ứng dụng rộng rãi trong nhiều lĩnh vực công nghệ hiện đại.[viettelidc+3](https://viettelidc.com.vn/tin-tuc/redis-la-gi-tat-tan-tat-uu-nhuoc-diem-va-ung-dung)

## Ứng dụng thực tế của Redis

- **Lưu cache dữ liệu:** Redis thường được dùng để lưu trữ dữ liệu tạm thời (cache) cho các ứng dụng web, giúp giảm tải cho cơ sở dữ liệu chính và tăng tốc độ truy cập.[topdev+3](https://topdev.vn/blog/redis-la-gi/)
    
- **Quản lý phiên người dùng:** Redis lưu trữ thông tin phiên đăng nhập, trạng thái người dùng, giỏ hàng... giúp các website và ứng dụng web hoạt động mượt mà hơn.[devwork+2](https://devwork.vn/blog/redis-la-gi)
    
- **Nhắn tin thời gian thực:** Redis hỗ trợ tính năng pub/sub, cho phép gửi và nhận thông tin theo thời gian thực, rất phù hợp cho hệ thống chat, bảng tin, cập nhật giá chứng khoán....[online.unicode+2](https://online.unicode.vn/bai-viet/kham-pha-redis-co-so-du-lieu-nhanh-nhu-chop-va-linh-hoat)
    
- **Thống kê, phân tích dữ liệu thời gian thực:** Redis lưu trữ và xử lý các thống kê như lượt truy cập, tương tác người dùng, dữ liệu cảm biến... với tốc độ cực nhanh.[viettelidc+2](https://viettelidc.com.vn/tin-tuc/redis-la-gi-tat-tan-tat-uu-nhuoc-diem-va-ung-dung)
    
- **Hàng đợi xử lý (Queue):** Redis hỗ trợ cấu trúc danh sách, giúp xây dựng các hàng đợi để xử lý tác vụ bất đồng bộ như gửi email, xử lý dữ liệu.[topdev+2](https://topdev.vn/blog/redis-la-gi/)
    
- **Ứng dụng trong game online và IoT:** Redis lưu trữ trạng thái game, bảng xếp hạng, dữ liệu thiết bị thông minh, giúp đồng bộ hóa và quản lý hiệu quả.[online.unicode+1](https://online.unicode.vn/bai-viet/kham-pha-redis-co-so-du-lieu-nhanh-nhu-chop-va-linh-hoat)
    

## Ưu điểm và nhược điểm

- **Ưu điểm:** Tốc độ truy xuất cực nhanh, hỗ trợ nhiều kiểu dữ liệu, dễ tích hợp với nhiều ngôn ngữ lập trình, phù hợp cho các ứng dụng thời gian thực.[devwork+3](https://devwork.vn/blog/redis-la-gi)
    
- **Nhược điểm:** Do lưu trữ trên RAM, Redis có thể tiêu tốn nhiều bộ nhớ nếu dữ liệu lớn; cần cấu hình thêm để đảm bảo an toàn và bảo mật dữ liệu.[online.unicode](https://online.unicode.vn/bai-viet/kham-pha-redis-co-so-du-lieu-nhanh-nhu-chop-va-linh-hoat)
    

Redis rất phù hợp để bắt đầu học về các công nghệ backend, tối ưu hiệu suất hệ thống, và xây dựng các ứng dụng web hiện đại.[viettelidc+3](https://viettelidc.com.vn/tin-tuc/redis-la-gi-tat-tan-tat-uu-nhuoc-diem-va-ung-dung)

1. [https://viettelidc.com.vn/tin-tuc/redis-la-gi-tat-tan-tat-uu-nhuoc-diem-va-ung-dung](https://viettelidc.com.vn/tin-tuc/redis-la-gi-tat-tan-tat-uu-nhuoc-diem-va-ung-dung)
2. [https://topdev.vn/blog/redis-la-gi/](https://topdev.vn/blog/redis-la-gi/)
3. [https://viblo.asia/p/redis-va-nhung-ung-dung-cua-redis-m68Z0zbz5kG](https://viblo.asia/p/redis-va-nhung-ung-dung-cua-redis-m68Z0zbz5kG)
4. [https://200lab.io/blog/redis-la-gi/](https://200lab.io/blog/redis-la-gi/)
5. [https://devwork.vn/blog/redis-la-gi](https://devwork.vn/blog/redis-la-gi)
6. [https://online.unicode.vn/bai-viet/kham-pha-redis-co-so-du-lieu-nhanh-nhu-chop-va-linh-hoat](https://online.unicode.vn/bai-viet/kham-pha-redis-co-so-du-lieu-nhanh-nhu-chop-va-linh-hoat)
7. [https://vietnix.vn/redis-la-gi/](https://vietnix.vn/redis-la-gi/)
8. [https://viblo.asia/p/tim-hieu-ve-redis-LzD5dXEW5jY](https://viblo.asia/p/tim-hieu-ve-redis-LzD5dXEW5jY)

---
# Redis GUI: 

https://github.com/redis/RedisInsight


29999
```bash
docker run -d -p 29999:8001 --name redisinsight redislabs/redisinsight:latest

```

Redis GUI: 

RedisInsight là một công cụ GUI trực quan giúp quản lý, phân tích và tối ưu hóa cơ sở dữ liệu Redis. Để sử dụng RedisInsight trên server, có thể triển khai theo các cách sau:

- RedisInsight có thể chạy dưới dạng ứng dụng desktop hoặc dưới dạng Docker container trên server.
- Cách phổ biến là chạy RedisInsight bằng Docker trên server để dễ dàng quản lý và truy cập từ xa qua trình duyệt web.



# Bug: 
- https://github.com/redis/RedisInsight/issues/5035

---
# 5. How to connect Redis with key 

```bash
REDIS_HOST=robot-ai-workflow-redis-master  
REDIS_PASSWORD=123456aA@  
REDIS_PORT=6379
```

---

```bash
θ78° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± ss -lntp | grep 6379
LISTEN    0         511                0.0.0.0:46379            0.0.0.0:*                                                                                       
LISTEN    0         511              127.0.0.1:6379             0.0.0.0:*                                                                                       
LISTEN    0         511                0.0.0.0:36379            0.0.0.0:*                                                                                       
LISTEN    0         511                   [::]:46379               [::]:*                                                                                       
LISTEN    0         511                  [::1]:6379                [::]:*                                                                                       
LISTEN    0         511                   [::]:36379               [::]:*                                                                                       
θ75° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± sudo iptables -S | grep 6379
[sudo] password for ubuntu: 
-A DOCKER -d 170.28.0.5/32 ! -i br-225955f83245 -o br-225955f83245 -p tcp -m tcp --dport 6379 -j ACCEPT
θ74° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± getent hosts robot-ai-workflow-redis-master || nslookup robot-ai-workflow-redis-master
;; Got SERVFAIL reply from 127.0.0.53
Server:         127.0.0.53
Address:        127.0.0.53#53

** server can't find robot-ai-workflow-redis-master: SERVFAIL

θ77° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± ss -lntp | grep 6379

```

### Hiện tại: 
Mọi chương trình/bot/container khác không nằm trên server này 
(hoặc trong Docker network khác) sẽ **không thể kết nối bằng hostname hoặc IP mạng** (robot-ai-workflow-redis-master).

 **Muốn các service khác (ví dụ một microservice hoặc một bot ở cụm khác) kết nối được bằng hostname `robot-ai-workflow-redis-master`, bạn cần:**

## 1. **Cấu hình lại Redis để listen trên network interface**

- **Chỉnh file cấu hình** (thường tên là `redis.conf`):
    Tìm dòng:
    `bind 127.0.0.1`
    Đổi thành:    
    `bind 0.0.0.0`
    (hoặc bind cụ thể IP private nếu cần)
    
- **Tắt chế độ protected mode (Chỉ dùng khi đã khóa port bằng firewall):**
    `protected-mode no`
    
- **Restart Redis:**

```bash
sudo systemctl restart redis
# hoặc trong Docker:
docker restart <tên_redis_container>

```
    

## 2. **Kiểm tra cho chắc chắn**
```bash
ss -lntp | grep 6379

=> LISTEN ... 0.0.0.0:6379 ...
=> LISTEN ... <IP mạng>:6379 ...

=> **Lúc đó**, từ bất cứ máy/service nào nhìn thấy hostname `robot-ai-workflow-redis-master` và truy cập được port 6379, chỉ cần cấu hình:
```


# 6. Check Redis? 

## 6.1 **Có bao nhiêu instance Redis** đang được deploy trên server
```bash
# - `ps aux`: Liệt kê toàn bộ tiến trình (process) đang chạy trên hệ thống.
    
# - `| grep redis-server`: Lọc ra các tiến trình có tên chứa "redis-server" (tức là Redis đang chạy).
ps aux | grep redis-server
```

```bash
θ77° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± ps aux | grep redis-server
redis       2147  0.2  0.0  86024 12100 ?        Ssl  Sep10  91:05 /usr/bin/redis-server 127.0.0.1:6379
dd-agent    6222  0.2  0.0 145696  5760 ?        Ssl  Sep10  92:47 redis-server *:6379
dd-agent   10904  0.2  0.0 145696  5780 ?        Ssl  Sep10  98:44 redis-server *:6379
dd-agent   11171  0.2  0.0 145696  5788 ?        Ssl  Sep10  94:23 redis-server *:6379
dd-agent   11934  0.2  0.0 145696  6236 ?        Ssl  Sep10  97:30 redis-server *:36379
dd-agent   14587  1.0  0.0 163680 11844 ?        Ssl  Sep10 408:39 redis-server *:6379
dd-agent   15130  0.2  0.0  37612  6724 ?        Ssl  Sep10  96:01 redis-server *:6379
dd-agent   15609  0.2  0.0 145696  6300 ?        Ssl  Sep10  96:02 redis-server *:46379
dd-agent   15638  0.2  0.0 145692  6396 ?        Ssl  Sep10  95:57 redis-server *:6379
dd-agent   15721  0.2  0.0 145696  5796 ?        Ssl  Sep10  96:34 redis-server *:6379
dd-agent   15722  0.2  0.0 148256  6136 ?        Ssl  Sep10  99:12 redis-server *:6379
dd-agent   17290  0.2  0.0 145696  5772 ?        Ssl  Sep10  96:11 redis-server *:6379
dd-agent   17438  0.2  0.0  40172  7120 ?        Ssl  Sep10 100:26 redis-server *:6379
dd-agent   23708  0.2  0.0 145696  6068 ?        Ssl  Sep10  97:52 redis-server *:6379
dd-agent   24041  0.2  0.0 148252  7808 ?        Ssl  Sep10  97:34 redis-server *:6379
dd-agent   24053  0.2  0.0 145696  5780 ?        Ssl  Sep10  94:53 redis-server *:6379
dd-agent  288482  0.2  0.0  69916  6824 ?        Ssl  Sep17  62:16 redis-server *:6379
dd-agent 1298457  0.2  0.0  69912  6016 ?        Ssl  Sep17  61:49 redis-server *:6379
dd-agent 1323075  0.2  0.0  69916  6732 ?        Ssl  Sep17  62:27 redis-server *:6379
dd-agent 1528618  1.1  0.0 161632 11964 ?        Ssl  Sep10 418:20 redis-server *:6379
dd-agent 2088274  0.2  0.0 145692  9364 ?        Ssl  15:26   0:12 redis-server *:6379
dd-agent 3320724  0.2  0.0  69912  7552 ?        Ssl  Oct03   9:49 redis-server *:6379
dd-agent 3797411  0.2  0.0  83228  9972 ?        Ssl  Oct01  15:22 redis-server *:6379
ubuntu   3889703  0.0  0.0   8168  2492 pts/2    S+   16:45   0:00 grep --color=auto redis-server
dd-agent 3968994  1.2  0.0 153608 12232 ?        Ssl  Sep18 326:48 redis-server *:6379
θ79° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workflow] manual-refactor-agent-registry(+32/-818,+1/-1)+ ± 
```