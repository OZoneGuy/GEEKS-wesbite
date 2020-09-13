#!/bin/bash

HELP="Please choose a valid command:\n\trestart | start | django | nginx | db"

if [  $# -eq 0]; then
    echo $HELP
    exit
fi


start() {
    docker-compose --project-directory $PATH up
}

restart() {
    docker-compose --project-directory $PATH restart
}

django() {
    docker-compose --project-directory $PATH exec -ti django /bin/bash
}

nginx() {
    docker-compose --project-directory $PATH exec -ti nginx /bin/bash
}

db() {
    docker-compose --project-directory $PATH exec -ti db /bin/bash
}

case $1 in
    "start")
        start
        ;;
    "restart")
        restart
        ;;
    "django")
        django
        ;;
    "nginx")
        nginx
        ;;
    "db")
        db
        ;;
esac
