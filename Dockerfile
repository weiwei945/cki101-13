# 使用與本機開發環境相同的 Python 版本
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴描述檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 宣告容器服務的埠號（Flask 預設為 5000）
EXPOSE 5000

# 啟動應用程式
CMD ["python", "app.py"]
