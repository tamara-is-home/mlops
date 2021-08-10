FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

RUN mkdir ./images
RUN mkdir ./models

COPY test* ./images
COPY models/* ./models
COPY inference.py ./
COPY rest_api.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

CMD ["python"]