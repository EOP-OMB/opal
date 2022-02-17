# OSCAL Policy Administration Library (opal)
Provides a simple web application for managing System Security Plans and related documents.  The data model is based on the OSCAL standard and objects can be exported in OSCAL compliant JSON. 

The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

1. Python >=3.8
2. apache
3. postgres client if using a postgres database

# Deployment Instructions
## Running a local development version using mysql
1. Clone the repository to your local directory\
   `git clone https://github.com/eop-omb/opal.git`
1. It is recomended to run the application from a virtual environment. To do so navigate to the application directory in a terminal and enter the following commands:\
   `python3 -m venv venv`\
   `source venv/bin/activate`
1. Install the required python modules by running:\
   `pip install -r requirements.txt`
1. Run the initial migration to create the database objects:\
   `python manage.py makemigrations`\
   `python manage.py migrate`
1. Create a superuser:\
   `python manage.py createsuperuser`
1. Start the Server\
   `python manage.py runserver`
## Start the app in a docker container using mysql
1. Clone the repository to your local directory
   `git clone https://gitlab.max.gov/max-security/opal.git`
3. Build the image\
    `docker build -t opal:opal .`
1. Run the container\
    `docker run --rm -it --name opal -p 8000:8000 opal:opal`
    
Note: A default superuser account is created in the docker container. You should immedietly change the password and create additional secure superuser accounts.

Username: admin\
Password: admin
## Setting environment variables
OPAL is designed to run well in a containerized environment. It is recomended to set any desired environment variables using your chosen container orchestration solution (kubernetes, docker-compose, etc.).  You can also set environment variables in a .env file which should be placed in the opal subdirectory. The available environment variables are: \

   "environment", #development or production \
   "opal_secret_key", #secret key used to create sessions \
   "debug", #True of False \
   "allowed_hosts", #Must be a comma seperated list of acceptable host names to use when accessing the application. Use '*' for all \
   "database", #sqlite or postgres \
   "db_password", #can be blank if using sqlite \
   "db_name", #name of db in postgres, can be blank if using sqlite \
   "db_user", #can be blank if using sqlite \
   "db_host", #can be blank if using sqlite \
   "db_port", #can be blank if using sqlite \
   "adfs_enabled", #True or False \
   "adfs_server", #can be blank if adfs_enabled is False \
   "adfs_client_id", #can be blank if adfs_enabled is False \
   "adfs_client_id", #can be blank if adfs_enabled is False \
   "adfs_relying_party_id", #can be blank if adfs_enabled is False \
   "adfs_audience" #can be blank if adfs_enabled is False \
