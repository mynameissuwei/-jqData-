def initialize(context):
  run_daily(period,time='every_bar')
  # 设定好要交易的股票数量stocksnum
  g.stocksnum = 10

def period(context):
  # 代码：找出市值排名最小的前stocksnum只股票作为要买入的股票
  # 获取上证指数和深证综指的成分股代码并连接，即为全A股市场所有股票的股票代码
  # 用加号可以连接两个list
  scu = get_index_stocks('000001.XSHG')+get_index_stocks('399106.XSHE')
  # 选出在scu内的市值排名最小的前stocksnum只股票
  q=query(valuation.code
              ).filter(
                  valuation.code.in_(scu)
              ).order_by(
                  valuation.market_cap.asc()
              ).limit(g.stocksnum)
  df = get_fundamentals(q)
  # 选取股票代码并转为list
  buylist=list(df['code'])

  # 代码：若已持有的股票的市值已经不够小而不在要买入的股票中，则卖出这些股票。
  # 对于每个当下持有的股票进行判断：现在是否已经不在buylist里，如果是则卖出
  for stock in context.portfolio.positions:
      if stock not in buylist: #如果stock不在buylist
          order_target(stock, 0) #调整stock的持仓为0，即卖出

  # 代码：买入要买入的股票，买入金额为可用资金的stocksnum分之一
  # 将资金分成g.stocksnum份
  position_per_stk = context.portfolio.cash/g.stocksnum
  # 用position_per_stk大小的g.stocksnum份资金去买buylist中的股票
  for stock in buylist:
      order_value(stock, position_per_stk)