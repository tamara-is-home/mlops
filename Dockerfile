FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

RUN mkdir ./images
RUN mkdir ./models
RUN mkdir ./templates

COPY images/test/* ./images
COPY models/* ./models
COPY inference.py ./
COPY rest_api.py ./
COPY requirements.txt ./
COPY templates/index.html ./templates/

RUN pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

CMD ["python", "rest_api.py"]