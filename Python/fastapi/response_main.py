from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn


app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title="이름")
    price: float = Field(None, ge=0)
    amount: int = Field(
        default=1,
        gt=0,
        le=100,
        title="수량",
        description="아이템 갯수. 1~100 개 까지 소지 가능",
    )


@app.post("/users/{user_id}/item")
def create_item(item: Item):
    return item


if __name__ == "__main__":
    uvicorn.run("response_main:app", reload=True)
