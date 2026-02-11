FROM python:3.11-slim

WORKDIR /worker

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY celery_app.py tasks.py ./

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=INFO"]
