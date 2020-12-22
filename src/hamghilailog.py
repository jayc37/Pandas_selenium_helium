from datetime import datetime,timedelta
import threading
from threading import Thread
def write_log_thanhcong(sdv,sdt):
    """Hàm này ghi lại log số đúng"""

    with open('log\\log_thanhcong','a') as f:
        f.write(sdv+","+str(sdt)+'\n')
    f.close()

def write_log_thatbai(sdv,sdt):
    """Hàm này ghi lại log số sai"""

    with open('log\\log_thatbai','a') as f:
        f.write(sdv+","+str(sdt)+'\n')
    f.close()

def rowfalse(sdv,sdt):
    """Hàm này ghi lại log số sai"""
    t = threading.Thread(target=write_log_thatbai,args =(sdv,sdt))
    t.start()
    date_n = datetime.now()
    date_n = date_n.strftime("%Y-%m-%d %H:%M:%S")
    sdate = date_n
    line = "su dung {} thay doi so dien thoai that bai".format(sdv)
    print(line)

def rowtrue(sdv,sdt):
    """Hàm này ghi lại log số đúng"""
    t = threading.Thread(target=write_log_thanhcong,args =(sdv,sdt))
    t.start()
    date_n = datetime.now()
    date_n = date_n.strftime("%Y-%m-%d %H:%M:%S")
    sdate = date_n
    line = "su dung {} thay doi so dien thoai thanh cong".format(sdv)
    print(line)

def sdvsai(sr,sodienthoai):
    t = threading.Thread(target=ghisai,args =(sr,sodienthoai))
    t.start()
    date_n = datetime.now()
    date_n = date_n.strftime("%Y-%m-%d %H:%M:%S")
    sdate = date_n
    line = "So dich vu {} co the bi sai".format(sr)
    print(line)

def ghisai(sr,sodienthoai):
    """
    Ý tưởng: Ghi số diện thoại vào bên cạnh số dịch vụ bi sai
    """    
    try:
        with open('log\\DSSODV_SAI','a') as f:
            f.write(sr+","+str(sodienthoai)+'\n')
        f.close()
    except Exception as e:
        print(str(e))
