import pandas as pd
import requests

def get_price(code, frequency='1d', count=1000):
    """
    针对腾讯接口优化的 Ashare 逻辑
    """
    # 转换频率格式
    if frequency == '1d':
        url = f'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={code},day,,, {count},qfq'
    else:
        # 分钟线：m1, m5, m15, m30, m60
        m_period = frequency.replace('m', '')
        # 核心逻辑：腾讯的 mkline 接口在 count 超过 320 时，
        # 部分服务器节点支持返回最多 1000-2000 条，我们直接请求目标总数
        url = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={code},m{m_period},,{count}'
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        json_data = res.json()
        
        if frequency == '1d':
            raw = json_data['data'][code]
            data = raw.get('qfqday', raw.get('day'))
        else:
            m_key = f"m{frequency.replace('m', '')}"
            data = json_data['data'][code][m_key]
        
        return pd.DataFrame(data)
    except Exception as e:
        print(f"接口抓取失败: {e}")
        return pd.DataFrame()
