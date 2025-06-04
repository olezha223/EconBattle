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
async def login(request: Request, redirect_after: str = Query('/')):
    request.session['redirect_after'] = redirect_after
    redirect_uri = 'http://econ-battle.ru/api/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router_auth.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return RedirectResponse(url=f'http://econ-battle.ru/login?error={error.error}')

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
        redirect_after = request.session.get('redirect_after', '/')
        redirect_url = f'http://econ-battle.ru/auth-success?sub={user_data["sub"]}&name={user_data["name"]}&redirect={redirect_after}'
        # Перенаправляем на фронтенд с токеном в URL
        return RedirectResponse(url=redirect_url)

    return RedirectResponse(url='http://econ-battle.ru/login?error=AuthFailed')


@router_auth.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')