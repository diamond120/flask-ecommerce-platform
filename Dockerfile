FROM python:3

WORKDIR /app

RUN pip install flask
RUN pip install -U Flask-SQLAlchemy

RUN pip install requests

COPY . .

EXPOSE 5000

CMD ["python", "./wsgi.py"]


