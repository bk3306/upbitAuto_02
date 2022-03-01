import time
import pyupbit
import datetime

access = "xzW2WJJ0fiDD6i6r7ufuQsURQQ3fHB3beEnNzMcp"
secret = "Dk0dEDUw9iAObVKJNq8vRTFesS8CM0WQQjdbP8FU"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_low_price(ticker):
    """전날 저가 구해서 밑으로 내려가면 손절"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    low_price = df.iloc[0]['low']
    return low_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    """10시간 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=10)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

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
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") #3:00
        end_time = start_time + datetime.timedelta(hours=1) #3:00 + 1h
        low_price = get_low_price("KRW-BTC")
        # 3:00 < now < 3:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            ma10 = get_ma10("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if ma10 < current_price:
                target_price = get_target_price("KRW-BTC", 0.2)
                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
            if ma10 > current_price:
                target_price = get_target_price("KRW-BTC", 0.5)
                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
            if current_price < low_price:
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)