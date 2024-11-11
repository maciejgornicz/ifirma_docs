APP_NAME ?= ifirma_docs
DOCKER_CONTAINTER ?= $(APP_NAME)-service
DOCKER_IMAGE ?= $(DOCKER_CONTAINTER)-image
DOCKER_NETWORK ?= $(DOCKER_CONTAINTER)-network

DOCKER_TEST_CONTAINER ?= $(DOCKER_CONTAINTER)-test
DOCKER_TEST_IMAGE ?= $(DOCKER_TEST_CONTAINER)-image

ROOTDIR := $(shell pwd)

clean:
	-docker stop $(DOCKER_CONTAINTER)
	-docker rm $(DOCKER_CONTAINTER)
	-docker rmi $(DOCKER_IMAGE)

	-docker stop $(DOCKER_TEST_CONTAINER)
	-docker rm $(DOCKER_TEST_CONTAINER)
	-docker rmi $(DOCKER_TEST_IMAGE)

	-docker network rm $(DOCKER_NETWORK)

network:
	-docker network create --subnet=192.168.253.0/24 $(DOCKER_NETWORK)
	docker network ls

image:
	docker build \
	-t $(DOCKER_IMAGE) \
	--build-arg APP_NAME=$(APP_NAME) \
	-f ./tests/unit/Dockerfile .

test_image:
	docker build \
	-t $(DOCKER_TEST_IMAGE) \
	--build-arg APP_NAME=$(APP_NAME) \
	-f ./tests/unit/Dockerfile .

unit: clean test_image
	docker run \
	--rm \
	--name $(DOCKER_TEST_CONTAINER) \
	--env-file env/.env.default \
	$(DOCKER_TEST_IMAGE)

prepare-env:
	python3 -m venv venv
	. ./venv/bin/activate
	pip3 install --upgrade pip
	pip3 install --no-cache-dir -r ./tests/unit/requirements.txt
	cp -u env/.env.default env/.env.develop
	mkdir -p $(ROOTDIR)/data
	sed -i "s|WATCHED_DIR=/data|WATCHED_DIR=$(ROOTDIR)/data|g" env/.env.develop

prepare-develop: prepare-env
	docker-compose up -d

flake8: prepare-env
	flake8 src

mypy: prepare-env
	mypy src

pydocstyle: prepare-env
	pydocstyle src

analyze: clean prepare-env flake8 mypy pydocstyle

test: clean analyze unit

run:
	docker-compose --profile all up -d --build