import time
import pyupbit
import datetime

access = "l89cbGwQkTXnoBKrjlcWcizdqiNiGN59x68VK8nZ"
secret = "oO9AobhIwa9VffVmzretNODivacHIXsnwsbPDPhE"
#tickers = pyupbit.get_tickers(fiat="KRW-ETH") #새로 추가

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(days=1)
#9:00 < 현재 < #8시 59분 50초 사이에 
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH", 0.6) # <- 이부분을 수정하면 새로운 전략이 된다 
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
        else:
            btc = get_balance("ETH")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

      #  sudo apt update
       # sudo apt install python3-pip
        #pip3 install pyupbit
        #nohup python3 bitcoinAutoTrade.py > output.log &
        #ps ax | grep .py
        #kill -9 PID
