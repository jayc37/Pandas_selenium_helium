## Ứng dụng này được xây dựng phục vụ cho việc nhập liệu số điện thoại lên trang HMS thông qua mã dịch vụ(code service).
# Ý tưởng: 
- Sử dụng thư viện selenium và henium kết hợp với ngôn ngữ python xây dựng bot tự động click đến các phần tử của trang https://hms.honda.com.vn/ sau đó thay đổi số điện thoại theo mã dịch vụ.
- Input: File excels chứa các dòng thông tin, mã dịch vụ và số điện thoại của các cửa hàng.
- Output: Các số điện thoại được thay đổi trực tiếp trên trang https://hms.honda.com.vn/ thông qua các bước:
+ Đăng nhập: Điền vào account tại các cửa hàng để đăng nhập lên trang hms.
+ Di chuyển: Bấm vào phần tử Yêu cầu dịch vụ -> Bấm vào textfield và điền vào Số yêu cầu dịch vụ -> Enter -> Chuyển đến màn hình thông tin khách hàng -> bấm vào họ của khách hàng -> Chuyển đến màn hình chi tiết thông tin khách hàng -> Kéo chuột lên trên --> bấm vào ô số điện thoại + xóa + điền vào số điện thoại mới.
+ Ghi log thành công: Ghi log vào file log_thanhcong nếu dòng thành công
+ Ghi log thất bại: Ghi log vào file log_thatbai nếu dòng bị phát sinh ảnh hưởng do các trường hợp như trang web bị treo..
+ Ghi log dòng sai:  Ghi log vào file DSSODV_SAI nếu mã dịch vụ không vào được trang chi tiết thông tin khách hàng.
## Developer ##:

# Input:
+ Dữ liệu từ file excels: Sử dụng thư viện pandas, lấy ra dữ liệu các dòng trong file excel lưu trữ bằng mảng.
+ Account: username lấy ra từ tên file excels trong thư mục file_excel_here, mật khẩu được nhập từ màn hình command promt.
# Đăng nhập:
+ B1: Sử dụng webdriver của selenium khởi tạo 1 trình duyệt trắng và truy cập đến trang https://hms.honda.com.vn/
+ B2: Tìm đến 3 phần tử, textField username,pasword, button login. Kiểm tra xem nếu tồn tại bắt đầu đăng nhập. nếu không tồn tại quay lại được B1.
+ B3: Thay đổi trạng thái islogin = True để dể kiểm soát.

## Thư viện
 - 
 - Selenium: Thư viện chính xây dựng nên project. https://selenium-python.readthedocs.io/
 - helium: Thư viện rút gọn của selenium. https://selenium-python-helium.readthedocs.io/en/latest/
 - Pandas: thư viện xử lý dữ liệu đầu vào.
 - openpyxl: Thư viện kết hợp cùng pandas xử lý file excels đầu vào.
 - bs4,Beautifulsoup: Thư viện dùng để crawler dữ liệu.
# Màn hình Yêu cầu dịch vụ:
# Bước 0: bấm vào Node "yêu cầu dịch vụ"
+ B1: Sử dụng helium kiểm tra xem có tồn tại phần tử TextField "Số yêu cầu dịch vụ" hay không, nếu có trạng thái ismanhinh_ycdv = True, Nếu không ismanhinh_ycdv = False và quay lại bước 0
+ B2: Nếu ismanhinh_ycdv = True, truyền vào số dịch vụ và gửi đi Keys ENTER, nếu không quay lại B1.
# Màn hình Thông tin khách hàng:
+ B1: Kiểm tra phần tử họ khách hàng và textField họ khách hàng có tồn tại hay không, nếu có trạng thái is_manhinh_thongtinkhachang = True, ngược lại is_manhinh_thongtinkhachang = False, quay lại bước 0.
+ B2: Nếu trạng thái is_manhinh_thongtinkhachang = True, click vào ô họ khách hàng để chuyển đến màn hình ## Chi tiết thông tin khách hàng ##
# Màn hình Chi tiết thông tin khách hàng
B1: Kiểm tra xem có ở màn hình này hay không bằng cách kiểm tra các trường thông tin trong màn hình này bao gồm: nút new bên dưới(NEW1) và nút new bên trên(NEW2).
 - (dk1)Nếu tồn tại nút NEW1 , gửi đi nút ARROW UP 6 lần để di chuyển lên khung bên trên.
 - (dk2)Nếu tìm thấy nút NEW2. Tìm TextField sodienthoai.
 - Đáp ứng các điều kiện trên trạng thái is_manhinh_chitiet_thongtinkhachhang = True
 - Ngược lại is_manhinh_chitiet_thongtinkhachhang = True quay lại bước 0.
 B2:
 -  is_manhinh_chitiet_thongtinkhachhang = True và gửi được sodienthoai, đánh dấu thành công.
 - Nếu is_manhinh_chitiet_thongtinkhachhang = True nhưng không gửi được sodienthoai, đánh dấu đây là mã dịch vụ sai.
 # Ghi log:
+ Ghi log thành công: Ghi log vào file log_thanhcong nếu dòng thành công
+ Ghi log thất bại: Ghi log vào file log_thatbai nếu dòng bị phát sinh ảnh hưởng do các trường hợp như trang web bị treo..
+ Ghi log dòng sai:  Ghi log vào file DSSODV_SAI nếu mã dịch vụ không vào được trang chi tiết thông tin khách hàng.

# Lỗi nghiêm trọng:
- Lỗi trang web đang chạy bị treo: khởi động lại trình duyệt mới bằng cách đặt 1 đồng hồ đếm trước khi chạy từ Bước 0.
- Lỗi trang web đang chạy bị treo và ứng dụng bên dưới vẫn chạy bình thường nhưng log liên tục ra file thatbai: Đặt điểm point + 1 nếu rơi vào trạng thái này. Nếu point = 3 sẽ khởi động lại trình duyệt mới.
# Khắc phục lỗi các dòng rơi vào file log_thatbai:
- Chuyển thành file excels sau đó khởi động chạy lại chương trình từ Bước 0.