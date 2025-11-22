FROM python:3.11-slim

LABEL "language"="python"
LABEL "framework"="flask"

WORKDIR /app

# 安裝 gcc 和其他必要的編譯工具
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "judge.py"]
