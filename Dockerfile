FROM python:3.9.16-alpine3.17
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.3.1/tailwindcss-linux-x64 && chmod +x tailwindcss-linux-x64 && mv tailwindcss-linux-x64 tailwindcss

CMD ["python", "main.py"]
EXPOSE 8090
