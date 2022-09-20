from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_login import LoginManager
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET = 'secret-key'
manager = LoginManager(SECRET, '/login')

DB = {
    'users': {
        'vasgan@mail.com': {
            'name': 'Vasgan',
            'password': 'vasgan'
        }
    }
}

@manager.user_loader()
def query_user(user_id: str):
    return DB['users'].get(user_id)

@app.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data = {'sub': email}
    )
    return {'access-token': access_token}

@app.get('/')
def hello():
    return 'Para usar la API dirigete a /login'