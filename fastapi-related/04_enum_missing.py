from typing import Any
from enum import Enum,EnumMeta

class DefaultEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultEnumMeta.default:
            # Assume the first enum is default
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)

class MyString(Enum,metaclass=DefaultEnumMeta):
    A = "A"
    B = "B"
    C = "C"

    @classmethod
    def _missing_(cls, value):
        return cls.A

    
print(MyString())