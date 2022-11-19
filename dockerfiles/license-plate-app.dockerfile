FROM python:3.9.13-slim-buster

WORKDIR /license-plate-app

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./backend/license-plate-app/requirements.txt .

RUN pip install --no-cache-dir -r /license-plate-app/requirements.txt

COPY ./backend/license-plate-app .

CMD [ "python", "main.py" ]

EXPOSE 8000