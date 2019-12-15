FROM python:3.7.2-alpine3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY server.py /app/

RUN addgroup -g 1000 -S app && \
    adduser -u 1000 -S app -G app

USER 1000

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8080", "server"]
