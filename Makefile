APP ?= $(shell grep name setup.cfg | cut -d '=' -f2 | xargs)
STAGE ?= test

APP_PORT ?= 8080
APP_NAME ?= $(APP)-$(STAGE)

FTP_PORTS ?= 20-21
FTP_PASSIVE_PORTS ?= 40000-40009

DOCKER_CONTAINTER ?= $(APP)-service
DOCKER_IMAGE ?= $(DOCKER_CONTAINTER)-image
DOCKER_NETWORK ?= $(DOCKER_CONTAINTER)-network

DOCKER_TESTS_CONTAINER ?= $(DOCKER_CONTAINTER)-tests
DOCKER_TESTS_IMAGE ?= $(DOCKER_TESTS_CONTAINER)-image

ROOTDIR := $(shell pwd)

clean:
	-docker stop $(DOCKER_CONTAINTER)
	-docker rm $(DOCKER_CONTAINTER)
	-docker rmi $(DOCKER_IMAGE)

	-docker stop $(DOCKER_TESTS_CONTAINER)
	-docker rm $(DOCKER_TESTS_CONTAINER)
	-docker rmi $(DOCKER_TESTS_IMAGE)

image:
	docker build \
	-t $(DOCKER_IMAGE) \
	--build-arg APP_NAME=$(APP_NAME) \
	-f ./tests/unit/Dockerfile .

tests_image:
	docker build \
	-t $(DOCKER_TESTS_IMAGE) \
	--build-arg APP_NAME=$(APP_NAME) \
	-f ./tests/unit/Dockerfile .

unit: clean tests_image
	docker run \
	--rm \
	--name $(DOCKER_TESTS_CONTAINER) \
	--env-file env/.env.default \
	$(DOCKER_TESTS_IMAGE)

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

env_file:
	$(eval file=env/.env.$(STAGE))
	@cp -u env/.env.default $(file)
	@grep -q -e 'FTP_PORTS=' $(file) || sed -i '1s/^/FTP_PORTS=$(FTP_PORTS)\n/' $(file)
	@grep -q -e 'FTP_PASSIVE_PORTS=' $(file) || sed -i '1s/^/FTP_PASSIVE_PORTS=$(FTP_PASSIVE_PORTS)\n/' $(file)
	@grep -q -e 'APP_PORT=' $(file) || sed -i '1s/^/APP_PORT=$(APP_PORT)\n/' $(file)
	@grep -q -e 'APP=' $(file) || sed -i '1s/^/APP=$(APP)\n/' $(file)
	@grep -q -e 'STAGE=' $(file) || sed -i '1s/^/STAGE=$(STAGE)\n/' $(file)
	@sed -i "s|STAGE=.*|STAGE=$(STAGE)|g" $(file)

run: env_file
	docker-compose --env-file env/.env.$(STAGE) -p "$(APP_NAME)" --profile all up -d --build

stop:
	docker-compose -p "$(APP_NAME)" down