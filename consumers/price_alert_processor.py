from kafka import KafkaConsumer
import json

## 설정값을 일단 직접 작성 
KAFKA_SERVER = 'localhost:9092'
TOPIC_NAME = 'stock-prices'
GROUP_ID = 'price-alert-group'

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