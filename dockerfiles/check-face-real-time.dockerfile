FROM python:3.9.13-slim-buster

WORKDIR /check-face-real-time

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./backend/check-face-real-time/requirements.txt .

RUN pip install --no-cache-dir -r /check-face-real-time/requirements.txt

COPY ./backend/check-face-real-time .

CMD [ "python", "main.py" ]

EXPOSE 8000