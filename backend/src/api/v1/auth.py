import json
from datetime import datetime, timedelta
import jwt
from urllib.parse import quote
from fastapi import APIRouter, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from src.config import configuration
from src.service import get_user_service

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id=configuration.auth.client_id,
    client_secret=configuration.auth.client_secret,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router_auth = APIRouter()

service = get_user_service()


@router_auth.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@router_auth.get('/login')
async def login(request: Request, return_to: str = Query("/")):
    # Сохраняем return_to в сессии
    request.session['return_to'] = return_to

    redirect_uri = 'http://econ-battle.ru/api/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_auth.get('/auth')
async def auth(request: Request):
    # Получаем return_to из сессии
    return_to = request.session.get('return_to', '/')

    # Очищаем сессию
    if 'return_to' in request.session:
        del request.session['return_to']

    # Остальной код остается прежним...
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    user = token.get('userinfo')
    if not user:
        return RedirectResponse(url='/')

    user_data = dict(user)
    request.session['user'] = user_data

    # Получаем/создаем пользователя в БД
    user_info = await service.get_user(user_id=user_data.get("sub"))
    if not user_info:
        await service.create_user(
            user_id=user_data.get("sub"),
            username=user_data.get("name"),
            picture=user_data.get("picture")
        )

    # Генерируем JWT с данными пользователя
    user_payload = {
        "sub": user_data.get("sub"),
        "name": user_data.get("name"),
        "picture": user_data.get("picture"),
        "exp": datetime.now() + timedelta(seconds=10)
    }
    user_jwt = jwt.encode(
        user_payload,
        configuration.auth.JWT_SECRET,
        algorithm=configuration.auth.JWT_ALGORITHM
    )
    user_jwt_quoted = quote(user_jwt)

    return_path_quoted = quote(return_to)

    return RedirectResponse(
        url=f"http://frontend:5173/auth-callback?user={user_jwt_quoted}&return_to={return_path_quoted}"
    )


@router_auth.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')