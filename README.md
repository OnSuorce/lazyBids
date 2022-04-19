# lazyBids
Simple REST API of an online service where users auction their items and other users can send their bids

# Goal
The goal of this project is to train myself on Django REST Framework and to have a starting point for my (eventual) future projects in Django as i won't be able to use it on work. Therefore i tried my best in implementing different solutins and documenting almost anything that's worth documenting

<p align="center">
  <img src="https://www.django-rest-framework.org/img/logo.png" alt="logo"/>
</p>


# Setup

Once the project is cloned create a virtual environment

```bash
cd lazyBids
python3 -m venv env
source env/bin/activate 
```

install the dependencies using the requirements.txt

```bash
pip3 install -r requirements.txt
```
Make migrations and create super user (not mandatory but useful for testing and developing)
```bash
cd lazyBids
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```
Run the server

```bash
python3 manage.py runserver
```

