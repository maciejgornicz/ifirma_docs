# ifirma-docs

This service is made for uploading scanned documents directly into ifirma.pl user account. It is not supported by ifirma.pl in any way. It does not use the ifirma.pl API, it performs its tasks using the Chrome browser and the Selenium library. It was created as a useful example of a microservice running in a docker-compose environment.

## Libraries and dependances
Using Python 3.11

There are two different python requirements:

* [test requirements](tests/unit/requirements.txt) - Used for unit tests and code analize
* [requirements](requirements.txt) - used for service

## Services

[Docker compose](docker-compose.yaml) contains some additional services providing functionalities for production use.

### Simple FTP service

Simple ftp server. This is useful for network printers with scanner functionality. Scanned document is uploaded to this servers shared directory for processing by ifirma_docs service.

Default FTP credentials (can be changed in [docker-compose.yaml](docker-compose.yaml))
* user: user
* pass: 123

### Selenium chrome browser service

Used to provide remote browser driver for selenium.

### Ifirma-docs service

This service is watching shared directory for new files (eg. uploaded via ftp). When file apears in shared directory, it is uploaded to ifirma user account as new document and deleted from shared directory.

## How to run

### Local development environment

#### Preparation
```bash
make prepare-develop
```
Command will prepare virtual python environment (venv) and install test requirements. Will also run FTP and Chrome docker containers (useful in development)

#### Configuration
Preparation will create ./env.develop configured ready to run local development environment. Adjust env variables to your need especially:
* `IFIRMA__LOGIN`
* `IFIRMA__PASSWORD`

#### Code analyze (flake8, mypy, pydocstyle)
```bash
make analyze
```

#### Unit tests
```bash
make unit
```

#### Debug
[.vscode](.vscode) included providing ready to run `VSCode launch debug target`.

### Prod/Prep/Test... environment

#### Configuration
To create defualt (`STAGE=test`) `.env` file run:
```bash
make env_file
```
Command will create `.env.test` file in [env](env).

To create different stage env file just use env variables:
```bash
make env_file STAGE=prod
```
Command will create `.env.prod` file in [env](env).

> [!NOTE]
> Edit `.env` file before run
#### Running

To run fully contenerized environment (default `STAGE=test`) run:
```bash
make run
```
It is possible to run different stage, just add custom env variable:
```bash
make run STAGE=prod
```
If you didn't run `make env_file STAGE=prod` before,
`.env.prod` file will be created with default values
and environment will try to run, so it is better to run `make env_file` first.

#### Stopping
To stop specific stage environment (eg. `prod`):
```bash
make stop STAGE=prod
```