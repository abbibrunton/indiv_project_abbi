#! /bin/sh
# check the database available
while ! nc -z mysql 3306; do echo "waiting for db..."; sleep 1; done
# run the create scripts
python create.py
# run the application
python run.py
