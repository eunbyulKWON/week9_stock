#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer
import json
import os
import sys

## 설정 파일 불러오기 위해 상위 디렉토리 추가 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import (
    KAFKA_SERVERS,
    TOPIC_NAME,
    PRICE_CHANGE_THRESHOLD
)

## 설정값을 일단 직접 작성 
# KAFKA_SERVER = 'localhost:9092'
# TOPIC_NAME = 'stock-prices'
# GROUP_ID = 'price-alert-group'

## 이전 가격 저장용 
previous_prices = {}
## 임계치(3%)
# THRESHOLD = 1.0 

def process_message(message):
    try:
        ticker = message['ticker']
        current_price = message['close']
        change_pct = message.get('change_pct', 0.0)
        
        #  이전 가격이 없는 경우 현재 가격 저장 후 처리 종료 
        if ticker not in previous_prices:
            previous_prices[ticker] = current_price
            print(f"종목 {ticker}의 초기 가격 : {current_price} 설정")
            return
        
        # 가격 변동률 계산 
        prev_prices = previous_prices[ticker]
        if prev_prices > 0:
            change_pct = (current_price - prev_prices) / prev_prices * 100
        else:
            change_pct = 0.0 

        ## 알림 설정 
        if abs(change_pct) > PRICE_CHANGE_THRESHOLD:
            print(f"가격 변동 알림!!! : {ticker}이 {change_pct}% 변동!!!")
        else:
            print(f"가격 변동치가 적음 : {ticker}이 {change_pct}% 변동")

        ## 다음 계산을 위해 현재 가격을 이전 가격으로 업데이트 
        previous_prices[ticker] = current_price
    
    except KeyError as  e:
        print(f"메시지에 필요한 키가 없습니다 : {e} - 메시지 내용 : {message}")

    except Exception as e:
        print(f"메시지 처리 중 오류 발생: {e}")

def run_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers = KAFKA_SERVERS,
            # group_id = GROUP_ID,
            auto_offset_reset='earliest',
            value_deserializer=lambda x:json.loads(x.decode('utf-8'))
        )
        print(f"Kafka Consumer 연결 성공 : {KAFKA_SERVERS}, 토픽 : {TOPIC_NAME}")

        for message in consumer:
            print(f"메시지 수신 : {message.value}")
            process_message(message.value)

    except Exception as e:
        print(f"Kafka Consumer 연결 실패 : {e}")
        return None
    

if __name__ == "__main__":
    run_consumer()