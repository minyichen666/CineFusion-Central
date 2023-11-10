FROM mysql:latest
COPY create-table.sql /docker-entrypoint-initdb.d/
