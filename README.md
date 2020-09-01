# content_management_system
create virtual environment by using below command
"python3 -m venv env"
Activate virtual environment
"source env/bin/activate"
install all required packages in virtual environment by using below command
"pip install -r requirements.txt"
To start the server use below command
"python manage.py runserver"

you can check all the urls by using below postman url
https://www.getpostman.com/collections/67cbe7809f893e7d3040


you can create admin user by using below procedure
start the shell session by using below command
"python manage.py shell"

import user model from file
"from authentication.models import User"

create user
"user = User.objects.create(email="amittambe2233@gmail.com", full_name="Amit Tambe", pin_code=410206, is_staff=True, phone_number=7039872034)"
set password
"user.set_password("Amit")"
"user.save()"


