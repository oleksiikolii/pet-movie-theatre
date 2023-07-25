# Movie theatre
​
## Table of Contents
​
- [Description](#description)
- [Application functional](#functional)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Shutdown](#shutdown)
- [Accessing the Application](#accessing-the-application)

## Link to the project
[https://movie-theatre.onrender.com](https://movie-theatre.onrender.com)
​
## Description
​
Simple pet project of the Cinema. This web-site represents imaginary movie theatre which
shows some old, but gold movies such as "Showshank redemption" and the "Avatar" at the same time.
​
## Functional
* [Install project](#setup)
* Checkout some movies on the home page
* Login/Register
* Choose day in the sidebar
* Choose session below the title or on movie detail page
* Pick seats
* Click "Purchase tickets", don't be afraid they are free
* You can see your tickets on the "Your tickets" page
​
## Technologies
​
- [Django Official Documentation](https://docs.djangoproject.com/)
Django is a high-level Python Web framework. In this project, it's used to create the whole website including frontend side. This service builds the Django application and exposes it on port 8000.
​
​
## Prerequisites
​
1. Make sure you have Python installed on your system. To check that you can run in your terminal ```python --version```
​
## Setup
​
1. Clone the project:
```
git clone https://github.com/oleksiikolii/pet-movie-theatre
```
2. Navigate to the project directory:
```
cd pet-movie-theatre
```
3. Install and activate virtual environment:
```
python -m venv venv
```
Then
```
venv\Scripts\activate.bat
```
4. Install Django and requirements:
```
pip install -r requirements.txt
```
5. Create DataBase by running:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
6. Fill DB with data:
```
python manage.py loaddata fixtures/data.json
```
7. Run server:
```
python manage.py runserver
```

​

## Shutdown
​
1. To stop running app in your terminal press:
```
ctrl + c
```
​
## Accessing the Application
​
* The Django application is accessible at `http://127.0.0.1:8000/`
* The Admin page can be accessed at `http://127.0.0.1:8000/admin`
* To make changes in sessions and movies and get admin you can use login `admin.user` with `1qazcde3` password or you can create yours by running ```python manage.py createsuperuser```

