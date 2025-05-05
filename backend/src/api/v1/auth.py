import json

import httpx
from fastapi import APIRouter, Header, HTTPException, Depends
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from src.config import configuration

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(config=Config(env_file='../../../.env'))
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router_user = APIRouter(
    tags=['user'],
    prefix='/user'
)

@router_user.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/user/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/user/login">login</a>')

@router_user.get('/login')
async def login(request: Request):
    redirect_uri = 'http://localhost:8000/user/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_user.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/user/')


@router_user.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/user/')



# from authlib.jose import jwt
#
#
# def verify_google_token(token: str) -> dict:
#     # Получаем ключи валидации от Google
#     resp = httpx.get('https://www.googleapis.com/oauth2/v3/certs')
#     public_key = jwt.PyJWKClient(resp.json()).get_signing_key_from_jwt(token)
#
#     # Валидация токена
#     claims = jwt.decode(
#         token,
#         public_key.key,
#         claims_options={
#             "iss": {"essential": True, "values": ["https://accounts.google.com"]},
#             "aud": {"essential": True, "value": configuration.auth.client_id},
#             "exp": {"essential": True}
#         }
#     )
#     return claims.validate()
#
# async def get_current_user(token: str = Header(..., alias="Authorization")) -> User:
#     try:
#         token = token.replace("Bearer ", "")
#         claims = verify_google_token(token)
#         user = await db.get(User, id=claims["sub"])
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid token")
#
# @router_auth.get("/me")
# async def user_profile(user: User = Depends(get_current_user)):
#     return user
#
#
# @router_auth.get('/auth')
# async def auth(request: Request):
#     # ... предыдущий код ...
#     user_data = dict(user)
#
#     # Сохраняем/обновляем пользователя в БД
#     user = await db.get(User, id=user_data['sub'])
#     if not user:
#         user = User(
#             id=user_data['sub'],
#             email=user_data['email'],
#             name=user_data['name'],
#             picture=user_data.get('picture')
#         )
#         await db.add(user)
#     else:
#         user.last_login = datetime.now()
#         await db.commit()
#
#     return RedirectResponse(url='/')