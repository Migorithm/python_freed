from pydantic import BaseSettings

class PostgreSQL(BaseSettings):
    # Postgres
    POSTGRES_SERVER:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_PORT:int

a = PostgreSQL()
print(a)

print("Dd")