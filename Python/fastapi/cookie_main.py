from fastapi import FastAPI, Cookie
import uvicorn


app = FastAPI()


@app.get("/cookie")
def get_cookies(ga: str = Cookie(None)):
    return {"ga": ga}


if __name__ == "__main__":
    uvicorn.run("cookie_main:app", reload=True)

