FROM python:3.8.5

RUN mkdir -p /projects/insta2tgbot
COPY . /projects/insta2tgbot
WORKDIR /projects/insta2tgbot

RUN pip3 install -r /projects/insta2tgbot/requirements.txt

ENTRYPOINT ["python3", "bot.py"]
