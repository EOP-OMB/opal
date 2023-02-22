FROM postgres:15.1

ENV POSTGRES_PASSWORD=use_a_secure_password_here

COPY init-db-scripts/* /docker-entrypoint-initdb.d/
