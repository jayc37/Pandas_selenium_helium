from imp import *

def log_4_pt(status,sokhung,listretried,filename):
    """
    Ý tưởng: 
    1. Ghi vào cuối file pt.xlsx dòng dữ liệu có status =='that bai'.
    2. Ghi vào cuối mỗi dòng trạng thái tùy ý: nếu that bai  = 0, ngươc lại = 1.
    """
    try:
        #get date
        log_list = listretried
        date_n = datetime.now()
        date_n = date_n.strftime("%Y-%m-%d %H:%M:%S")
        sdate = date_n
        #get file path
        fname = filename
        wk = load_workbook(fname)
        wh = wk.active
        lenth = wh.max_row
        pl = log_list
        if pl is not None and status == 'that bai': 
            # w = len(all row)
            w = lenth + 1
            wh['A{}'.format(w)] =  pl[0]
            wh['B{}'.format(w)] =  pl[1]
            wh['C{}'.format(w)] =  pl[2]
            wh['D{}'.format(w)] =  pl[3]
            wh['E{}'.format(w)] = 'retry'

        for row in wh['A']:
            # tìm ra dòng hiện tại bằng số khung để từ đó ghi vào cuối dòng trạng thái của nó.
            if row.value == sokhung:
                if status == 'thanh cong':
                    wh['E{}'.format(row.row)] = 1
                elif status =='that bai':
                    wh['E{}'.format(row.row)] = 0
                wh['F{}'.format(row.row)] = sdate
                break
        log_list.clear()
        wk.save(filename)
        wk.close()
    except Exception as e:
        print('write_log_excels :' + str(e))
