FROM postgres:15.1

ENV POSTGRES_PASSWORD=use_a_secure_password_here

COPY init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
