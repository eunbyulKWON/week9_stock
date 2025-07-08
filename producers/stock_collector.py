import yfinance as yf
from datetime import datetime 
from kafka import KafkaProducer
import json

def get_stock_data():
    try:
        # 1. 데이터 가져오기 
        data = yf.download('005930.KS', period='1d', interval='1m')
        print(data.iloc[:,-10:-1])
        # 2. 최신 데이터만 선택
        if not data.empty:
            latest = data.iloc[-1]
            # 3. 화면에 출력 - 최신데이터 
            message = {
                'ticker' : '005930.KS',
                'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'open' : float(latest['Open'].iloc[0]),
                'high' : float(latest['High'].iloc[0]),
                'low' : float(latest['Low'].iloc[0]),
                'close' : float(latest['Close'].iloc[0]),
                'volume' : float(latest['Volume'].iloc[0]),
                'change_pct' : float((latest['Close'].iloc[0]) - data.iloc[-2]['Close'] / data.iloc[-2]['Close'] * 100) if len(data) > 1 else 0.0
            }
            print(f"종목 : {message['ticker']}, 현재가 : {message['close']}, 변동률 : {message['change_pct']}%")
            # print("\n -- 데이터 가져오기 성공! --")
            # print(f"시간 : {latest.name}")
            # print(f"시가 : {latest['Open']}:.0f")
            # print(f"고가 : {latest['High']}:.0f")
            # print(f"저가 : {latest['Low']}:.0f")
            # print(f"중가 : {latest['Close']}:.0f")
            # print(f"거래량 : {latest['Volume']}:.0f")
            # print("--------------------------")

    except Exception as e:
        print(f"데이터 수집 중 오류 발생 : {e}")

if __name__ == "__main__":
    get_stock_data()
