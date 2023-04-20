FROM python:3.9
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.3.1/tailwindcss-linux-x64 && chmod +x tailwindcss-linux-x64 && mv tailwindcss-linux-x64 tailwindcss

VOLUME ["/var/run/docker.sock:/var/run/docker.sock"]

CMD ["python", "main.py"]
EXPOSE 8090
