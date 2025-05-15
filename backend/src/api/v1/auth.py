import json
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

@router_auth.post(
    path='/user',
)
async def create_new_user(
        user_id: str =  Query(..., title='User ID'),
        username: str = Query(..., title='Username'),
) -> None:
    return await service.create_user(user_id=user_id, username=username)

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
async def login(request: Request):
    redirect_uri = 'http://localhost:8000/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_auth.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    # получить информацию о юзере
    if user:
        user_data = dict(user)
        request.session['user'] = user_data
        user_info = await service.get_user(user_id=user_data.get("sub"))
        if not user_info:
            await service.create_user(
                user_id=user_data.get("sub"),
                username=user_data.get("name"),
                picture=user_data.get("picture")
            )
        # Отправляем данные пользователя в opener
        html = f"""
        <script>
            window.opener.postMessage({{
                user: {json.dumps(user_data)}
            }}, 'http://econ-battle.ru');
            window.close();
        </script>
        """
        return HTMLResponse(html)
    return RedirectResponse(url='/')


@router_auth.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')