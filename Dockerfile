FROM python:3.11

RUN apt-get update && \
    apt-get install -y \
    libopencv-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG AWS_ACCESS_KEY_ID=test
ARG AWS_SECRET_ACCESS_KEY=test

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN mkdir -p ~/.aws
RUN echo "[default]" > ~/.aws/config && \
    echo "region=us-east-2" >> ~/.aws/config && \
    echo "output=json" >> ~/.aws/config && \
    echo "[default]" > ~/.aws/credentials && \
    echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}" >> ~/.aws/credentials && \
    echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/credentials

CMD ["python", "app.py"]
