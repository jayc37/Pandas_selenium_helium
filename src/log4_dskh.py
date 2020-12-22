from imp import *
def log_4_dlkh(status,sokhung):
        """
    Ý tưởng: 
            Ghi vào cuối mỗi dòng trạng thái tùy ý: nếu that bai  = 0, ngươc lại = 1.
    """
        try:
            #get date
            date_n = datetime.now()
            date_n = date_n.strftime("%Y-%m-%d %H:%M:%S")
            sdate = date_n
            #get file cskh
            wk = load_workbook('mauthongtinkh.xlsx')
            wh = wk.active
            for row in wh['F']:
                if row.value == sokhung:
                    if status == 'thanh cong':
                        wh['K{}'.format(row.row)] = 1
                    else:
                        wh['K{}'.format(row.row)] = 0
                    wh['L{}'.format(row.row)] = sdate
                    break
            wk.save('mauthongtinkh.xlsx')
            wk.close()
        except Exception as e:
            print('write_log_excels :' + str(e))

def save_to_excels():
    """ Ý tưởng là xuất file excel từ file .txt"""
    import pandas as pd
    #get date
    date_n = datetime.now()
    date_n = date_n.strftime
    ("%Y-%m-%d %H:%M:%S")
    sdate = date_n
    excel = "log\\log_thatbai.txt"
    df = pd.read_csv(excel, sep=',')
    df.to_excel('DS_SDV_SDT_{}.xlsx'
    .format(str(sdate))
    , index=("SDV","SDT"),)