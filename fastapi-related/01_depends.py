from base64 import b64encode
from fastapi import Depends,Path,Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional,Union
from uuid import UUID,uuid4
import re
import os
from datetime import timedelta
from jose import jwt,ExpiredSignatureError 
from pydantic import networks,BaseModel


sample=uuid4()

CHANNEL_TOKEN_KEY_PREFIX = "tk_"
CHANNEL_REFRESH_TOKEN_KEY_PREFIX = "rtk_"

def get_channel_token_key(channel_id: Union[UUID, str]):
    return CHANNEL_TOKEN_KEY_PREFIX + str(channel_id)

class EndUserValidJWTHeaderOrCookie(OAuth2PasswordBearer):

    #Overriding
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if authorization is None or authorization.split() or authorization.split()[1] == "undefined":
            channel_token_pattern = re.compile('/channels/([^/]+)/') # Any occurrence of any character EXCEPT a, b, c, d. 
            try:
                channel_id = channel_token_pattern.search(str(request.url)).group(1)
            except AttributeError: #If not matched, you can do call group() method
                raise Exception(message="doesn't not found token")
            channel_token_key = get_channel_token_key(channel_id) #To prefix channel id
            if channel_token_key in request.cookies: #If tk_something is in cookies
                authorization = f"bearer {request.cookies[channel_token_key]}"
            if not authorization:
                raise Exception(message="doesn't not found token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer": 
            if self.auto_error:
                raise Exception(message="doesn't not found token")
            else:
                return None
        return param

API_V1_TOKEN_URL: str = os.getenv("API_V1_TOKEN_URL", "")
enduer_auth_schem = EndUserValidJWTHeaderOrCookie(tokenUrl=f"{API_V1_TOKEN_URL}") 
#OAuth2PasswordBearer takes tokenUrl parameter -> OAuthFlow - tokenUrl, scope


JWT_AUTH = {
    "SECRET_KEY": b64encode( os.getenv("SECRET_KEY", "")).decode(),
    "PUBLIC_KEY": None,
    "PRIVATE_KEY": None,
    "ALGORITHM": "HS256",
    "AUTHORIZATION_TYPE": "Bearer",
    "VERIFY": True,
    "VERIFY_EXPIRATION": True,
    "EXPIRATION_DELTA": timedelta(minutes=30),
    "REFRESH_EXPIRATION_DELTA": timedelta(days=15),
    "ALLOW_REFRESH": True,
}

class ValidateJWTToken:
    def __init__(self, jwt_auth_secret_key: str, token: str, channel_id: Union[UUID, str] = None):
        self.jwt_auth_secret_key = jwt_auth_secret_key
        self.token = token
        self.channel_id = channel_id

    def decode_token_or_raise_exception(self) -> dict:
        try:
            decoded_data = jwt.decode(self.token, key=self.jwt_auth_secret_key)
            if decoded_data.get('channel_id') and not self.channel_id:
                raise Exception(message="doesn't not found token")
            if decoded_data.get('channel_id') != self.channel_id:
                raise Exception(message="doesn't not found token")
            return decoded_data
        except ExpiredSignatureError:
            raise Exception(message="token is expired.")
        except Exception as e:
            raise Exception(message="token is invalid.")

    def get_user_id(self) -> str:
        return self.decode_token_or_raise_exception().get('sub')


class UserTypeEnum(StringEnum):
    BACK_OFFICE_USER = "back_office_user"
    BMW_CUSTOMER = "bmw_customer"
    CUSTOMER = "customer"

class TokenPayload(BaseModel):
    sub: UUID
    exp: int
    iat: int
    jti: UUID
    user_type: UserTypeEnum

class CustomerTokenPayload(TokenPayload):
    channel_id: UUID
    email: Optional[networks.EmailStr]
    nickname: str

def get_customer_data(token: str = Depends(enduer_auth_schem), channel_id : str = Path(...)) -> CustomerTokenPayload:
    token_data = ValidateJWTToken(token=token,channel_id=channel_id, jwt_auth_secret_key=JWT_AUTH['SECRET_KEY']).decode_token_or_raise_exception()
    return token_data

# def get_customer_date(channel_id : str = Path(..., example=str(sample))):

#     token_date = ValidateJWTToken(token=token,channel_id=channel_id, jwt_auth_secret_key=settings.JWT_AUTH['SECRET_KEY']).decode_token_or_raise_exception()

def get_customer_id(customer_data:dict = Depends(get_customer_data)) -> UUID:
    return customer_data["sub"]