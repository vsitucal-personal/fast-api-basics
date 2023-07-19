from typing import Union

from pydantic import BaseModel, Field


class LoginCreds(BaseModel):
    username: str
    password: str


class PersonModelWithFields(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default="Person", title="description of this person", max_length=10,
    )
    age: float = Field(ge=0, description="age must be greater than or equal to zero")


class MultiParam(BaseModel):
    person: PersonModelWithFields
    creds: LoginCreds


class NestedPersonWithCreds(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default="Person", title="description of this person", max_length=10,
    )
    age: float = Field(ge=0, description="age must be greater than or equal to zero")
    creds: Union[LoginCreds, None]


