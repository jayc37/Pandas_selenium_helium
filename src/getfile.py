import pandas as pd

def read_excel(filename):
    try:
        dr = pd.read_excel(filename, index_col=0,header= 2)
        datalist = {}
        
        for i in range(len(dr.values)):
            datal = []
            datal.append([x for x in dr.values[i]])
            datalist[datal[0][4]] = datal[0]
        return datalist
    except Exception as e:
        print(str(e))
def read_excel2(filename):
    try:
        dr = pd.read_excel(filename, index_col=None,header= 0)
        datalist = []
        for i in dr.values:
            datalist.append([x for x in i])
        return datalist
    except Exception as e:
        print(str(e))

def save_to_excels():
    """ Ý tưởng là xuất file excel từ file .txt"""
    #get date
    from datetime import datetime,timedelta
    date_n = datetime.now()
    date_n = date_n.strftime
    ("%Y_%m_%d")
    sdate = date_n
    excel = "log\\DSSODV_SAI"
    df = pd.read_csv(excel, sep=',')
    df.to_excel(r'log\\DSSODV_SAI.xlsx'
    , index=("SDV","SDT"),)


def read_log_thatbai():
    """Hàm này lấy ra số log thất bại"""
    with open('log\\log_thatbai','r+') as f:
        t = f.readlines()
        newlist = []
        for i in t:
            newlist.append(i.replace("\n",'').split(','))
        f.truncate(0)
    f.close()
    return newlist
def list_userlist(username):
    l = []
    if username in l:
       return True
    else:
        return False
        
