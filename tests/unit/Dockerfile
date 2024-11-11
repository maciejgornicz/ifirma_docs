FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get dist-upgrade --yes && \
    apt-get install curl git -y && \
    python -m pip install -U pip

COPY tests/unit/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ .
COPY tests/ tests/
COPY setup.cfg .
RUN mkdir /data

SHELL ["/bin/bash", "-c"]
ENTRYPOINT [ "python3", "-m", "pytest"]

