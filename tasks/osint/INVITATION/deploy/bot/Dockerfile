FROM python:3.9

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT python3 mail_bot.py