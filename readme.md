The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

# OSCAL Policy Administration Library (opal)
Provides a simple web application for managing System Security Plans and related documents.  The data model is based on the OSCAL standard and objects can be imported and exported in OSCAL compliant JSON. 

The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

1. Python >=3.8
2. apache
3. postgres client if using a postgres database

# Deployment Instructions
## Running a local development version using sqlite
1. Clone the repository to your local directory\
   `git clone https://github.com/eop-omb/opal.git`
1. It is recommended to run the application from a virtual environment. To do so navigate to the application directory in a terminal and enter the following commands:\
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
## Start the app in a docker container using sqlite
1. Clone the repository to your local directory
   `git clone https://gitlab.max.gov/max-security/opal.git`
3. Build the image\
    `docker build -t opal .`
1. Run the container\
    `docker run --rm -it --name opal -p 8000:8000 -e DB_HOST=localhost -e DB_NAME=db.sqlite3 -e LOG_LEVEL=DEBUG -e opal`
    

## Setting environment variables
OPAL is designed to run well in a containerized environment. It is recommended to set any desired environment variables using your chosen container orchestration solution (kubernetes, docker-compose, etc.).  You can also set environment variables in a .env file which should be placed in the opal subdirectory. All variables are optional and will be populated with reasonable defaults if not provided. 

**NOTE: defaults will be applied if the environment variable is NOT provided, but if you provide an empty string or something similar the application will not overwrite that with the default value.**

You can find a list of all environment variables and thier defaults in the opal/settings.py file.