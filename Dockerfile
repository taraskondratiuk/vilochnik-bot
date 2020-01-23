FROM python:3.8.1-alpine3.11

ADD /src/. /

RUN pip3 install redis pytelegrambotapi

CMD ["python", "./bot/bot.py"]