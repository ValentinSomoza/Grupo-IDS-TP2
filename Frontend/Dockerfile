FROM python:3.12-slim

WORKDIR /app

COPY ./Frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./Frontend /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["bash", "-c", "sleep 5 && flask run"]