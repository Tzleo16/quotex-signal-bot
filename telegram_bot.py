import yaml, time
import telegram
from signals import fetch_candles, check_signal

cfg = yaml.safe_load(open("config.yaml"))
bot  = telegram.Bot(cfg["telegram_token"])

def send_alert(pair, direction):
    msg = (f"📢 *SINAL M1* – {pair}\n"
           f"» Direção: *{direction}*\n"
           f"» Estratégia: Price Action + RSI + S/R\n"
           f"_Martingale até nível {cfg['martingale_levels']}_")
    bot.send_message(chat_id=cfg["chat_id"], text=msg, parse_mode="Markdown")

while True:
    for pair in cfg["symbols"]:
        candles = fetch_candles(pair, cfg["timeframe"])
        sig = check_signal(candles,
                           cfg["rsi_length"],
                           cfg["rsi_high"],
                           cfg["rsi_low"])
        if sig:
            send_alert(pair, sig)
    time.sleep(cfg["check_interval_sec"])