from datetime import datetime
from typing import *

import pytz
from pydantic import EmailStr, Field

from data.enums.gender import GenderEnum
from .base import ExtendedBaseModel


class MinimumUserInfo(ExtendedBaseModel):
    email: EmailStr
    avatar: Optional[str]


class MinimumRequiredUserInfo(MinimumUserInfo):
    name: str = Field(..., min_length=3, max_length=50)
    last_name: Optional[str] = Field(None, alias='lastName', title='lastName')
    phone_number: str = Field(..., alias='phoneNumber', title='phoneNumber')
    gender: GenderEnum = GenderEnum.male


class UserInDatabase(MinimumRequiredUserInfo):
    user_id: Optional[int] = Field(None, alias='id', title='id')
    hashed_password: str = Field(...)
    created_at: datetime = datetime.now().replace(tzinfo=pytz.timezone('Asia/Tehran'))
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class LoginUserInput(MinimumUserInfo):
    password: str


class RegisterUserInput(MinimumRequiredUserInfo):
    password: str = Field(..., min_length=0, max_length=20)
    repeat_password: str = Field(..., alias='repeatPassword', title='repeatPassword')
