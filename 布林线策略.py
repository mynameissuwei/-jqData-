import jqdata
from jqlib.technical_analysis import *

def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    g.security = '002888.XSHE'
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),type='stock')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)




def handle_data(context, data):
    cash = context.portfolio.available_cash
    # 获取股票的收盘价
    close_data = attribute_history(g.security, 5, '1d', ['close'])
    current_price = close_data['close'][-1]
    upperband, middleband, lowerband = Bollinger_Bands(g.security, context.previous_date, timeperiod=60, nbdevup=2, nbdevdn=2)
    downValue = lowerband[g.security]
    upValue = upperband[g.security] 
    print(current_price,upValue,downValue,context.previous_date,'记录')
    #如果股价跌破下轨线则买入
    if current_price < downValue:
      order_value(g.security, cash)
    #如果突破上轨线则卖出
    elif current_price > upValue:
      order_target(g.security, 0)
