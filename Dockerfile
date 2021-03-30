FROM python:3.8.5

WORKDIR /insta2tgbot
COPY . /insta2tgbot

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "bot.py"]
