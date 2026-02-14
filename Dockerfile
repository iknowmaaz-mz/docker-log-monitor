FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN mkdir -p /app/logs
EXPOSE 5000
CMD ["sh", "-c", "python monitor.py & python server.py"]
