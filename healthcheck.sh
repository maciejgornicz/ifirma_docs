#! /bin/bash

getstatus() {
    curl \
    --silent \
    -o /dev/null \
    --write-out '%{http_code}' \
    "http://localhost:8080/healthcheck"
}
status=$(getstatus)
if [ $status -ne 200 ]; then
    echo -n "Service is unhealthy: "
    if (( $RESTART_UNHEALTHY )); then
        echo "Exiting..."
        kill 1
    else
        echo "Zombieing..."
        exit 1
    fi
fi