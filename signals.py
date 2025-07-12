import requests, pandas as pd
from ta.momentum import RSIIndicator

TV_URL = "https://tvc4.forexpros.com/..."  # endpoint JSON do TradingView (ou use WebSocket)

def fetch_candles(symbol, tf="1", limit=150):
    # retorno = lista de [timestamp, open, high, low, close]
    data = requests.get(f"{TV_URL}/{symbol}?interval={tf}&points={limit}").json()
    df = pd.DataFrame(data, columns=["ts","o","h","l","c"])
    return df

def check_signal(df, rsi_len, rsi_high, rsi_low):
    rsi = RSIIndicator(df["c"], rsi_len).rsi()
    last_rsi = rsi.iloc[-2]   # vela recém-fechada
    last_close = df["c"].iloc[-2]
    last_high  = df["h"].iloc[-2]
    last_low   = df["l"].iloc[-2]

    # suporte = mínimo dos últimos 20
    sup = df["l"].rolling(20).min().iloc[-2]
    res = df["h"].rolling(20).max().iloc[-2]

    if last_close <= sup * 1.001 and last_rsi < rsi_low:
        return "CALL"
    if last_close >= res * 0.999 and last_rsi > rsi_high:
        return "PUT"
    return None