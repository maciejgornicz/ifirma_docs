FROM python:3.11-slim-bookworm
ARG APP_NAME

WORKDIR /app

RUN apt-get update && \
    apt-get dist-upgrade --yes && \
    apt-get install git -y && \
    python -m pip install -U pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ .
RUN mkdir /data

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
