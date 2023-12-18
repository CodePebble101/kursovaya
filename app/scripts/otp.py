import pyotp

import redis
from app.config.config import RedisSettings


redis_client = redis.StrictRedis(host=RedisSettings.REDIS_HOST, port=RedisSettings.REDIS_PORT, db=0)
async def generate_otp(username: str) -> str:
    otp_secret = pyotp.random_base32()
    redis_client.setex(name=username, time=300, value=otp_secret)
    totp = pyotp.TOTP(otp_secret, interval=300)
    return totp.now()


async def verify_otp(username: str, otp: str) -> bool:
    users_otp = redis_client.get(username)
    if users_otp:
        totp = pyotp.TOTP(users_otp, interval=300)
        return totp.verify(otp)
    return False
