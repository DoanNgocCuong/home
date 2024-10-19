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
https://open.larksuite.com/document/server-docs/docs/bitable-v1/app-table-record/batch_create
https://open.larksuite.com/api-explorer/cli_a7848edc6b7a9010?apiName=tenant_access_token_internal&from=op_doc&project=auth&resource=auth&version=v3


![[Pasted image 20241015200656.png]]


To resolve your issue with the Lark API tokens expiring after 2 hours, you can utilize **refresh tokens** to maintain continuous access without needing to re-authenticate frequently. Here's how it works:

1. **Access and Refresh Tokens**: The Lark API provides short-lived access tokens (valid for a limited time, e.g., 2 hours) and longer-lived refresh tokens. When the access token expires, you can use the refresh token to request a new access token without user interaction​
	- [DEV Community](https://dev.to/tijan_io/access-token-and-refresh-token-a-comprehensive-guide-40g7)
	-  [Auth0](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
2. **Refresh Token Flow**: You will need to implement a mechanism to refresh the access token automatically. This involves making a POST request to the token endpoint using the refresh token. The response will provide a new access token, and possibly a new refresh token as well, extending the session​
    - [OAuth 2.0 Simplified](https://www.oauth.com/oauth2-servers/making-authenticated-requests/refreshing-an-access-token/)
    - [Atlassian Developer](https://developer.atlassian.com/cloud/oauth/getting-started/refresh-tokens/)

**Các thành phần chính:**
- **App ID** và **App Secret**: Đây là hai giá trị **cố định** mà bạn nhận được khi đăng ký ứng dụng của mình với Lark. Chúng không thay đổi, và bạn sẽ sử dụng chúng để lấy **app_access_token** hoặc **tenant_access_token**.
    
- **User Access Token**: Đây là token dùng để xác thực người dùng khi gọi API. Token này **chỉ có hiệu lực trong 2 giờ**. Khi token này hết hạn, bạn cần làm mới (refresh) bằng cách sử dụng **refresh_token**.
    
- **Refresh Token**: Đây là token bạn nhận được cùng với **user access token** và có thời gian tồn tại dài hơn nhiều so với access token (thường kéo dài vài tuần hoặc lâu hơn). Bạn sử dụng **refresh_token** để lấy **user access token mới** mà không cần người dùng đăng nhập lại.
    

Em đang hiểu là:

App ID và App Secret → Lấy App Token.

App Token + Authorization_code → Đổi lấy Access Token.

App Token + Refresh Token -> để refresh Access Token khi hết hạn

-------------

Log conversation của chatbot vào larkbase sử dụng Access Token. <Em đang không biết lấy: Refresh Token, Authorization_code ở đâu>


### 3. Làm thế nào để lấy được **refresh token**?

Để lấy được **refresh token**, bạn cần làm theo các bước sau:

1. **Thực hiện quy trình OAuth 2.0** để lấy **user access token** lần đầu tiên. Khi bạn thực hiện yêu cầu này, hệ thống sẽ trả về cả **user access token** và **refresh token**.
    
    Cách làm:
    
    - Gửi yêu cầu **POST** tới endpoint xác thực của Lark.
    - Endpoint: `https://open.larksuite.com/open-apis/authen/v1/oidc/token`
    - Trong yêu cầu này, bạn cần gửi **App ID**, **App Secret**, và các thông tin xác thực người dùng.
2. **Khi nhận được refresh token**: Lưu trữ token này và sử dụng nó để làm mới **user access token** khi cần thiết.
![[Pasted image 20241016103259.png]]

OAuth 2.0 và OAuth 1.0 đều là cơ chế xác thực giúp các ứng dụng truy cập vào tài khoản của người dùng mà không cần tiết lộ mật khẩu, nhưng chúng có một số điểm khác biệt lớn:

### 1. **Bảo mật tốt hơn**:

- **OAuth 1.0** yêu cầu các ứng dụng sử dụng **chữ ký số** (digital signature) để bảo mật yêu cầu truy cập. Điều này khá phức tạp và khó triển khai.
- **OAuth 2.0** không cần sử dụng chữ ký số nữa. Thay vào đó, nó dựa trên các **token** (mã thông báo), giúp đơn giản hóa quá trình xác thực và bảo mật tốt hơn nhờ sử dụng **HTTPS** để mã hóa yêu cầu.

### 2. **Dễ triển khai hơn**:

- OAuth 2.0 dễ dàng hơn để các nhà phát triển triển khai, nhờ việc loại bỏ yêu cầu phức tạp về chữ ký số. Điều này giúp các ứng dụng dễ dàng tích hợp tính năng "đăng nhập qua Google, Facebook,..." hơn.

### 3. **Nhiều loại luồng xác thực**:

- OAuth 2.0 cung cấp nhiều cách xác thực hơn, chẳng hạn như **Authorization Code Flow**, **Implicit Flow**, **Client Credentials**, và **Password Grant**, phù hợp với nhiều tình huống khác nhau (ứng dụng web, ứng dụng di động, server-to-server,...).
- OAuth 1.0 chủ yếu chỉ có một cách xác thực duy nhất, khiến nó không linh hoạt bằng OAuth 2.0.

    [OAuth 2.0 Simplified](https://www.oauth.com/oauth2-servers/server-side-apps/example-flow/)
    [Ory](https://www.ory.sh/docs/oauth2-oidc/authorization-code-flow)
 [RFC 6749: The OAuth 2.0 Authorization Framework (rfc-editor.org)](https://www.rfc-editor.org/rfc/rfc6749)


Quy trình sử dụng **OAuth 2.0 với Lark** có thể được tóm tắt và hoàn thiện như sau:

### 1. **App ID và App Secret**:

- Đầu tiên, bạn cần sử dụng **App ID** và **App Secret** của ứng dụng đã được đăng ký trên nền tảng Lark để lấy **App Token**. Đây là bước khởi đầu trong quy trình xác thực OAuth 2.0. **App Token** này đóng vai trò là mã xác thực tạm thời cho ứng dụng, cần thiết để lấy các token tiếp theo.

### 2. **Lấy Authorization Code**:

- Khi người dùng đăng nhập và chấp nhận cấp quyền cho ứng dụng của bạn (quyền truy cập vào tài khoản hoặc dữ liệu của họ), bạn sẽ nhận được **Authorization Code** từ máy chủ xác thực. **Authorization Code** là mã tạm thời ngắn hạn, được sử dụng để tiếp tục quy trình lấy **Access Token**.
-  **Refresh Token** được cấp cùng với **Access Token** khi bạn hoàn thành quy trình xác thực OAuth 2.0 lần đầu tiên. Để nhận được **Refresh Token**, bạn cần đảm bảo rằng khi gửi yêu cầu lấy **Authorization Code**, bạn yêu cầu scope `offline_access` để đảm bảo nhận được **Refresh Token** cùng với **Access Token**. (**Authorization Code Flow**)

### 3. **Đổi Authorization Code lấy Access Token**:

- Sau khi có **Authorization Code**, bạn sẽ dùng **App Token** và **Authorization Code** này để gửi yêu cầu lấy **Access Token** từ máy chủ xác thực của Lark. **Access Token** là mã mà ứng dụng sẽ sử dụng để truy cập vào các tài nguyên của người dùng thông qua API. **Access Token** có thời gian tồn tại ngắn (thường là 2 giờ) và sẽ hết hạn sau khoảng thời gian này.

### 4. **Làm mới Access Token bằng Refresh Token**:

- Khi **Access Token** hết hạn, bạn sẽ không cần yêu cầu người dùng đăng nhập lại nếu đã nhận được **Refresh Token**. **Refresh Token** là mã dài hạn, có thể được sử dụng nhiều lần để lấy **Access Token** mới mà không cần sự can thiệp của người dùng. Quy trình làm mới này cho phép ứng dụng duy trì quyền truy cập mà không làm gián đoạn trải nghiệm của người dùng.
- Yêu cầu này thường bao gồm các tham số như:
        - `grant_type=refresh_token`
        - `refresh_token`: là mã bạn nhận được từ bước xác thực ban đầu.
        - `client_id` và `client_secret`: nếu cần thiết.
### Lưu ý:

- **Refresh Token** có thời hạn dài hơn **Access Token** nhưng vẫn có thể hết hạn hoặc bị thu hồi nếu người dùng thay đổi mật khẩu hoặc rút lại quyền truy cập đã cấp cho ứng dụng.
- Bạn cần lưu trữ cả **Access Token** và **Refresh Token** trong cơ sở dữ liệu để sử dụng và làm mới token một cách tự động mà không cần tương tác từ người dùng.
    
    [Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
    [Microsoft Learn](https://learn.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens)​
    [OAuth](https://oauth.net/2/refresh-tokens/)

### SUMMARY VÀ KIỂM CHỨNG 
```
- App ID và App Secret → Lấy App Token.
- App Token + Authorization_code → Đổi lấy Access Token <valid 2h>. (yêu cầu scope `offline_access`  -> nhận thêm Refresh Token <mã dài hạn hơn: nhưng vẫn có thể hết hạn hoặc bị thu hồi nếu người dùng thay đổi mật khẩu hoặc rút lại quyền truy cập đã cấp cho ứng dụng>
- App Token + Refresh Token -> để refresh Access Token khi hết hạn. 

```
Đúng như bạn đã hiểu về OAuth 2.0 với Lark:

1. **App ID và App Secret → Lấy App Token**:
    
    - Bạn sử dụng **App ID** và **App Secret** của ứng dụng để yêu cầu **App Token**. Đây là bước đầu tiên trong quy trình xác thực.
2. **App Token + Authorization Code → Đổi lấy Access Token**:
    
    - Sau khi người dùng đăng nhập và cấp quyền, ứng dụng của bạn sẽ nhận được một **Authorization Code**. Bạn sử dụng **App Token** và **Authorization Code** này để đổi lấy **Access Token**, có thời hạn sử dụng ngắn (thường là 2 giờ)​
        [OAuth 2.0 Simplified](https://www.oauth.com/oauth2-servers/server-side-apps/authorization-code/)
        [Okta Developer](https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type)
3. **App Token + Refresh Token → Làm mới Access Token**:
    
    - Khi **Access Token** hết hạn, bạn có thể sử dụng **Refresh Token** để lấy **Access Token** mới mà không cần người dùng phải xác thực lại. **Refresh Token** có thể tồn tại lâu hơn, nhưng vẫn có thể hết hạn hoặc bị thu hồi nếu người dùng thay đổi mật khẩu hoặc rút quyền truy cập của ứng dụng​
        [OAuth](https://oauth.net/2/grant-types/authorization-code/)
        [DEV Community](https://dev.to/risafj/beginner-s-guide-to-oauth-understanding-access-tokens-and-authorization-codes-2988)

### Lưu ý quan trọng:
- Bạn cần đảm bảo rằng ứng dụng yêu cầu **scope `offline_access`** để có thể nhận được **Refresh Token** khi người dùng đăng nhập lần đầu​
    [DEV Community](https://dev.to/risafj/beginner-s-guide-to-oauth-understanding-access-tokens-and-authorization-codes-2988)
Vậy, quy trình của bạn được kiểm chứng là đúng, và đây là cơ chế chuẩn của OAuth 2.0 khi làm việc với các API như Lark.


#### QUAY LẠI BÀI: LOG VÀO LARKBASE: 

Của em chắc đơn giản hơn. 
- Có mỗi conversation chat dạng JSON => log vào larkbase (thông qua: tenant_access_token) 
- tenant_access_token hết hạn thì xin lại (sử dụng app_id, app_secret)
- ```
```
cơ chế của lark nó nửa nửa Oauth
nửa nửa còn lại giống API key
tức là nó hết hạn
khi nào cần thì xin lại :v
cơ chế của lark nó nửa nửa Oauth
nửa nửa còn lại giống API key
tức là nó hết hạn
khi nào cần thì xin lại :v
đúng r, lark nó ở giữa thôi, cơ chế này strava nó làm triệt để
sau bạn có làm sẽ thấy
cơ chế Oauth2 làm mệt, nhưng dc cái bảo mật
còn api key thì đơn giản hơn, nhưng dễ gặp vấn đề hơn
```

- 


![[Pasted image 20241016114305.png]]

1. **app_access_token**: Đây là token ngắn hạn được cấp sau khi bạn sử dụng **App ID** và **App Secret** để xác thực với Lark API. Token này được sử dụng để gọi các API của Lark với quyền ứng dụng (không cần quyền người dùng).
    
2. **tenant_access_token**: Đây cũng là một loại token ngắn hạn, nhưng dành cho việc truy cập các tài nguyên trong phạm vi của tenant (công ty hoặc tổ chức). Token này dùng để xác thực các yêu cầu liên quan đến thông tin của tenant (ví dụ: truy cập thông tin doanh nghiệp, thông tin người dùng thuộc tổ chức).
    

### Vậy hai token này có giống nhau không?

- **Không hoàn toàn giống nhau**: Mặc dù cả hai đều là token để xác thực, nhưng chúng được dùng cho các mục đích khác nhau. **App Access Token** được dùng để gọi các API liên quan đến ứng dụng mà không cần quyền người dùng, còn **Tenant Access Token** được sử dụng khi bạn cần truy cập thông tin liên quan đến tổ chức hoặc tenant trong hệ thống của Lark.

--------------
Để chuyển chatbot Streamlit của bạn vào Lark, bạn có thể thực hiện theo các bước sau:

### 1. **Đăng ký tài khoản trên Lark Open Platform**:

- Truy cập [Lark Open Platform](https://open.larksuite.com) và đăng ký một tài khoản tổ chức nếu bạn chưa có. Sau đó, tạo một ứng dụng mới và bật tính năng bot cho ứng dụng này.

### 2. **Cấu hình bot trên Lark**:

- **Tạo một bot mới**: Trên Lark Open Platform, chọn mục **Bot** và tạo một bot mới. Điền các thông tin cần thiết như tên bot và hình đại diện.
- **Cấu hình URL cho bot**: Tại đây, bạn cần cung cấp **URL webhook** để Lark có thể giao tiếp với dịch vụ chatbot của bạn.

### 3. **Kết nối bot với dịch vụ Streamlit**:

- Hiện tại, chatbot của bạn đang chạy trên Streamlit tại URL: `https://cskh-stepupedu-chatbot-deploy2-aiteam.streamlit.app/`. Tuy nhiên, để tích hợp vào Lark, bạn sẽ cần tạo một **API endpoint** cho chatbot thay vì chỉ sử dụng giao diện Streamlit.
- Bạn có thể tạo một server API (ví dụ bằng Flask, FastAPI) để nhận các yêu cầu từ Lark và xử lý các sự kiện chat. Sau đó, cấu hình URL của API này vào phần "Callback URL" trong bot của Lark.

### 4. **Lập trình giao tiếp giữa Lark và chatbot**:

- Khi Lark gửi các sự kiện chat tới API của bạn, bạn cần xử lý chúng. Điều này có thể bao gồm việc xử lý các tin nhắn, trả lời tự động, và sử dụng mô hình chatbot đã có trong Streamlit để đưa ra phản hồi phù hợp.
- Đảm bảo rằng bot của bạn có khả năng xử lý các **webhook** từ Lark và gửi phản hồi lại thông qua API của Lark.

### 5. **Cấp quyền cho bot**:

- Trong mục quản lý bot trên Lark, bạn cần bật các quyền liên quan như: **Gửi và nhận tin nhắn**, **Quản lý cuộc trò chuyện nhóm** để bot có thể hoạt động trong các cuộc trò chuyện và nhóm.

### 6. **Kiểm tra và khởi chạy bot**:

- Sau khi hoàn tất việc cấu hình và tích hợp, bạn cần kiểm tra kỹ lưỡng hoạt động của bot trên Lark. Nếu mọi thứ hoạt động ổn định, bạn có thể khởi chạy bot để mọi người trong tổ chức sử dụng.

### 7. **Theo dõi và bảo trì**:

- Bạn có thể theo dõi log và các sự kiện tương tác trên Lark Open Platform để kiểm tra trạng thái hoạt động của bot và cập nhật nếu cần thiết.

Tóm lại, bạn sẽ cần thiết lập một API để giao tiếp giữa chatbot Streamlit và Lark, sau đó cấu hình bot trên Lark để nhận và xử lý tin nhắn thông qua API đó.

4o

##### You said:

URL webhook là cái gì vậy? -

###### ChatGPT said:

ChatGPT

**Webhook URL** là một đường dẫn (URL) mà một dịch vụ (như Lark) sử dụng để gửi dữ liệu hoặc thông báo tự động đến một ứng dụng khác (như chatbot của bạn). Webhook hoạt động như một **cầu nối** giữa hai ứng dụng, giúp chúng giao tiếp với nhau theo thời gian thực.

### Cách hoạt động:

- **Webhook** được cấu hình trong dịch vụ gửi dữ liệu (Lark, trong trường hợp này).
- Khi có sự kiện xảy ra (ví dụ: người dùng gửi tin nhắn cho bot trên Lark), Lark sẽ gửi một yêu cầu HTTP (thường là POST) đến URL webhook của bạn, cùng với dữ liệu về sự kiện đó (dạng JSON).
- Server hoặc ứng dụng của bạn nhận yêu cầu này tại URL webhook, xử lý nó (ví dụ, lấy tin nhắn, xử lý qua chatbot, và gửi phản hồi).

### Ví dụ:

1. Người dùng nhắn tin cho chatbot trên Lark.
2. Lark gửi yêu cầu HTTP POST đến webhook URL (ví dụ: `https://your-server.com/webhook`) kèm dữ liệu về tin nhắn.
3. Server của bạn xử lý thông tin, sau đó gửi phản hồi ngược lại cho Lark để chatbot trả lời người dùng.

Webhook rất hữu ích vì giúp bạn **xử lý sự kiện ngay lập tức** mà không cần ứng dụng của bạn phải liên tục yêu cầu (polling) dữ liệu từ Lark.

Nếu bạn muốn tích hợp chatbot của mình vào Lark, URL webhook sẽ là nơi Lark "gửi" các sự kiện đến để chatbot của bạn xử lý.

## 2.4 Lark AnyCross: [Build a chatbot via OpenAI connector - Documentation - Lark AnyCross (larksuite.com)](https://anycross-sg.larksuite.com/documentation/template/all/build-a-chatbot-via-open#Guide%20on%20using%20the%20template)

- https://botbuilder.larksuite.com/
![[Pasted image 20241019190008.png]]

[Build a chatbot via OpenAI connector - Documentation - Lark AnyCross (larksuite.com)](https://anycross-sg.larksuite.com/documentation/template/all/build-a-chatbot-via-open)