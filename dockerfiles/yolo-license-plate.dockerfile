FROM python:3.9.13-slim-buster

WORKDIR /yolo-license-plate

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

COPY ./backend/yolo-license-plate/requirements.txt .

RUN pip install --no-cache-dir -r /yolo-license-plate/requirements.txt

COPY ./backend/yolo-license-plate .

CMD [ "python", "main.py" ]

EXPOSE 8000