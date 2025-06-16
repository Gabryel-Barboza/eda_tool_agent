FROM bitnami/mysql:9.3.0

COPY create_tables.sql /docker-entrypoint-initdb.d/
