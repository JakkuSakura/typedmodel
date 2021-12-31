import beartype

from .compat import *
from .utils import *


class MetaClass(type):
    def __new__(cls, name, bases, attr):
        # Replace each function with type checked one
        for name, value in attr.items():
            if not name.startswith("_") and (type(value) is FunctionType or type(value) is MethodType):
                    # FIXME: classmethod is not type checked isinstance(value, classmethod) due to problem with:

                attr[name] = my_beartype(value)

        return super(MetaClass, cls).__new__(cls, name, bases, attr)


class BaseModel(metaclass=MetaClass):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if self._can_be_set(key):
                self.__setattr__(key, val)
            else:
                raise ExtraArgumentException(f"`{key}` is the extra argument and cannot be set")
        for key in self._keys():
            if key not in self.__dict__:
                if self._has_default(key):
                    self.__setattr__(key, self._get_default(key))
                else:
                    raise MissingArgumentException(f"`{key}` is the missing argument and doesn't have a default value")

    @classmethod
    def _keys(cls):
        keys = set(hasattr(cls, "__annotations__") and cls.__annotations__.keys() or [])
        for key, value in cls.__dict__.items():
            if not key.startswith("_") and not isinstance(value, Callable) and not isinstance(value, classmethod):
                keys.add(key)
        if issubclass(cls.__base__, BaseModel):
            keys.update(cls.__base__._keys())
        return keys

    @classmethod
    def _has_default(cls, key: str):
        return key in cls.__dict__

    @classmethod
    def _get_default(cls, key: str):
        import copy
        return copy.copy(cls.__dict__.get(key))

    @classmethod
    def _can_be_set(cls, key: str):
        return cls._get_annotation(key) or hasattr(cls, key)

    @classmethod
    def _get_annotation(cls, key: str):
        if hasattr(cls, "__annotations__"):
            return cls.__annotations__.get(key)

    def __setattr__(self, key, value):
        annotation = type(self)._get_annotation(key) or Any
        check_pep_type_raise_exception(value, annotation)
        object.__setattr__(self, key, value)
