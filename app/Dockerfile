FROM python:3.11-slim-buster
RUN apt-get update \
     && mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR ..
CMD ["python","app/main.py"]