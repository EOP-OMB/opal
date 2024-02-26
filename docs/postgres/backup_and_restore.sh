DUMP
// pod-name         name of the postgres pod
// postgres-user    database user that is able to access the database
// database-name    name of the database
kubectl -n opal exec $(kubectl get pods -n opal | grep opal-postgres-db | cut -f 1 -d ' ' -s) -- bash -c "pg_dump -U postgres opal" > database.sql



RESTORE
// pod-name         name of the postgres pod
// postgres-user    database user that is able to access the database
// database-name    name of the database
cat database.sql | kubectl exec -i $(kubectl get pods -n opal | grep opal-postgres-db | cut -f 1 -d ' ' -s) -- psql -U postgres -d opal