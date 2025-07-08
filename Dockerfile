# 1. 베이스 이미지 선택
# 파이썬 3.9dml 가벼운(slim) 버전을 기반으로 이미지 생성 
FROM python:3.9-slim

# 2. 작업 디렉토리 설정 
# 컨테이너 내부에 /app 디렉토리 생성, 앞으로 모든 작업을 해당 디렉토리에서 수행 
WORKDIR /app

# 3. 의존성 설치 (가장 중요한 최적화 단계)
# 먼저 requirements.txt 파일만 복사 
# 이 파일이 변경되지 않으면, 다음 빌드 시 캐시된 레이어를 사용하여 매우 빠르게 넘어감
COPY requirements.txt .

# requirements.txt에 명시된 라이브러리들을 설치 
RUN pip install --no-cache-dir -r requirements.txt 

# 4. 소스코드 복사
# 현재 디렉토리의 모든 파일(producers/, config/ 등)을 컨테이너의 /app 폴더로 복사 
COPY . . 

# 5. 컨테이너 실행 시 수행할 명령어 
# 이 컨테이너가 시작될 때, "python producers/stock_collector.py" 명령어 실행 
# CMD ["python", "producers/stock_collector.py"]
