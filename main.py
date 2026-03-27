import argparse
import pandas as pd
from Ashare import get_price

def format_code(symbol):
    """自动给代码补全前缀"""
    if symbol.startswith('6'):
        return 'sh' + symbol
    return 'sz' + symbol

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True, help="股票代码如 600900")
    parser.add_argument("--period", type=str, default="1d", help="1d, 1m, 5m, 15m, 30m, 60m")
    parser.add_argument("--count", type=int, default=1000, help="获取最近多少条记录")
    parser.add_argument("--start", type=str, default="2025-01-01", help="开始日期 YYYY-MM-DD")
    
    args = parser.parse_args()
    
    # 转换代码格式
    code = format_code(args.symbol)
    
    # 获取数据
    df = get_price(code, frequency=args.period, count=args.count)
    
    # 时间过滤
    df['time'] = pd.to_datetime(df['time'])
    df = df[df['time'] >= args.start]
    
    # 修改表头为中文，并解决乱码
    df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量']
    
    if not df.empty:
        print(f"成功获取 {args.symbol} 数据：")
        print(df.tail())
        filename = f"{args.symbol}_{args.period}.csv"
        # 保持之前的 utf-8-sig 编码优化
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    else:
        print("未筛选到指定日期范围内的数据。")
