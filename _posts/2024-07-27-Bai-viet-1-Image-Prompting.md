---
layout: post
title: "Bài 1: Nguyên lý của các mô hình tạo ảnh và so sánh GANs-VAEs"
date: 2024-07-27
categories: blog
---

Bài 1: ***Nguyên lý của các mô hình tạo ảnh khác gì so với các mô hình gen văn bản và so sánh kiến trúc GANs-VAEs trong việc Gen Ảnh***

### Phần 1: Khác biệt giữa mô hình tạo ảnh và mô hình gen văn bản
**Sự khác biệt chính:**
- **Kiến trúc mạng:** Mô hình tạo ảnh dùng GANs/VAEs, mô hình gen văn bản dùng Transformer.
- **Mục tiêu tối ưu hóa:** Mô hình tạo ảnh tạo hình ảnh đúng mô tả, mô hình gen văn bản dự đoán từ tiếp theo hợp lý.

**Mô hình tạo ảnh:**
- **Nguyên lý hoạt động:** Sử dụng mạng nơ-ron sâu như GANs hoặc VAEs để tạo ra hình ảnh từ mô tả văn bản.
- **Quá trình huấn luyện:** Được huấn luyện trên hàng triệu hình ảnh có chú thích để hiểu mối liên hệ giữa mô tả và hình ảnh.
- **Đầu vào:** Đoạn văn bản mô tả (prompt) và các tham số điều chỉnh. => **Đầu ra:** Hình ảnh phù hợp với mô tả.


### Phần 2: So sánh kiến trúc GANs và VAEs (DALL-E3 và Stable Diffusion)

**Khác biệt chính:**
- **Kiến trúc mạng:** GANs sử dụng hai mạng cạnh tranh (Generator và Discriminator), trong khi VAEs sử dụng một mạng để mã hóa và giải mã.
- **Quá trình huấn luyện:** GANs huấn luyện qua quá trình cạnh tranh, trong khi VAEs huấn luyện qua quá trình tối ưu hóa phân phối tiềm ẩn.
- **Mục tiêu:** GANs tập trung vào việc tạo ra hình ảnh giả mà Discriminator không thể phân biệt được, còn VAEs tập trung vào việc tái tạo lại dữ liệu đầu vào và học được biểu diễn tiềm ẩn của dữ liệu.


    **GANs (Generative Adversarial Networks):**
    - **Kiến trúc:** Gồm hai mạng nơ-ron: Generator và Discriminator. Generator tạo ra hình ảnh mới, trong khi Discriminator cố gắng phân biệt giữa hình ảnh thật và giả.
    - **Nguyên lý hoạt động:** Generator và Discriminator được huấn luyện cùng nhau trong một quá trình cạnh tranh. Generator cố gắng tạo ra hình ảnh ngày càng giống thật hơn để đánh lừa Discriminator.
    - **Ví dụ:** DALL-E3 sử dụng các yếu tố từ kiến trúc GANs để tạo ra hình ảnh từ văn bản mô tả, dựa trên một quá trình cạnh tranh giữa các mạng.

    **VAEs (Variational Autoencoders):**
    - **Kiến trúc:** Gồm hai phần chính: Encoder và Decoder. Encoder chuyển đổi dữ liệu đầu vào thành một phân phối tiềm ẩn (latent distribution), sau đó Decoder tái tạo lại hình ảnh từ phân phối này.
    - **Nguyên lý hoạt động:** VAEs tối ưu hóa để tái tạo lại dữ liệu đầu vào và học được biểu diễn tiềm ẩn của dữ liệu, giúp tạo ra hình ảnh mới từ phân phối tiềm ẩn này.
    - **Ví dụ:** Stable Diffusion sử dụng VAEs để tạo ra hình ảnh, bắt đầu từ một biểu diễn tiềm ẩn và khuếch tán (diffuse) nó để tạo ra hình ảnh mới.

**Ứng dụng:**
- **DALL-E3:** Sử dụng các nguyên lý của GANs để tạo ra hình ảnh phức tạp từ văn bản.
- **Stable Diffusion:** Sử dụng VAEs để tạo ra hình ảnh từ biểu diễn tiềm ẩn và khuếch tán nó để tạo ra hình ảnh chi tiết hơn.

