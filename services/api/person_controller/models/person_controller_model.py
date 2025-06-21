from pydantic import BaseModel, RootModel
from typing import Optional, List

class User(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    secondName: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    money: Optional[float] = None


class PersonControllerModel(RootModel[List[User]]):
    pass
