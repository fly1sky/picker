# Picker
----

## Installation

### Prerequisites
- [Python](https://www.python.org/downloads/)  3.8.7 
This is what I'm using, maybe a little lower version also works.

#### Step by step
0. Clone the project.
```
$ git clone https://github.com/fly1sky/picker.git
$ cd picker
```
1. Install some dependencies.
```
$ pip3 install -r requirements.txt
```
2. Create migrations for user app.
```
$ python manage.py makemigrations user
```
3. Apply migrations to the database. 
```
$ python manage.py migrate
```
4. Create a user who can login to the admin site.
```
$ python manage.py createsuperuser
```
5. Just run it. 
```
$ python manage.py runserver
```
PS: http://127.0.0.1:8000/admin/ is a good startpoint to explore.
