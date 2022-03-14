# Rango
A simple app where user can see total views of categories,
create pages within them and like the most interesting ones.
Simple search and category filtering are also included.

## Installation:
1. Clone the repository:
```
git clone https://github.com/Techinek/rango.git
```

2. Install all the needed packages:
```
pip install -r reqs.txt
```
3. Make migrations:
```
python manage.py makemigrations и $ python manage.py migrate
```
4. After making migrations run the following script to generate
categories and pages:
```
python populate_rango.py
```
5. Finally run local server:
```
python manage.py runserver
```
###### This is the pet project of the book Tango With Django 2 by Leif Azzopardi and David Maxwel.

