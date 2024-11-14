https://eduportal-beta.vercel.app/

virutualenv venv
pip install django     


django-admin startproject eduportal .

python manage.py migrate
python manage.py runserver

python manage.py createsuperuser
