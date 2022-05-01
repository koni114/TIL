import uvicorn
from typing import List

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class SomeError(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f"<{self.name}> is occured. code: <{self.code}>"


users = {
    1: {"name": "Fast"},
    2: {"name": "Campus"},
    3: {"name": "API"}
}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"<User: {user_id}> is not exists",
        )
    return users[user_id]


# @app.exception_handler(SomeError)
# async def some_error_handler(request: Request, exc: SomeError):
#     return JSONResponse(
#         content={"message": f"error is {exc.name}"}, status_code=exc.code
#     )


@app.get("/error")
async def get_error():
    raise SomeError("Hello", 500)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
