import argparse
import pandas as pd
from Ashare import get_price

def format_code(symbol):
    symbol = str(symbol).strip()
    if symbol.startswith(('6', '9', '5')):
        return 'sh' + symbol
    return 'sz' + symbol

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--period", type=str, default="1m")
    parser.add_argument("--count", type=int, default=2000) # 调高初始请求量
    parser.add_argument("--start", type=str, default="2025-01-01")
    
    args = parser.parse_args()
    code = format_code(args.symbol)
    
    print(f"🚀 开始循环抓取 {code}，目标频率: {args.period}...")

    # 第一次尝试抓取
    df = get_price(code, frequency=args.period, count=args.count)
    
    if df is not None and not df.empty:
        # 统一表头
        df = df.iloc[:, :6] 
        df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量']
        
        # 转换时间并排序
        df['时间'] = pd.to_datetime(df['时间'])
        df = df.sort_values('时间').drop_duplicates('时间')
        
        # 检查最早的时间点
        min_date = df['时间'].min()
        print(f"📍 当前已抓取到最早时间: {min_date}")

        # 过滤用户需要的起始日期
        df = df[df['时间'] >= pd.to_datetime(args.start)]
        
        if not df.empty:
            filename = f"{args.symbol}_{args.period}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✅ 成功保存 {len(df)} 行数据。")
        else:
            print("⚠️ 抓取到的数据均晚于设定的开始日期。")
    else:
        print("❌ 无法获取数据，请检查网络或股票代码。")
