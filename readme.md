# OSCAL Policy Administation Library (opal)

Provides a simple web application for managing System Security Plans.  The data modle is based on the OSCAL standard. 

## Deployment Instructions

### Clone and configure the app

1. Clone the repository to your local directory\
   `git clone https://gitlab.max.gov/max-security/opal.git`
1. Install some required packages\
   `sudo apt-get install python3-venv apache2-dev libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev python3-pip`
1. It is recomended to run the application from a virtual environment. To do so navigate to the application directory in a terminal and enter the following commands:\
   `python3 -m venv venv`\
   `source venv/bin/activate`
1. Install the required python modules by running:\
   `pip install -r requirements.txt`
1. create a local settings file\
   `cp opal/local_settings.py.template opal/local_settings.py`
1. Create a sqlite db file (or update the local_settings.py file with your database connection information)\
   `touch db.sqlite3`
1. Run the initial migration to create the database objects:\
   `python manage.py makemigrations`\
   `python manage.py migrate`
1. Create a superuser:\
   `python manage.py createsuperuser`
1. Start the Server\
   `python manage.py runserver`
## Start the app in a docker container
1. Clone the repository to your local directory
1. Build the image\
    `docker build -t opal:opal .`
1. Run the container\
    `docker run --rm -it --name opal -p 8000:8000 opal:opal`
    
Note: A default superuser account is created in the docker container. You should immedietly change the password and create additional secure superuser accounts.

Username: admin\
Password: admin
