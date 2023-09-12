FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["python", "app.py"]