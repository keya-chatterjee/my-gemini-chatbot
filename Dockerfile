FROM python:3.11-slim

WORKDIR /app

# Copy the shopping list into the container first
COPY requirements.txt /app/requirements.txt

# Tell pip to install everything listed in that shopping list
RUN pip install -r requirements.txt

COPY app.py /app/app.py

CMD ["python", "app.py"]