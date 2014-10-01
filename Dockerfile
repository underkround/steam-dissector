FROM underkround/python:2

ADD /steam_dissector /app
WORKDIR /app

ADD /requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENV WORKERS 5
ENV PORT 8080

EXPOSE 8080

CMD gunicorn main:app -b 0.0.0.0:$PORT -w $WORKERS --access-logfile -
