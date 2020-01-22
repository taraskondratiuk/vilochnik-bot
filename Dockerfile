FROM python:3

ADD /src/. /


RUN pip install --upgrade pip
RUN pip install redis
RUN pip install pytelegrambotapi

CMD ["python", "./bot/bot.py"]