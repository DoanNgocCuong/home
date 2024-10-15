- Đường link read: 
	- API Guide: https://lark-base-team.github.io/js-sdk-docs/en/api/guide
	
	- [Automations (larksuite.com)](https://www.larksuite.com/hc/en-US/category/7187737994626039813-automations)
  
```

File: [Obtain access tokens - Server API - Documentation - Lark Developer (larksuite.com)](https://open.larksuite.com/document/server-docs/getting-started/api-access-token/app-access-token-development-guide)

- tenant_access_token
	If your business logic does not require operating on user data resources and only needs to operate on the app's own resources, such as creating a cloud document in the app's document directory space, it is recommended to use the tenant_access_token without requiring additional authorization.

  

- user_access_token
	If your business logic needs to operate the user's data resources, for example, you need to create a cloud document under the user's document directory space, it is recommended to use user_access_token without additional application for authorization.
	If the tenant_access_token is used in this case, you need to additionally add the corresponding authorization for the app at the resource level. For example, if you call the contacts API using the tenant_access_token, you need to configure the app's contacts permission range on the Lark Developer Console's permission management page. However, if you use the user_access_token, you do not need to configure the contacts permission range separately. It follows the contacts permission range of the user_access_token owner.
```

```
Để sử dụng **API của Lark** cho ứng dụng của bạn, có hai loại **token** chính để xác thực:

1. **tenant_access_token**: 
   - Token này dùng để thực hiện các tác vụ chỉ liên quan đến tài nguyên của chính ứng dụng, không cần truy cập đến dữ liệu cá nhân của người dùng. Ví dụ như tạo tài liệu trong không gian lưu trữ của ứng dụng mà không cần sự cho phép từ phía người dùng.
   - Nếu cần truy cập tài nguyên cấp cao hơn (ví dụ như API danh bạ), bạn cần cấu hình quyền truy cập cho ứng dụng trên trang **Permission Management** của Lark Developer Console.

2. **user_access_token**: 
   - Token này được dùng khi bạn cần thực hiện các thao tác liên quan đến dữ liệu cá nhân của người dùng, chẳng hạn như tạo tài liệu trong không gian lưu trữ của người dùng. Token này không yêu cầu thêm bất kỳ cấu hình quyền nào, vì nó dựa trên quyền của chủ sở hữu token.

Như vậy, bạn sử dụng **tenant_access_token** khi không cần truy cập dữ liệu người dùng và **user_access_token** khi cần thao tác với dữ liệu cá nhân của người dùng.

**Link tham khảo**:
- [Obtain Access Tokens - Lark Developer](https://open.larksuite.com/document/server-docs/getting-started/api-access-token/app-access-token-development-guide)

```

## Cách để connect: Pipeline: DATA -> API/APP -> DATABASE (MongoDB, Excel sử dụng AppsScripts, Larkbase)

Video hướng dẫn: https://youtu.be/zrJH3xJRzAA?feature=shared
Playlist: [Hướng dẫn tự động truyền dữ liệu khách hàng trên Ladipage về Base (youtube.com)](https://www.youtube.com/playlist?list=PLLoxrqyIDp4FQTEvBvnoSAKvV4PI8g0I2)

![[Pasted image 20241015161253.png]]

### 2.1 Cách connect App với Larkbase
1. Create App: [Lark Developer (larksuite.com)](https://open.larksuite.com/app)
2. Submit release app: [Review custom apps - Developer Guides - Documentation - Lark Developer (larksuite.com)](https://open.larksuite.com/document/best-practices/intro-to-custom-app-review)
3. Quản lý các app đã tạo: [App Management - Lark Admin Console (larksuite.com)](https://csg2ej4iz2hz.sg.larksuite.com/admin/appCenter/manage)
(Sau khi submit xong, vào larkbase để import Application mà vẫn chưa được)
Cuối cùng nhận ra  phần IMPORT QUYỀN ở: `Permissions & Scopes` tích `All` rùi thật ra vẫn chưa được, phải vào `Docs`
### Define App
- API of APP: https://open.larksuite.com/api-explorer/
![[Pasted image 20241015173324.png]]
- `app_token`: vào từng app để lấy "APP Secret" : để biết bạn dùng app nào? 

[Update a record - Server API - Documentation - Lark Developer (larksuite.com)](https://open.larksuite.com/document/server-docs/docs/bitable-v1/app-table-record/update?appId=cli_a7848edc6b7a9010)

### 2.2 WebHook - Larksuite ? 
- https://botbuilder.larksuite.com/ - Flow? 

## 2.3 API DIRECTLY TO LARKBASE: 
- [Create a record - Server API - Documentation - Lark Developer (larksuite.com)](https://open.larksuite.com/document/server-docs/docs/bitable-v1/app-table-record/create)
	- Access token có thể là `tenant_access_token` (dành cho ứng dụng) hoặc `user_access_token` (dành cho người dùng cụ thể).
	- CÁI App (KHẢ NĂNG LÀ APP CÓ UI của 2.1) nó hiển thị lên làm mình cứ tìm mãi cái `app_token` của cái app đó. Sau mới nhận ra
		- `app_token` là mã định danh của ứng dụng Base,  `gpt bảo`
		- và `table_id` là mã định danh của bảng dữ liệu bạn muốn thêm record. (Cũng đi tìm mã định danh, sau nhận ra nó ở ngay trên cái đường link: `[‍​​﻿﻿​⁠‌​​⁠‌﻿​﻿​‌​​‍​​﻿​⁠﻿‌‍​​‌​​​​​​‍⁠​‍⁠‌​‌‍​‬​​Untitled base - Lark Docs (larksuite.com)](https://csg2ej4iz2hz.sg.larksuite.com/base/HTJ6bPPPfaelL5sKDVglGHHOgCg?table=tblpgKokUDFf7cFn&view=vewoxkJT8q)`


![[Pasted image 20241015200656.png]]



