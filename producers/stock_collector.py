#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import yfinance as yf
from datetime import datetime 
from kafka import KafkaProducer
import json
import os
import sys

## 상위 디렉토리를 path에 추가하여 다른 모듈 import (config/config.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import KAFKA_SERVERS, TOPIC_NAME

## 설정값을 일단 직접 작성 
# KAFKA_SERVER = 'localhost:9092'
# TOPIC_NAME = 'stock-prices'

def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        # print(producer) 
        return producer
    except Exception as e:
        print(f"Kafka Producer 연결 실패 : {e}")
        return None
def get_and_send_data(producer):
    """ 주식 데이터 수집 및 Kafka 전송 """
    """ print 에서 출력하는 것을 Kafka Producer로 전달 """
    if not producer:
        print("Kafka Producer가 없습니다. 데이터 수집을 중단합니다")
        return
    
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
            print(f"현재가 : {message['close']}, 이전가격 : {data.iloc[-2]['Close']}")
            print(f"종목 : {message['ticker']}, 현재가 : {message['close']}, 변동률 : {message['change_pct']}%")
        # Kafka 토픽에 메시지 전송 
        producer.send(TOPIC_NAME, message)
        print(f"종목 데이터 전송 완료 : 현재가 {message['close']}")

        producer.flush()

    except Exception as e:
        print(f"종목 데이터 수집 중 오류 발생 : {e}")


# def get_stock_data():
#     try:
#         # 1. 데이터 가져오기 
#         data = yf.download('005930.KS', period='1d', interval='1m')
#         print(data.iloc[:,-10:-1])
#         # 2. 최신 데이터만 선택
#         if not data.empty:
#             latest = data.iloc[-1]
#             # 3. 화면에 출력 - 최신데이터 
#             message = {
#                 'ticker' : '005930.KS',
#                 'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'open' : float(latest['Open'].iloc[0]),
#                 'high' : float(latest['High'].iloc[0]),
#                 'low' : float(latest['Low'].iloc[0]),
#                 'close' : float(latest['Close'].iloc[0]),
#                 'volume' : float(latest['Volume'].iloc[0]),
#                 'change_pct' : float((latest['Close'].iloc[0]) - data.iloc[-2]['Close'] / data.iloc[-2]['Close'] * 100) if len(data) > 1 else 0.0
#             }
#             print(f"종목 : {message['ticker']}, 현재가 : {message['close']}, 변동률 : {message['change_pct']}%")
#             # print("\n -- 데이터 가져오기 성공! --")
#             # print(f"시간 : {latest.name}")
#             # print(f"시가 : {latest['Open']}:.0f")
#             # print(f"고가 : {latest['High']}:.0f")
#             # print(f"저가 : {latest['Low']}:.0f")
#             # print(f"중가 : {latest['Close']}:.0f")
#             # print(f"거래량 : {latest['Volume']}:.0f")
#             # print("--------------------------")

#     except Exception as e:
#         print(f"데이터 수집 중 오류 발생 : {e}")

if __name__ == "__main__":
    producer = create_producer()

    try:
        get_and_send_data(producer)
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램 종료")
    except Exception as e:
        print(f"예상치 못한 오류 발생 : {e}")
    
    finally:
        if producer:
            producer.close()
            print("Kafka producer 연결 종료")
