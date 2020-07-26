# 导入函数库
import jqdata

# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    run_daily(period,time='every_bar')
    # 定义一个全局变量, 保存要操作的股票
    # 000001(股票:平安银行)
    g.security = ['002271.XSHE','000001.XSHE']
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def period(context):
    for str in g.security:
        order(str,100)


