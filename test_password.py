from passlib.context import CryptContext
from fastapi import status 

#passwordhashing 
pwd_ctx = CryptContext(schemes=["bcrypt"])
def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password,hashed_password)


print(status.HTTP_200_OK)
print(status.HTTP_500_INTERNAL_SERVER_ERROR)
print(status.HTTP_422_UNPROCESSABLE_ENTITY)




