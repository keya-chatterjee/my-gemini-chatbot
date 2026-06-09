FROM python:3.11-slim

WORKDIR /app

# Install all necessary packages explicitly
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    google-genai \
    pydantic \
    pandas

# Copy the local files (including app.py and the data folder)
COPY . .

EXPOSE 8000

# Force Python to flush logs immediately so we see errors in 'docker logs'
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]