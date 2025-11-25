FROM python:3.12-slim
WORKDIR /app
COPY . /app
COPY Frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./Frontend /app
ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
COPY ./Backend /app
EXPOSE 5000
CMD ["flask", "run"]