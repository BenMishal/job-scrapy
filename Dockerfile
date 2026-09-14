FROM python:3.10-slim

# Create a non-root user
RUN groupadd -r scrapy && useradd -r -g scrapy scrapy

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set permissions
RUN chown -R scrapy:scrapy /app

USER scrapy

# Ensure stdout is unbuffered for MCP communication
ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]
