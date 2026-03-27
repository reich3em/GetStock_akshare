import akshare as ak
import argparse
import pandas as pd

def fetch_stock_data(symbol, period, start_date, end_date):
    """
    symbol: 股票代码 (如 000001)
    period: 颗粒度 (daily, weekly, monthly, 1, 5, 15, 30, 60 分钟)
    """
    print(f"正在获取 {symbol} 的数据，周期：{period}...")
    
    # 针对日线及以上颗粒度
    if period in ['daily', 'weekly', 'monthly']:
        df = ak.stock_zh_a_hist(symbol=symbol, period=period, 
                                start_date=start_date, end_date=end_date, adjust="qfq")
    # 针对分钟级数据
    else:
        df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, 
                                       start_date=start_date, end_date=end_date, adjust="qfq")
    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True, help="股票代码")
    parser.add_argument("--period", type=str, default="daily", help="颗粒度: daily, 1, 5, 15...")
    parser.add_argument("--start", type=str, default="20230101", help="开始日期 YYYYMMDD")
    parser.add_argument("--end", type=str, default="20261231", help="结束日期 YYYYMMDD")
    
    args = parser.parse_args()
    
    data = fetch_stock_data(args.symbol, args.period, args.start, args.end)
    print(data.tail()) # 输出最后5行到日志
    # 使用 utf-8-sig 编码，完美解决 Excel 打开乱码问题
    data.to_csv(f"{args.symbol}_{args.period}.csv", index=False, encoding='utf-8-sig')
