FROM python:3.12-slim-bookworm

# Install supervisor
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Install fast python package installer "uv"
RUN pip install --no-cache-dir uv

WORKDIR /app

ENV TZ=Asia/Kolkata
ENV UV_HTTP_TIMEOUT=120

COPY . .

# Install dependencies
RUN uv pip install --system --no-cache -r requirements.txt

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["/usr/bin/supervisord"]
