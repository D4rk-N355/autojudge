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

<<<<<<< HEAD
CMD ["python", "judge.py"]
=======
CMD ["python", "judge.py"]
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9
