FROM python:3.14-slim

WORKDIR /application

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY main.py .

RUN mkdir -p /application/data

EXPOSE 5000

CMD ["python", "main.py"]