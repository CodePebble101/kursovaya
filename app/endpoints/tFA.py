from fastapi import FastAPI, Form, Request, Depends, HTTPException, status, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import pyotp
import redis

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from app.config.config import RedisSettings
from app.scripts.otp import verify_otp, generate_otp
from app.scripts.register import get_register_data_from_mongo
from app.scripts.mail import send_email

redis_client = redis.StrictRedis(host=RedisSettings.REDIS_HOST, port=RedisSettings.REDIS_PORT, db=0)
tfa_router = APIRouter(
    prefix='/tfa',
    tags=["2FA"],
)

templates = Jinja2Templates(directory="app/templates")
user_secrets = {}


@tfa_router.post(path="/verify-otp/{username}")
async def verify_one_time_password(username: str, otp: str = Form(...)):
    if await verify_otp(username, otp):
        return {"message": "Verification successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")


@tfa_router.get(path="/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Страница верификации одноразового пароля
@tfa_router.post(path="/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_exist = await get_register_data_from_mongo(request=request, username=username)
    if not user_exist:
        raise HTTPException(status_code=400, detail="LOGIN_BAD_CREDENTIALS")
    if username != user_exist.get('username') or password != user_exist.get('password'):
        raise HTTPException(status_code=400, detail="LOGIN_BAD_CREDENTIALS")

    otp = await generate_otp(username)
    print(otp)
    send_email.delay([username], subject="Одноразовый код",
                     content=f"Ваш код для входа в систему: {otp} \n ВНИМАНИЕ! Данный код действителен на протяжении 5 минут")

    return templates.TemplateResponse("verify.html", {"request": request, "username": username})
