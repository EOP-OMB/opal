The included files will help you setup a postgres database server for opal.

**Deploying a postgres instance in a container**

1. Open the included Dockerfile and specify a password for the default postgres user. This user will have superuser privileges on your postgres database so pick a strong password.
2. Create a new docker image from the included Dockerfile 
<pre>docker build -t opal-db .</pre>
This will create an image based on the latest postgres image from dockerhub that includes an init script to create the opal database and user account.  The script runs on container creation and accepts the opal user's password from an environment password "POSTGRES_OPAL_PASSWORD"
3. Create a volume to store the data.
<pre>docker volume create postgresql</pre>
4. To start the postgres db container locally you can run 
<pre>docker run -it -d -p 5432:5432 --name opaldb  -v postgresql:/var/lib/postgresql/data -e POSTGRES_PASSWORD=use_a_secure_password_here -e POSTGRES_OPAL_PASSWORD=letmein opal-db</pre>
But the recommended solution is to use the kubernetes deployment files in docs/k8/ directory to deploy the application and the database to a kubernetes cluster.

**Deployment to an existing postgres instance**

If you just want to deploy the opal database to an existing postgres instance you can just use the script in the init-user-db.sh file.