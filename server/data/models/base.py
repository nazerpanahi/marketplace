from datetime import datetime
from itertools import starmap
from typing import *

from pydantic import BaseModel


class ExtendedBaseModel(BaseModel):
    def serialize(self, **kwargs):
        def _serializer(value: Any):
            if isinstance(value, datetime):
                return value.isoformat()
            return value

        return dict(starmap(lambda k, v: (k, _serializer(v)), self.dict(**kwargs).items()))
