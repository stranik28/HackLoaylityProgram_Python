from typing import Optional

from api.request.base import RequestBase

from pydantic import Field


class RequestRegistration(RequestBase):
    username: str = Field(..., examples=['oleg_Jovanovich'])
    password: str = Field(..., example='<PASSWORD>')
    role: str = Field(..., example='admin')
