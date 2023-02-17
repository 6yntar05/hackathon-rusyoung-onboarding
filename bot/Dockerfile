FROM python:3.10.10-alpine3.17
RUN apk update && apk upgrade && apk add bash

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python3", "/app/bot.py"]