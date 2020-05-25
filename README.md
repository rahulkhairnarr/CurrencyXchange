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
● API to send money in a currency and receive the same in a different currency to another User
● API to identify avg Profit and loss for the money transferred
● API to average money transferred for every weekday
● Create a PDF and send it users on successful order placement 
● Setup Background Task Scheduler to send Monthly Statement

Documentation : https://documenter.getpostman.com/view/7846454/SztA78vU?version=latest#8ef74686-d32f-4802-b8e1-63d963ae315f


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

10. API to send money in a currency and receive the same in a different currency to another User
    - CLI: curl --location --request POST 'http://localhost:8000/api/transfer/' \
            --header 'Authorization: Token 072269a44c3f78470d14e55d89564641f4676c81' \
            --form 'receiver=admin' \
            --form 'amount=1'


11. API to identify avg Profit and loss for the money transferred
    - CLI: curl --location --request GET 'http://localhost:8000/api/get_pl_data/' \
            --header 'Authorization: Token 072269a44c3f78470d14e55d89564641f4676c81' \
            --form 'start_date=2020-05-01'


12. API to average money transferred for every weekday
    - CLI: curl --location --request GET 'http://localhost:8000/api/get_avg_tranfer/' \
            --header 'Authorization: Token 072269a44c3f78470d14e55d89564641f4676c81'