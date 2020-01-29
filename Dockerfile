FROM python:3.8.1-alpine3.11

ADD /src/. /src/

RUN pip3 install redis pytelegrambotapi schedule bs4

CMD ["python", "./src/bot.py"]