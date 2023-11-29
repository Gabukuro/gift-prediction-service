FROM python:3.11

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libsm6 \
        libxext6 \
        libxrender-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
