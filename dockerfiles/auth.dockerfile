FROM python:3.9.13-slim-buster

WORKDIR /auth

COPY ./backend/auth/requirements.txt .

RUN pip install --no-cache-dir -r /auth/requirements.txt

COPY ./backend/auth .

CMD [ "python", "main.py" ]

EXPOSE 8000