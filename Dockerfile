FROM python:3.11

RUN apt-get update && \
    apt-get install -y \
    libopencv-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


RUN mkdir -p ~/.aws
RUN echo "[default]" > ~/.aws/config && \
    echo "region=us-east-2" >> ~/.aws/config && \
    echo "output=json" >> ~/.aws/config && \
    echo "[default]" > ~/.aws/credentials && \
    echo "aws_access_key_id=<aws_access_key>" >> ~/.aws/credentials && \
    echo "aws_secret_access_key=<aws_secret_access_key>" >> ~/.aws/credentials

CMD ["python", "app.py"]
