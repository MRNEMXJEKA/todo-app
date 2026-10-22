from pydantic import BaseModel, ConfigDict


# ---------- Задачи ----------

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # собирать схему из ORM-объекта

    id: str
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


# ---------- Категории ----------

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None
