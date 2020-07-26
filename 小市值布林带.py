import datetime
from jqdata import * 

def filter_st_stock(stocks):
    stocks = [
        stock for stock in stocks
        if str(get_security_info(stock).display_name).find('ST') == -1 
    ]
    return stocks


check_out_lists = get_index_stocks("399101.XSHE")


check_out_lists = filter_st_stock(check_out_lists)

q = query(valuation.code).filter(
    valuation.code.in_(check_out_lists)
).order_by(
    valuation.circulating_market_cap.asc()
).limit(
    10 * 5
)
check_out_lists = list(get_fundamentals(q).code)

def get_two_float(f_str, n):
    f_str = str(f_str)      # f_str = '{}'.format(f_str) 也可以转换为字符串
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])



def MA120_xielv(security):
    array_bars = get_bars(security, 121, '1d', fields=['close'], include_now =True)
    ma_now = array_bars[1:120]
    ma_last = array_bars[0:120]
    k_ma = np.mean(ma_now['close'])/np.mean(ma_last['close'])
    print(get_two_float(k_ma,2),k_ma,security)
    return get_two_float(k_ma,2) == '1.00'


    
def Stock_Filter(stocks, day, daytime):
    stocks = [
        stock for stock in stocks
        if len(get_trade_days(get_security_info(stock).start_date, day, count=None)) >= daytime
    ]
    return stocks

 

def Score(check_out_lists):
    check_out_lists = Stock_Filter(check_out_lists,'2020-05-01',120)
    newlist = filter(MA120_xielv, check_out_lists)
    return list(newlist)

Score(check_out_lists)