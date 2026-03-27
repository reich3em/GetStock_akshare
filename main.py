import argparse
import pandas as pd
from Ashare import get_price

def format_code(symbol):
    """自动给代码补全前缀"""
    symbol = str(symbol)
    if symbol.startswith(('6', '9', '5')):
        return 'sh' + symbol
    return 'sz' + symbol

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True, help="股票代码如 600900")
    parser.add_argument("--period", type=str, default="1d", help="1d, 1m, 5m, 15m, 30m, 60m")
    parser.add_argument("--count", type=int, default=1000, help="获取最近多少条记录")
    parser.add_argument("--start", type=str, default="2025-01-01", help="开始日期 YYYY-MM-DD")
    
    args = parser.parse_args()
    
    # 1. 转换代码格式
    code = format_code(args.symbol)
    
    # 2. 获取数据
    print(f"正在从腾讯接口获取 {code} 的数据...")
    df = get_price(code, frequency=args.period, count=args.count)
    
    if df is not None and not df.empty:
        # 3. 强制重命名列（解决 KeyError: 'time'）
        # Ashare 返回的列通常是: 时间, 开盘, 收盘, 最高, 最低, 成交量
        df.columns = ['time', 'open', 'close', 'high', 'low', 'volume']
        
        # 4. 时间过滤
        df['time'] = pd.to_datetime(df['time'])
        df = df[df['time'] >= args.start]
        
        # 5. 最终保存前转换为中文表头
        df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量']
        
        print(f"成功筛选出 {len(df)} 条数据。")
        filename = f"{args.symbol}_{args.period}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"文件保存成功: {filename}")
    else:
        print("错误：未能获取到数据，请检查网络或股票代码。")
