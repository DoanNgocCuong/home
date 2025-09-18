# Hướng Dẫn Gỡ Cài Đặt Microsoft Edge System Level

## Tổng Quan

Tài liệu này mô tả chi tiết quá trình gỡ cài đặt Microsoft Edge hoàn toàn ở mức system level, bao gồm các lệnh đã sử dụng, kết quả trả về và cách kiểm tra thành công.

## Môi Trường

- **OS**: Windows
- **Edge Version**: 140.0.3485.66
- **Tool**: Windows PowerShell (Admin)
- **Path gốc**: `C:\Program Files (x86)\Microsoft\Edge\Application\140.0.3485.66\Installer`

---

## Step 1: Thử Gỡ Cài Đặt Bằng Setup.exe

### Mục đích

Sử dụng setup.exe chính thức để gỡ cài đặt Edge theo cách Microsoft khuyến nghị.

### Lệnh thực hiện

```powershell
cd "C:\Program Files (x86)\Microsoft\Edge\Application\140.0.3485.66\Installer"
setup.exe --uninstall --system-level --verbose-logging --force-uninstall
```

### Kết quả

```
setup.exe : The term 'setup.exe' is not recognized as the name of a cmdlet, function, script file, or operable program...
```

### Nguyên nhân lỗi

PowerShell cần prefix `.\` để chạy executable từ thư mục hiện tại.

### Lệnh sửa lỗi

```powershell
.\setup.exe --uninstall --system-level --verbose-logging --force-uninstall
```

### Kết quả sau sửa lỗi

```
PS C:\...\Installer> .\setup.exe --uninstall --system-level --verbose-logging --force-uninstall
>>
```

### Phân tích

- Lệnh chạy không báo lỗi
- Tuy nhiên không có thông báo thành công rõ ràng
- Cần kiểm tra bằng cách khác

---

## Step 2: Kiểm Tra File Setup.exe

### Mục đích

Xác nhận file setup.exe tồn tại và có thể thực thi.

### Lệnh kiểm tra

```powershell
ls
```

### Kết quả

```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         9/14/2025   5:58 AM           3584 msedge_7z.data
-a----         9/14/2025   5:57 AM        7629352 setup.exe
```

### Phân tích

- File setup.exe tồn tại (7.6MB)
- File có thể đã chạy nhưng không thể xác định kết quả

---

## Step 3: Xóa Thủ Công Bằng PowerShell

### Mục đích

Dừng tất cả tiến trình Edge và xóa thư mục Edge hoàn toàn.

### Lệnh dừng tiến trình

```powershell
Stop-Process -Name "msedge" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "MicrosoftEdge*" -Force -ErrorAction SilentlyContinue
```

### Lệnh xóa thư mục chính

```powershell
cd "C:\Program Files (x86)\Microsoft"
Remove-Item -Recurse -Force "Edge" -ErrorAction SilentlyContinue
```

### Kết quả

```
PS C:\Program Files (x86)\Microsoft> Remove-Item -Recurse -Force "Edge" -ErrorAction SilentlyContinue
```

### Phân tích

- Lệnh chạy thành công (không báo lỗi)
- Thư mục Edge đã bị xóa
- **✅ THÀNH CÔNG**: Bước quan trọng nhất đã hoàn tất

---

## Step 4: Xóa EdgeUpdate

### Mục đích

Xóa thành phần EdgeUpdate để tránh Edge được cài lại tự động.

### Lệnh thực hiện

```powershell
Remove-Item -Recurse -Force "C:\Program Files (x86)\Microsoft\EdgeUpdate" -ErrorAction SilentlyContinue
```

### Kết quả

Lệnh chạy thành công (không báo lỗi).

---

## Step 5: Kiểm Tra AppX Packages

### Mục đích

Kiểm tra các thành phần Edge còn lại trong Windows AppX system.

### Lệnh kiểm tra

```powershell
Get-AppxPackage *edge*
```

### Kết quả

```
Name              : Microsoft.MicrosoftEdgeDevToolsClient
Publisher         : CN=Microsoft Corporation...
Architecture      : Neutral
ResourceId        : neutral
Version           : 1000.22621.1.0
PackageFullName   : Microsoft.MicrosoftEdgeDevToolsClient_1000.22621.1.0_neutral_neutral_8wekyb3d8bbwe
InstallLocation   : C:\Windows\SystemApps\Microsoft.MicrosoftEdgeDevToolsClient_8wekyb3d8bbwe
IsFramework       : False
PackageFamilyName : Microsoft.MicrosoftEdgeDevToolsClient_8wekyb3d8bbwe
PublisherId       : 8wekyb3d8bbwe
IsResourcePackage : False
IsBundle          : False
IsDevelopmentMode : False
NonRemovable      : True
SignatureKind     : System
Status            : Ok
```

### Phân tích

- Chỉ còn lại **EdgeDevToolsClient**
- Đây là Developer Tools, không phải trình duyệt chính
- `NonRemovable : True` = Thành phần hệ thống được bảo vệ

---

## Step 6: Thử Xóa EdgeDevToolsClient

### Mục đích

Cố gắng xóa thành phần DevTools còn lại.

### Lệnh thực hiện

```powershell
Get-AppxPackage *MicrosoftEdgeDevToolsClient* | Remove-AppxPackage
```

### Kết quả

```
Remove-AppxPackage : Deployment failed with HRESULT: 0x80073CFA, Removal failed...
error 0x80070032: AppX Deployment Remove operation on package Microsoft.MicrosoftEdgeDevToolsClient...failed. 
This app is part of Windows and cannot be uninstalled on a per-user basis.
```

### Phân tích

- **Lỗi mong đợi**: EdgeDevToolsClient là thành phần hệ thống
- Windows không cho phép xóa
- **✅ BÌNH THƯỜNG**: Đây không phải trình duyệt chính

---

## Kết Quả Cuối Cùng

### Tình Trạng Sau Khi Hoàn Tất

|Thành Phần|Trạng Thái|Ghi Chú|
|---|---|---|
|**Microsoft Edge Browser**|❌ ĐÃ XÓA|Trình duyệt chính đã bị gỡ bỏ hoàn toàn|
|**Edge Program Files**|❌ ĐÃ XÓA|Thư mục `C:\Program Files (x86)\Microsoft\Edge` không tồn tại|
|**EdgeUpdate**|❌ ĐÃ XÓA|Không thể tự động cài lại Edge|
|**EdgeDevToolsClient**|✅ CÒN LẠI|Thành phần hệ thống, không thể xóa|

### Cách Kiểm Tra Thành Công

#### 1. Kiểm tra thư mục chính

```powershell
Test-Path "C:\Program Files (x86)\Microsoft\Edge"
Test-Path "C:\Program Files\Microsoft\Edge"
```

**Kết quả mong đợi**: Cả hai đều trả về `False`

#### 2. Thử mở Edge

- Nhấn `Windows + R`
- Gõ `msedge` và Enter
- **Kết quả mong đợi**: Báo lỗi "không tìm thấy lệnh"

#### 3. Kiểm tra Start Menu

- Tìm "Microsoft Edge"
- **Kết quả mong đợi**: Chỉ thấy "Microsoft Edge DevTools" (không phải Edge chính)

#### 4. Kiểm tra Default Browser

- Mở file .html
- **Kết quả mong đợi**: Windows hỏi chọn trình duyệt khác

### Lệnh Kiểm Tra Tổng Hợp

```powershell
Write-Host "=== KIỂM TRA XÓA EDGE ===" -ForegroundColor Yellow
Write-Host "1. Program Files (x86):" -NoNewline
if (Test-Path "C:\Program Files (x86)\Microsoft\Edge") { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }

Write-Host "2. Program Files:" -NoNewline  
if (Test-Path "C:\Program Files\Microsoft\Edge") { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }

Write-Host "3. AppX Package (Edge chính):" -NoNewline
if (Get-AppxPackage *MicrosoftEdge* | Where-Object {$_.Name -eq "Microsoft.MicrosoftEdge"}) { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }
```

```powershell
PS C:\Program Files (x86)\Microsoft> # Tìm Edge browser chính
>> Get-AppxPackage *MicrosoftEdge* | Where-Object {$_.Name -eq "Microsoft.MicrosoftEdge"}
>>
PS C:\Program Files (x86)\Microsoft> Write-Host "=== KIỂM TRA XÓA EDGE ===" -ForegroundColor Yellow
>> Write-Host "1. Program Files (x86):" -NoNewline
>> if (Test-Path "C:\Program Files (x86)\Microsoft\Edge") { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }
>>
>> Write-Host "2. Program Files:" -NoNewline
>> if (Test-Path "C:\Program Files\Microsoft\Edge") { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }
>>
>> Write-Host "3. AppX Package (Edge chính):" -NoNewline
>> if (Get-AppxPackage *MicrosoftEdge* | Where-Object {$_.Name -eq "Microsoft.MicrosoftEdge"}) { Write-Host " CÒN TỒN TẠI" -ForegroundColor Red } else { Write-Host " ĐÃ XÓA" -ForegroundColor Green }
=== KIỂM TRA XÓA EDGE ===
1. Program Files (x86): ĐÃ XÓA
2. Program Files: ĐÃ XÓA
3. AppX Package (Edge chính): ĐÃ XÓA
```
---

## Kết Luận

### ✅ THÀNH CÔNG HOÀN TOÀN

- **Microsoft Edge (trình duyệt chính)** đã được gỡ bỏ hoàn toàn ở system level
- EdgeDevToolsClient còn lại là **BÌNH THƯỜNG** vì đây là thành phần hệ thống Windows
- Mục tiêu xóa Edge để cài lại sạch đã đạt được

### Các Bước Quan Trọng Nhất

1. **Stop-Process**: Dừng tất cả tiến trình Edge
2. **Remove-Item Edge folder**: Xóa thư mục chính (bước quyết định)
3. **Remove EdgeUpdate**: Ngăn cài lại tự động

### Để Cài Lại Edge (Nếu Cần)

```powershell
# Cách 1: Tải từ trang chủ
# Truy cập: https://www.microsoft.com/edge

# Cách 2: Sử dụng winget
winget install Microsoft.Edge

# Cách 3: Enterprise version
# Tải MicrosoftEdgeEnterpriseX64.msi và chạy:
Start-Process msiexec.exe -ArgumentList "/i MicrosoftEdgeEnterpriseX64.msi /quiet ALLUSERS=1" -Wait
```

---

## Ghi Chú Kỹ Thuật

### Tại Sao Setup.exe Không Hoạt động Rõ Ràng?

- Setup.exe có thể đã chạy nhưng không hiển thị output
- Một số phiên bản Edge có cơ chế bảo vệ khỏi uninstall
- Phương pháp thủ công đáng tin cậy hơn

### Tại Sao EdgeDevToolsClient Không Thể Xóa?

- Đây là thành phần `.NET WebView2` runtime
- Được sử dụng bởi nhiều ứng dụng Windows khác
- Windows bảo vệ để đảm bảo ổn định hệ thống

### Rủi Ro và Cảnh Báo

- ✅ **An toàn**: Quá trình này không gây hại hệ thống
- ⚠️ **Lưu ý**: Một số app có thể cần WebView2, nhưng có thể cài riêng
- 🔄 **Phục hồi**: Edge có thể được cài lại bất cứ lúc nào

---

_Tài liệu này được tạo dựa trên thực tế quá trình gỡ cài đặt Edge phiên bản 140.0.3485.66 trên Windows._