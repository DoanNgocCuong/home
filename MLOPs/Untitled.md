1. Triển khai Docker (Từ máy chủ vật lý - Virtualization - Containerlization):

- Virtualization: Virtualization gặp vấn đề về lãng phí tài nguyên và thời gian. Tài nguyên như RAM được phân bổ cố định cho mỗi máy ảo, dẫn đến lãng phí nếu máy ảo không sử dụng hết tài nguyên đó + Thời gian khởi động máy ảo đến vài phút
    
- Containerlization: Đóng gói phần mềm và phụ thuộc vào 1 container riêng biệt. **Docker** là một nền tảng mã nguồn mở phổ biến nhất để tạo, triển khai và quản lý các container.
    
    - Triển khai môi trường nhanh chóng, giảm xung đột (giữa các gói requirements: thư viện, mã nguồn, cấu hình, các hệ điều hành, …)
    - Tính tương thích với cả 3 hệ điều hành: Window, MacOS, Ubutun
    
    (Ban đầu, Docker chủ yếu hỗ trợ các container Linux. Tuy nhiên, hiện nay Docker cũng hỗ trợ chạy các container Windows khi đang chạy trên hệ điều hành Windows)
    
- **Dockerfile - Docker Image - Docker Container**
    
    - **Dockerfile** giống như bản vẽ thiết kế ngôi nhà, ghi rõ cần những gì để xây dựng ngôi nhà. Dockerfile định nghĩa cấu hình và các bước cần thiết để xây dựng một Docker Image.
    - **Docker Image** là ngôi nhà đã được xây xong nhưng chưa có ai ở. Nó chứa tất cả các thành phần cần thiết để chạy ứng dụng.
    - **Docker Container** là ngôi nhà có người ở và đang hoạt động. Khi "mở" Docker Image, bạn sẽ có một Docker Container - ngôi nhà đang được sử dụng.

References:

1. [https://viblo.asia/p/docker-chua-biet-gi-den-biet-dung-phan-1-lich-su-ByEZkWrEZQ0](https://viblo.asia/p/docker-chua-biet-gi-den-biet-dung-phan-1-lich-su-ByEZkWrEZQ0)

Docker from ProtonX

[ProtonX](https://www.facebook.com/share/p/B8MFbSLV9X56HQeD/)

Git

Các chuyên gia lập trình thường sử dụng các quy trình quản lý phiên bản (version control) một cách cẩn thận và có tổ chức để đảm bảo rằng dự án phát triển ổn định, dễ theo dõi và có thể phối hợp giữa nhiều người. Dưới đây là một số phương pháp phổ biến và thực tiễn tốt mà họ thường áp dụng khi quản lý phiên bản:

### 1. **Git Flow - Quy trình quản lý nhánh (branching model)**

Git Flow là một mô hình quản lý các nhánh trong Git được sử dụng rộng rãi, giúp cho việc phát triển, thử nghiệm, và phát hành các phiên bản trở nên rõ ràng và có hệ thống. Trong Git Flow, có một số nhánh cơ bản:

- **`main` (hoặc `master`)**: Nhánh này chứa mã đã sẵn sàng để phát hành (production). Mỗi khi có một phiên bản ổn định của sản phẩm (ví dụ, `v1.0`, `v2.0`), nhánh này sẽ được cập nhật.
- **`develop`**: Nhánh phát triển chính, nơi tất cả các tính năng mới được hợp nhất. Mọi thay đổi lớn sẽ được tích hợp ở đây trước khi sẵn sàng cho production.
- **Feature branches (nhánh tính năng)**: Mỗi tính năng mới hoặc cải tiến được phát triển trên các nhánh riêng biệt dựa trên nhánh `develop`. Điều này giúp làm việc độc lập mà không ảnh hưởng đến mã gốc cho đến khi sẵn sàng.
- **Release branches (nhánh phát hành)**: Khi nhánh `develop` đã sẵn sàng để phát hành, một nhánh phát hành mới được tạo ra để chuẩn bị cho các thử nghiệm cuối cùng, sửa lỗi, và phát hành.
- **Hotfix branches (nhánh sửa lỗi nóng)**: Khi phát hiện ra lỗi nghiêm trọng trong phiên bản đã phát hành, các lập trình viên tạo ra các nhánh hotfix từ nhánh `main` để sửa lỗi nhanh chóng và sau đó hợp nhất lại vào `main` và `develop`.

### Quy trình Git Flow cơ bản:

1. **Phát triển tính năng mới**: Tạo một nhánh tính năng từ `develop`, phát triển tính năng, và sau đó hợp nhất nó vào `develop` khi hoàn thành.
2. **Chuẩn bị phát hành**: Khi các tính năng mới sẵn sàng, tạo một nhánh phát hành từ `develop`, kiểm tra, sửa lỗi, và cuối cùng hợp nhất vào cả `main` và `develop`.
3. **Phát hành sản phẩm**: Đánh dấu phiên bản (tag) trên `main` và phát hành. Sau khi phát hành, nhánh phát hành có thể được xóa.
4. **Sửa lỗi khẩn cấp**: Nếu phát hiện lỗi trong phiên bản sản phẩm, tạo nhánh hotfix từ `main`, sửa lỗi và hợp nhất vào `main` và `develop`.

### 2. **Sử dụng Tag để quản lý phiên bản**

Các chuyên gia thường sử dụng **tags** để đánh dấu các phiên bản cụ thể của dự án, đặc biệt là những phiên bản đã phát hành ra môi trường sản xuất (production). Các tag này thường tuân theo hệ thống quản lý phiên bản ngữ nghĩa (Semantic Versioning):

- **Phiên bản ngữ nghĩa** có định dạng `MAJOR.MINOR.PATCH`:
    - **MAJOR**: Tăng khi có thay đổi lớn, không tương thích ngược (backward-incompatible).
    - **MINOR**: Tăng khi thêm tính năng mới nhưng vẫn tương thích với các phiên bản cũ.
    - **PATCH**: Tăng khi sửa lỗi hoặc thực hiện các thay đổi nhỏ mà không ảnh hưởng đến API hoặc tính năng lớn.

Ví dụ: `v1.0.0`, `v1.1.0`, `v1.1.1`.

Việc sử dụng phiên bản ngữ nghĩa giúp người dùng và các lập trình viên khác dễ dàng hiểu được mức độ thay đổi của từng phiên bản.

### 3. **Sử dụng Continuous Integration/Continuous Deployment (CI/CD)**

Các chuyên gia lập trình thường tích hợp **CI/CD** vào quy trình quản lý phiên bản để tự động hóa việc kiểm tra mã và triển khai sản phẩm. Quy trình này bao gồm:

- **Continuous Integration (CI)**: Mỗi khi có thay đổi mã, hệ thống CI sẽ tự động chạy các bài kiểm tra (tests) để đảm bảo rằng không có lỗi mới phát sinh. Điều này giúp phát hiện lỗi sớm trong quá trình phát triển.
- **Continuous Deployment (CD)**: Khi mã đã vượt qua các bài kiểm tra CI, hệ thống sẽ tự động triển khai sản phẩm lên môi trường thử nghiệm hoặc sản xuất.

Nhờ CI/CD, việc phát hành phiên bản mới trở nên nhanh chóng và đáng tin cậy hơn.

### 4. **Sử dụng công cụ quản lý phiên bản (Version Management Tools)**

Ngoài Git, nhiều đội ngũ phát triển sử dụng các công cụ bổ trợ để theo dõi, kiểm soát và quản lý các phiên bản:

- **GitHub Releases**: GitHub cung cấp tính năng **Releases** giúp quản lý và ghi chú lại các phiên bản phát hành. Bạn có thể liên kết tag với release, thêm ghi chú phát hành (release notes) và đính kèm file nếu cần.
- **Changelog**: Các lập trình viên chuyên nghiệp thường duy trì một file **CHANGELOG** trong dự án để theo dõi tất cả các thay đổi qua các phiên bản. Điều này rất hữu ích để ghi lại các thay đổi quan trọng, bug fixes, và các tính năng mới.

### 5. **Kiểm soát xung đột (Conflict Management)**

Trong các dự án lớn, việc nhiều người cùng làm việc trên các nhánh khác nhau có thể dẫn đến xung đột khi hợp nhất (merge). Để giảm thiểu xung đột:

- **Merge thường xuyên**: Liên tục hợp nhất các nhánh phát triển (feature branches) với nhánh `develop` để tránh việc các nhánh đi quá xa nhau và khó hợp nhất.
- **Code Reviews**: Trước khi hợp nhất mã, các chuyên gia thường sử dụng quy trình **code review** để đảm bảo rằng mã được viết đúng tiêu chuẩn và không gây ra lỗi.
- **Automated Testing**: Việc sử dụng các bài kiểm tra tự động (unit test, integration test) giúp phát hiện xung đột và lỗi trong mã trước khi hợp nhất.

### 6. **Sử dụng Branch Protection Rules và Pull Requests (PRs)**

Các chuyên gia cũng thường áp dụng **quy tắc bảo vệ nhánh (branch protection rules)** để bảo vệ nhánh `main` hoặc `develop` khỏi các thay đổi không kiểm soát. Quy tắc này yêu cầu tất cả các thay đổi phải được kiểm tra (code review) thông qua **pull request (PR)** và phải vượt qua các bài kiểm tra tự động trước khi hợp nhất.

---

### Tóm lại:

- **Git Flow** là một trong những quy trình quản lý phiên bản phổ biến, giúp các chuyên gia dễ dàng quản lý nhánh và các phiên bản.
- **Tag** và **semantic versioning** được sử dụng để ghi lại các phiên bản quan trọng của dự án.
- **CI/CD** và các công cụ hỗ trợ giúp tự động hóa và kiểm soát quá trình phát triển.
- Quy trình **merge thường xuyên**, **code reviews**, và **test tự động** giúp giảm thiểu rủi ro xung đột và lỗi.

Bạn có thể áp dụng một hoặc nhiều quy trình và công cụ này tùy thuộc vào quy mô và yêu cầu của dự án.


List of API: [public-api-lists/public-api-lists at dailydev (github.com)](https://github.com/public-api-lists/public-api-lists?ref=dailydev)