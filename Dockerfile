FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl bash zstd \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app.py .
COPY database.py .
COPY vector.py .
COPY realistic_restaurant_reviews.csv .
COPY chrom_langchain_db ./chrom_langchain_db
COPY templates ./templates
COPY start.sh .

RUN chmod +x start.sh

# after installing ollama, pull models during BUILD not runtime
RUN ollama serve & sleep 8 && \
    ollama pull mxbai-embed-large && \
    ollama pull llama3 && \
    killall ollama || true

EXPOSE 11434
EXPOSE 5000

CMD ["./start.sh"]