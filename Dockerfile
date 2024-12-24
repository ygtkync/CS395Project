FROM python:3.10-slim

WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && apt-get install -y \
    procps \
    systemd \
    && apt-get clean

EXPOSE 8765

CMD ["python", "src/server.py"]

