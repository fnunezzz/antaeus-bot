FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD gunicorn --workers=1 main:app --bind 0.0.0.0:5000