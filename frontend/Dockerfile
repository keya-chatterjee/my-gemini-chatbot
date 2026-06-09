FROM python:3.11-slim

WORKDIR /app

# Install the frontend packages directly inside the container
RUN pip install --no-cache-dir streamlit requests

# Copy all files from the frontend folder into the container
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]