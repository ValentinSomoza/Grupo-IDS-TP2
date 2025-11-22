FROM python:3.12-slim
WORKDIR /app
COPY . /app
COPY Backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
COPY ./Backend /app

EXPOSE 5001

CMD [ "flask", "run"]
#CMD ["python3", "app.py"]
#CMD ["python", "app.py"]