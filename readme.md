# OSCAL Policy Administation Library (opal)
Provides a simple web application for managing System Security Plans.  The data modle is based on the OSCAL standard. 
# Deployment Instructions
## Clone and configure the app
1. Clone the repository to your local directory\
   `cd /opt/`\
   `sudo mkdir opal`\
   `sudo chown -R user:user /opt/opal/`\
1. Install some required packages\
   `sudo apt-get install python3-venv apache2-dev libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev python3-pip`
1. It is recomended to run the application from a virtual environment. To do so navigate to the application directory in a terminal and enter the following commands:\
   `python3 -m venv venv`\
   `source venv/bin/activate`
1. Install the required python modules by running:\
   `pip install -r requirements.txt`
1. Create a sqlite db file (or update the settings.py file with your database connection information)\
   `touch db.sqlite3`
1. Run the initial migration to create the database objects:\
   `python manage.py makemigrations`\
   `python manage.py migrate`
1. Create a superuser:\
   `python manage.py createsuperuser`
1. Start the Server\
   `python manage.py collectstatic`\
   `python manage.py runmodwsgi --user www-data --group www-data`\
## Start the app in a docker container
1. Clone the repository to your local directory
1. Build the image\
    `docker build -t opal:opal .`
1. Run the container\
    `docker run -p 8000:8000`
    
Note: A default superuser account is created in the docker container. You should immedietly change the password and create additional secure superuser accounts.

Username: admin\
Password: admin
              
## Load initial data
Note: These import scripts are pretty buggy right now.  Best of luck.\
1. Create a folder at the root of your application called "source"\
   `mkdir source`
1. Download the NIST SP 800-53 rev. 5 JSON catalog\
   `wget https://github.com/usnistgov/oscal-content/raw/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5-FINAL_catalog.json -O source/NIST_SP-800-53_rev4_catalog.json`
1. Run the import script for the NIST Controls\
   `python manage.py runscript OSCAL_Catalog_import`
1. Assuming you have a Word document in the FedRAMP template with your controls in it, You can import those using the importSecurityControlsFromWord script\
   `python manage.py runscript importSecurityControlsFromWord(path\to\file.docx)`