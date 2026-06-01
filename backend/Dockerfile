FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libmagic1 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create models directory for Hugging Face cache
RUN mkdir -p /app/models /app/uploads

# Copy requirements first (for Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download Hugging Face models (done once during build)
# This will be cached in the image, speeding up container startup
RUN python -c "from transformers import GPT2LMHeadModel, GPT2Tokenizer; \
    GPT2LMHeadModel.from_pretrained('gpt2'); \
    GPT2Tokenizer.from_pretrained('gpt2'); \
    print('GPT-2 downloaded')"

RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('all-MiniLM-L6-v2'); \
    print('Sentence-BERT downloaded')"

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 plagiat && \
    chown -R plagiat:plagiat /app
USER plagiat

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
