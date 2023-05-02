FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY backup.py /app/
RUN chmod +x /app/backup.py

RUN apt-get update && apt-get install -y cron
RUN touch /var/log/cron.log
RUN (crontab -l ; echo "0 * * * * /usr/local/bin/python /app/backup.py >> /var/log/cron.log 2>&1") | crontab -

CMD cron && tail -f /var/log/cron.log
