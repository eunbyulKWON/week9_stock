from kafka import KafkaConsumer
import json

## 설정값을 일단 직접 작성 
KAFKA_SERVER = 'localhost:9092'
TOPIC_NAME = 'stock-prices'
GROUP_ID = 'price-alert-group'

## 이전 가격 저장용 
previous_prices = {}
## 임계치(3%)
THRESHOLD = 1.0 

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
        previous_prices = previous_prices[ticker]
        if previous_prices > 0:
            change_pct = (current_price - previous_prices) / previous_prices * 100
        else:
            change_pct = 0.0 

        ## 알림 설정 
        if abs(change_pct) > THRESHOLD:
            print(f"가격 변동 알림!!! : {ticker}이 {change_pct}% 변동!!!")
        else:
            print(f"가격 변동치가 적음 : {ticker}이 {change_pct}% 변동")


    except Exception as e:
        print(f"메시지 처리 중 오류 발생: {e}")
        
def run_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers = KAFKA_SERVER,
            group_id = GROUP_ID,
            auto_offset_reset='earliest',
            value_deserializer=lambda x:json.loads(x.decode('utf-8'))
        )
        print(f"Kafka Consumer 연결 성공 : {KAFKA_SERVER}, 토픽 : {TOPIC_NAME}")

        for message in consumer:
            print(f"메시지 수신 : {message.value}")
        # return consumer

    except Exception as e:
        print(f"Kafka Consumer 연결 실패 : {e}")
        return None

if __name__ == "__main__":
    run_consumer()