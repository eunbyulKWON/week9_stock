#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

"""
설정 파일
Stock Alert Pipeline 프로젝트에서 사용되는 설정 값들을 정의합니다.
"""
## python-dotenv reads key-value pairs from a .env file and can set them as environment variables
## load_dotenv()  # take environment variables
## Code of your application, which uses environment variables (e.g. from `os.environ` or
## `os.getenv`) as if they came from the actual environment.

import os 
from dotenv import load_dotenv

# .env 파일 로드 (존재하는 경우)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

## Kafka 설정
KAFKA_SERVERS=os.getenv('KAFKA_SERVERS', 'localhost:9092')
TOPIC_NAME=os.getenv('TOPIC_NAME', 'stock-prices')

## 데이터 수집 설정 
STOCK_TICKERS=os.getenv('STOCK_TICKERS', '005930.KS')
STOCK_COLLECTION_INTERVAL=int(os.getenv('STOCK_COLLECTION_INTERVAL', 300))

# 알림 설정 
PRICE_CHANGE_THRESHOLD=float(os.getenv('PRICE_CHANGE_THRESHOLD', 1.0))
VOLUME_CHANGE_THRESHOLD=float(os.getenv('VOLUME_CHANGE_THRESHOLD', 20.0))
TECHNICAL_INDICATOR_THRESHOLD=float(os.getenv('TECHNICAL_INDICATOR_THRESHOLD', 10.0))

# 로깅 설정
LOG_LEVEL=os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE_MAX_BYTES=int(os.getenv('LOG_FILE_MAX_BYTES', 10485760))
LOG_FILE_BACKUP_COUNT=int(os.getenv('LOG_FILE_BACKUP_COUNT', 5))