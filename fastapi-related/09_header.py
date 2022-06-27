from fastapi import FastAPI, Header
import uvicorn

app = FastAPI()

@app.post("/whatever")
def header_test(x_unsigned_secret_key:str | None = Header(None)):
    return x_unsigned_secret_key



if __name__ == "__main__":
    uvicorn.run(app)