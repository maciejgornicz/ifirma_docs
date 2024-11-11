FROM python:3.11-slim-bookworm
WORKDIR /app

RUN apt-get update && \
    apt-get dist-upgrade --yes && \
    apt-get install curl git -y && \
    python -m pip install -U pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ .
COPY healthcheck.sh .
RUN mkdir /data

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
