FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD python -m flask --app main.py run --host=0.0.0.0