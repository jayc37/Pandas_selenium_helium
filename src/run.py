#! coding: utf-8
from imp import *
from getfile import read_excel,list_userlist,read_excel2
from helium import *
import threading
from hamghilailog import write_log_thatbai
def sleeping(min_s, max_s):
    sleep(randint(min_s, max_s))

class pushdata:
    def __init__(self,op):
        self.username = '' 
        self.password = ''
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)
        self.sokhung = ''
        self.op = op
        self.file_name = '' 
        self.point = 0
        self.data_from_excel_file = None
        self.err_list = []
        self.log_list = []
        self.sodichvu = ''
        self.islogin = False
        self.is_manhinh_ycdv = False
        self.is_manhinh_kh1 = False
        self.readpd = None
        self.click_ho = False
        self.press_enter_pass = False
        self.sodichvusai = False
    def login(self):
            sleeping(1,1)
            t = Timer(60, self.force_timeout)
            t.start()
            """ 
            This function: LOGIN IN TO PAGE,
            with handle 3 element: 
             """
            UURL = ""
            # self.URL = UURL
            self.driver.get(UURL)
            self.driver.refresh()
            self.driver.maximize_window()
            try:
                # actions = ActionChains(self.driver)
                status_id,username_ele = self.waiting_by_name("SWEUserName")
                status_btn,login_ele = self.waiting_by_Xpath(".//*[@id='s_swepi_22']")
                status_pw,password_ele = self.waiting_by_name("SWEPassword")
                if status_id == status_pw == status_btn == True:
                    username_ele.send_keys(self.username)
                    password_ele.send_keys(self.password)
                    sleeping(1,1)
                    login_ele.click()
                    self.is_login(True)
                else:
                    self.is_login(False)
                # sleeping(3,4) #--
            except Exception as e:
                print('LOGIN FAIL Because: ' + str(e))
                print("--" * 30)
                print('LOGIN AGAIN')
                t.cancel()
                self.force_timeout()
            t.cancel()

    def write_log_error(self,message):
        """
            File log error
        """
        with open('log\\logfile_error', 'a',encoding="utf-8") as f:
            da = datetime.now()
            da = da.strftime("%d/%m/%Y %H:%M:%S")
            f.write('[' + str(da)+'] <------> {' + str(message) + ' }')
            f.write('<' + '--' * 100 + '>')
        f.close()

    def get_object(self):
        """ B1. Kiểm tra login và Lấy mảng dữ liệu được truyền vào và chạy dòng for
            B2. Kiểm tra vị trí can_start_new_soycdv và bắt đầu biến mới.
            B3. Khai báo các biến cần thiết và bắt đầu di chuyển bằng hàm 'send_values_so_dich_vu'
        """
        try:
            dat_ex = self.data_from_excel_file
            for i in range(len(dat_ex)):
                try:
                    dx =  dat_ex[i]
                    l = len(dx)
                    self.log_list = dx
                    sodichvu = str(dx[0])
                    self.sodichvu = sodichvu
                    sodienthoai = str(dx[1])
                    sodienthoai_dakiemtra =  self.kiemtrasr(sodienthoai)
                    ###################################################
                    al = self.alert()
                    if al:
                        self.force_timeout()
                    if self.point == 3:
                        self.force_timeout()
                    if self.islogin:
                        self.fyeucaudichvu()
                        if self.is_manhinh_ycdv:
                            sleeping(1,1)
                            #---------------------------------------------------------#
                            t = Timer(180,self.force_timeout)
                            t.start()
                            self.send_values_so_dich_vu(sodichvu,sodienthoai_dakiemtra)
                            t.cancel()
                            #---------------------------------------------------------#
                        else:
                            rowfalse(sodichvu,sodienthoai_dakiemtra)
                            self.force_timeout()
                            pass
                    else:
                        rowfalse(sodichvu,sodienthoai_dakiemtra)
                        self.force_timeout()
                        pass
                except Exception as e:
                    print(str(e))
                    t.cancel()
                    self.force_timeout()
                    pass
                    ###################################################
        except Exception as e:
            print(str(e))
            pass

    def kiemtrasr(self,sodienthoai):
        _c = re.search(r'^[0]((([0-9]{9})\b)|(([0-9]{10})\b))$',str(sodienthoai))
        if _c:
            return sodienthoai
        else:
            lsdt =  len([i for i in range(len(str(sodienthoai)))])
            t = 10 - lsdt
            sodienthoai = str(("0" * t))+ str(sodienthoai)
            return sodienthoai
    
    def send_values_so_dich_vu(self,sodichvu,sodienthoai):
        """ CHANGE_SDT BẰNG SỐ DỊCH VỤ"""
        try:
            status_form,form_sodichvu = self.waiting_by_name("s_6_1_14_0")
            if status_form:
                form_sodichvu.send_keys(sodichvu)
                self.fmanhinhkhachhang1()
                if self.is_manhinh_kh1:
                    self.fmanhinhkhachhang2()
                    if self.is_manhinh_kh2:
                        try:
                            _,sdt = self.waiting_by_name("s_2_1_89_0")
                            sdt.click()
                            sleeping(1,1)
                            press(END)
                            press(BACK_SPACE *11)
                            sleeping(1,1)
                            sdt.send_keys(sodienthoai)
                            sleeping(1,1)
                            press(CONTROL +'s')
                            rowtrue(sodichvu,sodienthoai)
                            self.point = 0
                        except Exception as e:
                            print(str(e))
                            rowfalse(sodichvu,sodienthoai)
                            pass
                    else:
                        self.is_manhinh_kh2 = False
                        sdvsai(sodichvu,sodienthoai)
                        # self.point += 1
                else:
                    rowfalse(sodichvu,sodienthoai)
                    self.point += 1
                    self.is_manhinh_kh1 = False
            else:
                self.is_manhinh_ycdv = False
                rowfalse(sodichvu,sodienthoai)
                self.point += 1
                sleeping(2,2)
        except Exception as e:
            rowfalse(sodichvu,sodienthoai)
            self.point += 1
            pass

    def fyeucaudichvu(self):
        """
            Hàm này gọi 2 hàm để đi đến màn hình yêu cầu dịch vụ
        """
        self.manhinh_ycdv() # di chuyển
        self.f_is_manhinh_ycdv() # kiểm tra

    def manhinh_ycdv(self):
        """
            Di chuyển đến "màn hình yêu cầu dịch vụ" thông qua việc "bấm nút yêu cầu dịch vụ"
        """
        try:
            # status_ycdv,ycdv = self.waiting_by_text("Yêu cầu dịch vụ")
            set_driver(self.driver)
            wait_until(Text("Yêu cầu dịch vụ").exists)
            if (Text("Yêu cầu dịch vụ").exists):
                sleeping(1,1)
                # t1 = Timer(15,self.force_timeout)
                # t1.start()
                click(Text("Yêu cầu dịch vụ"))
                # t1.cancel()
            else:
                sleeping(2,2)
                wait_until(Text("Yêu cầu dịch vụ").exists)
                sleeping(1,1)
                click(Text("Yêu cầu dịch vụ"))
        except Exception as e:
             # không thể bấm vào nút yêu cầu dịch vụ hoặc di chuyển đến màn hình yêu cầu dịch vụ
            pass
           
    def fmanhinhkhachhang1(self):
        """
        Hàm này di chuyển màn hình khách hàng 1 và kiểm tra xem đã ở màn hình 1 hay chưa
        """

        self.send_key_enter()
        if self.press_enter_pass:
            self.manhinh_kh1()
        else:
            self.is_manhinh_kh1 = False
    def fmanhinhkhachhang2(self):
        """
        Hàm này di chuyển màn hình khách hàng 2 và kiểm tra xem đã ở màn hình 1 hay chưa
        """
        self.click_ho_khachhang()
        if self.click_ho:
            self.manhinh_kh2()
        else:
            self.is_manhinh_kh2 = False
                
    def f_is_manhinh_ycdv(self):
        set_driver(self.driver)
        """ Biến is_manhinh_ycdv = True nếu đang ở màn hình yêu cầu dịch vu"""
        wait_until(Text("Số yêu cầu dịch vụ:").exists)
        status_form,form_sodichvu = self.waiting_by_name("s_6_1_14_0")
        if Text("Số yêu cầu dịch vụ:").exists or status_form:
            self.is_manhinh_ycdv = True
        else:
            self.is_manhinh_ycdv = False

    def fid(self,elm):
            return self.driver.find_element_by_id(elm)
    def fna(self,elm):
            return self.driver.find_element_by_name(elm)
    
    def fxp(self,elm):
            return self.driver.find_element_by_xpath(elm)
    
    def alert(self):
        """ Ý tưởng: tìm kiếm xem khi nhập liệu khung alert có bị hiện lên hay không."""
        try:
            alert = self.driver.switch_to_alert()
            print("found alert !!")
            self.force_timeout()
            return True
        except:
            return False
    def waiting_by_id(self,element):
        try:
            myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, element)))
            return True,myElem
        except TimeoutException:
            return False,"None"
    def waiting_by_name(self,element):
        try:
            myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, element)))
            return True,myElem
        except TimeoutException:
            return False,"None"

    def waiting_by_Xpath(self,element):
        try:
            myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element)))
            return True,myElem
        except TimeoutException as e:
            print(str(e))
            return False,"None"
    def waiting_DOM(self):
        driver = self.driver
        driver.implicitly_wait(15)
        return True

    def force_timeout(self):
        try:
            self.point = 0
            set_driver(self.driver)
            kill_browser()
            # os.system('taskkill /im chrome.exe /f /t') #kill chrome
            self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.op) #create new chrome
            self.driver.delete_all_cookies()
            self.login()
            pass
        except:
            print("Reset chrome failed")
            print("Close Progam !!")
            pass 
    
    def is_login(self,status):
            if status:
                self.islogin = True
            else:
                self.islogin = False

    def send_key_enter(self):
        try:
            set_driver(self.driver)
            sleeping(2,2)
            t1 = Timer(20, self.force_timeout)
            t1.start()
            press(ENTER)
            t1.cancel()
            self.press_enter_pass = True
        except Exception as e:
            #Ghi lai log may bi dung
            self.press_enter_pass = False
            pass
    def click_ho_khachhang(self):
        status_ho,ho = self.waiting_by_Xpath('//*[@id="1_s_2_l_Contact_Last_Name"]/a')
        try:
            sleeping(2,2)
            t2 = Timer(20, self.force_timeout)
            t2.start()
            ho.click()
            t2.cancel()
            self.click_ho = True
        except Exception as e:
            #Ghi lai log may bi dung
            self.click_ho = False
            pass

    def manhinh_kh1(self):
        """
            Khi thực thi sẽ di chuyển đến màn hình khách hàng 1
        """
        try:
            wait_until(Text("Họ khách hàng").exists)
            status_ho,ho = self.waiting_by_Xpath('//*[@id="1_s_2_l_Contact_Last_Name"]/a')
            if (Text("Họ khách hàng").exists) and status_ho == True:
                self.is_manhinh_kh1 = True
            else:
                self.is_manhinh_kh1 = False
        except Exception as e:
            self.is_manhinh_kh1 = False

    def manhinh_kh2(self):
        """
            Khi thực thi sẽ di chuyển đến màn hình khách hàng 2
        """
        try:
            status_record,record = self.waiting_by_id("s_1_1_13_0_Ctrl")
            if status_record:
                press(ARROW_UP*7)
                status_plus,plus = self.waiting_by_id("s_2_1_68_0_Ctrl")
                if status_plus == False:
                    press(ARROW_UP*6)
                status_sdt,sdt = self.waiting_by_name("s_2_1_89_0")
                if status_sdt:
                    sleeping(1,1)
                    sdt.click()
                    self.is_manhinh_kh2 = True
                else:
                    self.is_manhinh_kh2 = False
            else:
                self.is_manhinh_kh2 = False
        except Exception as e :
            self.is_manhinh_kh2 = False
            pass

 
# def Pro(data,file,username,pasword):
#             p = Process(target=pushda.getacount,args =(data,file,username,pasword,)).run()
#             p.close()
    def reStart(self,_):
        print("Chuan bi chay lai cac dong that bai lan thu {}".format(_))
        self.data_from_excel_file.clear()
        data = read_log_thatbai()
        if len(data) != 0:
            self.point = 0
            self.data_from_excel_file = data
            self.get_object()
            self.reStart(_ + 1)
        else:
            print("CHUONG TRINH KET THUC O LAN CHAY LAI THU {}".format(_))

    def getacount(self,data_from_excel,file_name,usr,pwd):
        """
            data_from-excel: Dist data get from file_excel_here\\filename.xlsx
            file_name: using for write log.
            usr,pwd: account for login.
            bool iw: check on "change/write" mode
        """
        try:
            self.file_name = file_name
            self.data_from_excel_file = data_from_excel
            self.username = usr
            self.password = pwd
            self.login()
            self.point = 0
            self.get_object()
            self.reStart(1)
            print('FINISH')
        except Exception as e:
            message = "Loi ham getacount : " + str(e)
            print(message)
            # self.write_log_error(message)


if __name__ == '__main__':
    plan = input('su dung mat khau cu type "1":')
    pasword = ''
    if plan == "1":
        pasword = ""
    else:
        pasword = input('Nhập password:')
    op = webdriver.ChromeOptions()
    op.add_argument("--disable-gpu")
    op.add_argument('start-maximized')
    op.add_argument("--disable-extensions")
    op.add_argument("enable-automation")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-infobars")
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument("--disable-browser-side-navigation")
    op.add_experimental_option("excludeSwitches", ["enable-logging"])
    sr_ch = []
    # Tìm kiếm các file excel trong folder file_excel_here
    for root, dirs, files in os.walk("file_excel_here"):
        for file in files:
                if file.endswith(".xlsx") and '~' not in file: #tìm ra file excel
                    x = re.search(r'SR_',file) #so khớp
                    if x:
                        x = (x.string).replace("SR_",'')
                        username = x.replace(".xlsx",'')
                    file_name = os.path.join(root, file)
                    _sr = {}
                    wb = read_excel2(file_name)
                    _sr["username"] = username
                    _sr["data"] = wb
                    sr_ch.append(_sr)
    for i in range(len(sr_ch)):
        _c = sr_ch[i]
        username = _c["username"]
        data = _c["data"]
        pushda = pushdata(op)
        try:
            # t = threading.Thread(target=pushda.getacount,args =(data,file,username,pasword,)).start()
            pushda.getacount(data,file,username,pasword)
        except Exception as e:
            print(str(e))
            pass
    
    # pushda.driver.close()
