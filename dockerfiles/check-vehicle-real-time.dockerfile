FROM python:3.9.13-slim-buster

WORKDIR /check-vehicle-real-time

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./backend/check-vehicle-real-time/requirements.txt .

RUN pip install --no-cache-dir -r /check-vehicle-real-time/requirements.txt

COPY ./backend/check-vehicle-real-time .

CMD [ "python", "main.py" ]

EXPOSE 8000