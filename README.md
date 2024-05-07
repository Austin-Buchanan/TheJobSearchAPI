# TheJobSearchAPI

## Description
This is TheJobSearchAPI, an API I'm using to track applications during my job search in 2024. It was developed in Python using the FastAPI framework with a PostgreSQL database.

## Motivation 
Early on in my job search, I was using Excel spreadsheets to track which jobs and companies I had applied to and what the status of my applications were. At this same time, I was learning more about Python back end development, so I thought it would be good practice to build a REST API in Python that somehow related to my job search. 

Since I found tracking my applications in an Excel workbook a little boring, I decided to build a REST API that could help replace the functionality of my workbook. That way, I could both get more practice building APIs in Python while also building something that I would frequently use. 

## Quick Start 
### Requirements 
This quick start guide assumes that you have Python and PostgreSQL installed on your computer. See the following links if you need help installing or setting up either of them.
Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
PostgreSQL: [https://www.postgresql.org/](https://www.postgresql.org/)
### Create a database in PostgreSQL called JobSearch.
No tables need to be created yet--just the database. Also, create a user that can create and edit tables within JobSearch. 
### Clone this repository. 
```Terminal with git 
git clone https://github.com/Austin-Buchanan/TheJobSearchAPI/
```
### Create a database.ini file within the repository directory.
Add the following contents to the file:
```
[postgresql]
host=localhost
database=JobSearch
user=<user>
password=<password>
```
Replace <user> and <password> with the username and password of a PostgreSQL user that has sufficient access to the JobSearch database to create and edit tables. 
### Install the Psycopg2 PostgreSQL database adapter for Python.
You can do this and later terminal commands from within a Python virtual environment made inside the repo directory if you want. 
```Terminal
pip install psycopg2
```
### Install FastAPI.
```Terminal
pip install fastapi
```
### Create tables.
The create_tables.py file in the repo will create the tables used by the API for you. 
```Terminal
py create_tables.py
```
### Run the server.
```Windows Terminal
uvicorn thejobsearch:app
```
or 
```Bash
fastapi run thejobsearch.py
```

