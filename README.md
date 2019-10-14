# Survey_APIs
Survey_APIs implemented in Flask

## Prerequisites (Used Technologies)

* Python 3.6.8 or above
* Flask 1.1.1


## Installing

1- Navigate to the project directory

2- Run `pip3 install -r requirements.txt` in your terminal window to get all necessary packages installed.

3- Run the Flask server using:
```
        python3 application.py
```

## APIs reference
1- Register (POST: http://127.0.0.1:5000/Register)
```
    request body(ex.):
    {
        "username": "username",
        "password": "password",
        "password_confirm": "password"
    }

```

2- Login (POST: http://127.0.0.1:5000/Login)
```
    request body(ex.):
    {
        "username": "username",
        "password": "password"
    }

```

3- Get All surveys (GET: http://127.0.0.1:5000/survey)

4- Add a Survey (POST: http://127.0.0.1:5000/survey)
```
    request body(ex.):
    {
        "name": "First Survey",
        "description": "This is the First Survey",
        "questions": [
            {
                "body": "What is your name?",
                "note": "required"
            },
            {
                "body": "How old are you?",
                "note": "required"
            },
            {
                "body": "what is your nationality?",
                "note": "optional"
            }
        ],
        "start_data": "02/08/2019 00:22",
        "end_data": "01/01/2020 22:22"
    }

```