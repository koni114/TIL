from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3']
}

user = User(** external_data)
print(f"user.id --> {user.id}")
print(f"user.signup_ts --> {user.signup_ts}")
print(f"user.friends   --> {user.friends}")
print(user.dict())


