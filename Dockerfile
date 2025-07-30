FROM python:3.9-slim

# 1. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        tar \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Akash CLI (without checksum verification for now)
RUN curl -fsSLO https://github.com/akash-network/node/releases/download/v0.28.0/akash_0.28.0_linux_amd64.tar.gz && \
    tar -xzf akash_0.28.0_linux_amd64.tar.gz && \
    mv akash_0.28.0_linux_amd64/akash /usr/local/bin/ && \
    chmod +x /usr/local/bin/akash && \
    rm -rf akash_0.28.0_linux_amd64*

# 3. Set up workspace
WORKDIR /app
COPY . .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot/start.py"]
