FROM python:3
# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN touch db.sqlite3
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py runscript scripts.ssp_all_data_2020_10_01 -v2


EXPOSE 8000

CMD ["python", "python manage.py runserver 0.0.0.0:8000"]