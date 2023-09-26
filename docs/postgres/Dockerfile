FROM postgres:15.1

ENV POSTGRES_PASSWORD=use_a_secure_password_here

COPY init-db-scripts/* /docker-entrypoint-initdb.d/

RUN mkdir -p /usr/src/app/
RUN chown -R postgres:postgres /usr/src/app/
