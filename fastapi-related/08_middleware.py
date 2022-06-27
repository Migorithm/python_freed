from fastapi import Request
from datetime import datetime, date, timedelta
import time

class D:
    def __init__(self, *args):
        self.utc_now = datetime.utcnow()
        self.timedelta = 0

    @classmethod
    def datetime(cls, diff: int=0) -> datetime:
        return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

    @classmethod
    def date(cls, diff: int=0) -> date:
        return cls.datetime(diff=diff).date()

    @classmethod
    def date_num(cls, diff: int=0) -> int:
        return int(cls.date(diff=diff).strftime('%Y%m%d'))


async def access_control(request:Request,call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None

    #If request doesn't go through LB, there is no x-forwared-for. 
    ip = request.headers["x-forwarded-for"] \
        if "x-forwarded-for" in request.headers.keys() \
        else request.client.host
    request.state.ip = ip.split(".")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies
    url = request.url.path

    # TODO URL pattern check
    try:
        if url.startswith("/api/v1/external/e"):
            if "authorization" in headers.keys():
                token_info = await token_decode(access_token=headers.get("Authorization"))
                request.state.user = UserToken(**token_info)
            else: # No token
                if "Authorization" not in headers.keys():
                    raise Exception
        response = await call_next(request) #execute endpoint function
    except Exception as e:
        error = await exception_handler(e)
    return response

async def exception_handler(error:Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error,detail=str(error))
    return error


async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload