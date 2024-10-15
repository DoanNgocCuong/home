- Đường link read: 
	- https://lark-base-team.github.io/js-sdk-docs/en/api/guide
	
	- https://www.larksuite.com/hc/en-US/articles/125809335872-use-base-to-automate-the-sending-of-http-requests

  
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
