SSH key gồm cặp private key (khóa bí mật) và public key (khóa công khai), hoạt động theo mã hóa bất đối xứng để xác thực an toàn hơn mật khẩu.nhanhoa+1

## Private vs Public Key

Private key giống "chìa khóa cá nhân" chỉ bạn giữ trên máy Mac (file `id_rsa`), tuyệt đối không chia sẻ vì ai có nó sẽ truy cập được server như bạn.[[vutruso](https://vutruso.com/ssh-key/)]​  
Public key giống "ổ khóa" (file `id_rsa.pub`), bạn gửi lên server để lưu trong `~/.ssh/authorized_keys` – ai cũng có thể xem nhưng vô hại vì chỉ mã hóa, không giải mã được.fptshop.com+1  
Cơ chế: Khi ssh vào server, Mac dùng private key mã hóa một thông điệp thử thách từ server; server dùng public key giải mã kiểm tra khớp → cho phép vào không cần mật khẩu.topon+1

## Tạo Key trên Mac

Mở Terminal (Spotlight tìm "Terminal").  
Chạy: `ssh-keygen -t ed25519 -C "email@ban.vn"` (nhấn Enter 3 lần: đường dẫn mặc định, không passphrase để đơn giản).[[hocvps](https://hocvps.com/ssh-keys-login/)]​  
Kết quả: `~/.ssh/id_ed25519` (private) và `id_ed25519.pub` (public) – copy public bằng `pbcopy < ~/.ssh/id_ed25519.pub` rồi paste lên server.[[hocvps](https://hocvps.com/ssh-keys-login/)]​