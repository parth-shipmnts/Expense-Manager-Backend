# Expense-Manager-Backend

This web app allows user to manager simple day to day expenses.
`Backend` folder contains flask web app components. Structure for `Backend` folder is given below

```
|   startup.py              #start point of flask application
|
\---ExpenseManager          #Expense Manager package
    |   .gitignore
    |   auth_user.py        #logic to authorize users and their roles
    |   forms.py            #verify input given from client side
    |   models.py           #database models
    |   repository.py       #logic to store and get data from database
    |   seed_database.py    #initial seed data for database
    |   databaseconfig.py   #file to config database connections
    |   __init__.py
    |
    \---Views
            home.py         #for public access
            user.py         #for user only access
            __init__.py
```
### Api Documentation

**API BODY MUST HAVE JSON FORMAT WHEREVER NEEDED.**  
**AUTHORIZATION TOKEN WHICH YOU GET AFTER LOGIN MUST BE PASS AS AN AUTHORIZATION HEADER IN EACH REQUEST.**

`/api/v1/login`: Gets the authentication toke for the given email and password which are send in body.
```
{
    "email":"email of user",
    "password":"password of user"
}
```  
`/api/v1/register`: Register new user with following informations.
```
{
	"user_name": "username",
	"email": "user email",
	"password": "user password"
}
```  
`/api/v1/user/expense_details/<category_name>`: Gets expense details for specific user with optional category name filter. You can also send `start_date` and `end_date`with body of api as shown below with to further filter the results.
```
{
    "start_date": "2016-01-01",
    "end_date": "2016-05-01"
}
```
`/api/v1/user/categories`: Get all the categories that belongs to logged in user.

- GET API
- Requires Authorization Header.

`/api/v1/user/add_expense`: Add expense for logged in user.

- POST API
- Requires Authorization Header.

```
{
	"category": "Food",
	"amount": 190,
	"description": "Food"
}
```
`/api/v1/user/add_category`: Add new category for logged in user.

- POST API
- Requires Authorization Header.


```
{
	"name": "Movies"
}
```

**Tech used:**  
1. Flask
2. SQLAlchemy ORM
3. PostgresDB
4. Visual Studio Code IDE

**Check `requirements.txt` for python packages used**

**Installing Dependencies**

`pip install -r requirements.txt`

**Starting Server**

`python startup.py`
