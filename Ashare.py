import pandas as pd
import requests

def get_price(code, end_date=None, count=10, frequency='1d'):
    if frequency == '1d':
        url = f'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={code},day,,, {count},qfq'
    else:
        url = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={code},m{frequency[:-1]},,{count}'
    
    res = requests.get(url)
    json_data = res.json()
    
    try:
        if frequency == '1d':
            data = json_data['data'][code].get('qfqday', json_data['data'][code].get('day'))
        else:
            data = json_data['data'][code][f'm{frequency[:-1]}']
        
        df = pd.DataFrame(data)
        if df.empty: return df
        
        # 仅取前6列：时间, 开盘, 收盘, 最高, 最低, 成交量
        df = df.iloc[:, :6]
        return df
    except Exception as e:
        print(f"解析数据出错: {e}")
        return pd.DataFrame()
