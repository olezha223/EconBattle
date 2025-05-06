import json
from fastapi import APIRouter, Header, HTTPException, Depends
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from src.config import configuration
from src.service import get_user_service

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(config=Config(env_file='.env'))
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router_user = APIRouter()

service = get_user_service()

@router_user.get('/')
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


@router_user.get('/login')
async def login(request: Request):
    redirect_uri = 'http://localhost:8000/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_user.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    # получить информацию о юзере
    if user:
        request.session['user'] = dict(user)
        user_info = await service.get_user(user_id=user.get("sub"))
        if not user_info:
            await service.create_user(user_id=user.get("sub"), username=user.get("name"))
    return RedirectResponse(url='/')


@router_user.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')