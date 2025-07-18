FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip --default-timeout=1000 --retries 10 install --no-cache-dir -r requirements.txt

COPY . .

# Copy the pre-downloaded model into the container
COPY all-MiniLM-L6-v2 ./all-MiniLM-L6-v2

CMD ["python", "extract_outline.py"]
