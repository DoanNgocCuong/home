---
layout: post
title: "Bài 1: Nguyên lý của các mô hình tạo ảnh và so sánh GANs-VAEs"
date: 2024-07-27
categories: blog
---

### Bài 1: ***Nguyên lý của các mô hình tạo ảnh khác gì so với các mô hình gen văn bản và so sánh kiến trúc GANs-VAEs trong việc Gen Ảnh***

### Phần 1: Khác biệt giữa mô hình tạo ảnh và mô hình gen văn bản
**Sự khác biệt chính:**
- **Kiến trúc mạng:** Mô hình tạo ảnh thường dùng GANs hoặc VAEs, trong khi mô hình gen văn bản dùng Transformer.
- **Nguyên lý hoạt động:**
    - **Mô hình gen văn bản (Text Generation Models):**
    Nguyên lý hoạt động chủ yếu là Predict Next Token (Dự đoán từ tiếp theo). Mô hình này dựa vào ngữ cảnh của các từ trước đó để đưa ra dự đoán cho từ hoặc token tiếp theo trong câu. Ví dụ, khi nhận được một đoạn văn bản đầu vào, mô hình sẽ phân tích ngữ cảnh và đưa ra từ tiếp theo sao cho câu văn vẫn giữ được ý nghĩa.
    - **Mô hình tạo ảnh (Image Generation Models):**
    Nguyên lý hoạt động chủ yếu là Generate Image from Latent Space (Tạo hình ảnh từ không gian tiềm ẩn). Mô hình này mã hóa thông tin từ một đoạn văn bản mô tả hoặc từ một nguồn ngẫu nhiên, sau đó giải mã để tạo ra hình ảnh mới tương ứng với thông tin đó.


**Mô hình tạo ảnh:**
- **Nguyên lý hoạt động:** Sử dụng mạng nơ-ron sâu như GANs hoặc VAEs để tạo ra hình ảnh từ mô tả văn bản.
- **Quá trình huấn luyện:** Được huấn luyện trên hàng triệu hình ảnh có chú thích để hiểu mối liên hệ giữa mô tả và hình ảnh.
- **Đầu vào:** Đoạn văn bản mô tả (prompt) và các tham số điều chỉnh. => **Đầu ra:** Hình ảnh phù hợp với mô tả.

### Phần 2: So sánh kiến trúc GANs và VAEs (DALL-E3 và Stable Diffusion)

**Khác biệt chính:**
- **Kiến trúc mạng:** GANs sử dụng hai mạng cạnh tranh (Generator và Discriminator), trong khi VAEs sử dụng một mạng với Encoder và Decoder để mã hóa và giải mã.

**GANs (Generative Adversarial Networks):**
- **Dữ liệu huấn luyện:** Huấn luyện trên tập hợp lớn các hình ảnh thật, có hoặc không có nhãn lớp.
- **Nguyên lý hoạt động:** Generator và Discriminator được huấn luyện cùng nhau trong một quá trình cạnh tranh. Generator cố gắng tạo ra hình ảnh ngày càng giống thật hơn để đánh lừa Discriminator.
- **Kiến trúc:**
    - **Generator:** Tạo ra hình ảnh mới từ một không gian ngẫu nhiên hoặc từ mô tả cụ thể.
    - **Discriminator:** Phân biệt giữa hình ảnh thật và hình ảnh giả.
    - **Quá trình cạnh tranh:** Generator và Discriminator cạnh tranh liên tục, giúp cải thiện chất lượng hình ảnh giả.

**VAEs (Variational Autoencoders):**
- **Dữ liệu huấn luyện:** Huấn luyện trên tập hợp lớn các hình ảnh không cần nhãn.
- **Nguyên lý hoạt động:** Tối ưu hóa để tái tạo lại dữ liệu đầu vào và học được biểu diễn tiềm ẩn của dữ liệu.
- **Kiến trúc:**
    - **Encoder:** Mã hóa dữ liệu đầu vào thành một phân phối tiềm ẩn.
    - **Decoder:** Giải mã từ phân phối tiềm ẩn để tái tạo lại hình ảnh gốc.
    - **Quá trình tối ưu hóa:** Tối ưu hóa mất mát tái tạo và độ lệch Kullback-Leibler để đảm bảo tính chính xác và tính ngẫu nhiên của biểu diễn tiềm ẩn.

**Ứng dụng:**
- **DALL-E3:** Sử dụng các yếu tố từ kiến trúc GANs để tạo ra hình ảnh từ văn bản mô tả.
- **Stable Diffusion:** Sử dụng VAEs để tạo ra hình ảnh từ biểu diễn tiềm ẩn và khuếch tán nó để tạo ra hình ảnh chi tiết hơn.
