FROM python:3.9.13

WORKDIR /face-recognition

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

COPY ./backend/face-recognition/requirements.txt .

RUN pip install --no-cache-dir -r /face-recognition/requirements.txt

RUN pip install eventlet

COPY ./backend/face-recognition .

CMD [ "python", "main.py" ]

EXPOSE 8000