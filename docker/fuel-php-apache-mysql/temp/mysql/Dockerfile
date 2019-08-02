ARG MYSQL_VERSION=""
FROM mysql:${MYSQL_VERSION:-latest}

COPY ./install/ /docker-entrypoint-initdb.d/

EXPOSE 3306 3306