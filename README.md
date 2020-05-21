# Django REST API - CurrencyXchange

# Project Description
Following API has been create 
● User Auth API for SignUp
● User Auth API for SignIn (based on Signup password)
● API to Create User Balance / Wallet
● API to Read User Balance / Wallet
● API to Update User Balance / Wallet
● API to convert currency
● API to allow users to upload a profile photo.


# Instructions
1. To start the API
  - Open your terminal
  - $ sudo easy_install pip         # installs Pip package manager
  - $ pip install virtualenv				# Virtualenv is a tool to create isolated Python environments.
  - $ git clone https://github.com/rahulkhairnarr/CurrencyXchange.git
  - $ source env/bin/activate       # Launch the environment
  - $ cd CurrencyXchange                     # Browse into the project directory
  - $ python manage.py runserver    # Start the server
2. To be able to Install all required package through the terminal
  - $ pip install requirements.txt           # installs required package
3. API for user to get Token
    You need to generate token from admin credentials
  - CLI: curl --location --request POST 'http://localhost:8000/api/api-token-auth/' \
        --data-raw '{
            "username": "username",
            "password": "password"
            }'
4. API for user to Sign up 
  - CLI: curl --location --request POST 'http://localhost:8000/api/registration/' \
        --header 'Authorization: "Token " + {{API Token}}' \
        --data-raw '{
            "username": "username",
            "password": "password",
            "email": "email@eample.com"
            }'
4. API for user to login
  - CLI: curl --location --request POST 'http://localhost:8000/api/login/' \
        --header 'Authorization: "Token " + {{API Token}}' \
        --data-raw '{
            "username": "username",
            "password": "password",
            }'
5. API to Create User Balance / Wallet
    - CLI: curl --location --request GET 'http://localhost:8000/api/create_wallet/' \
            --header 'Authorization: "Token " + {{API Token}}' \

6. API to Read User Balance / Wallet
    - CLI: curl --location --request GET 'http://localhost:8000/api/get_balance/' \
            --header 'Authorization: "Token " + {{API Token}}' \

7. API to Update User Balance / Wallet
    - CLI: curl --location --request PUT 'http://localhost:8000/api/update_balance/' \
            --header 'Authorization: "Token " + {{API Token}}' \
            --data-raw '{
            "balance": {{amount}},
            }'

8. API to convert currency
    - CLI: curl --location --request POST 'http://localhost:8000/api/convert_currency/' \
            --header 'Authorization: "Token " + {{API Token}}' \
            --data-raw '{'from': 'usd',
            'to': 'inr',
            'amount': '10'
            }'

9. API to allow users to upload a profile photo.
    - CLI: curl --location --request POST 'http://localhost:8000/api/upload_photo/' \
            --header 'Authorization: "Token " + {{API Token}}' \
            --form '{{img}}'