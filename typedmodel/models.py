import copy

from .utils import *


class MetaClass(type):
    def __new__(mcs, name, bases, attr):
        # Replace each function with type checked one
        for key, value in attr.items():
            if not key.startswith("_"):
                if type(value) is FunctionType:
                    attr[key] = my_beartype(value)
                elif isinstance(value, classmethod):
                    attr[key] = classmethod(my_beartype(value.__func__))
                elif isinstance(value, staticmethod):
                    attr[key] = staticmethod(my_beartype(value.__func__))
                # elif isinstance(value, property):

        return super(MetaClass, mcs).__new__(mcs, name, bases, attr)


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
        if key in cls.__dict__:
            return True
        elif issubclass(cls.__base__, BaseModel):
            return cls.__base__._has_default(key)
        else:
            return False

    @classmethod
    def _get_default(cls, key: str):
        if key in cls.__dict__:
            return copy.copy(cls.__dict__.get(key))
        elif issubclass(cls.__base__, BaseModel):
            return cls.__base__._get_default(key)
        else:
            return None

    @classmethod
    def _can_be_set(cls, key: str):
        if cls._get_annotation(key) or hasattr(cls, key):
            return True
        elif issubclass(cls.__base__, BaseModel):
            return cls.__base__._can_be_set(key)
        else:
            return False

    @classmethod
    def _get_annotation(cls, key: str):
        if hasattr(cls, "__annotations__"):
            return cls.__annotations__.get(key)

    @classmethod
    def _get_value(cls, v, to_dict: bool):
        if not to_dict:
            return v

        if hasattr(v, 'dict'):
            return v.dict()

        if isinstance(v, dict):
            return {
                key: cls._get_value(val, to_dict=to_dict)
                for key, val in v.items()
            }
        if isinstance(v, list):
            return [
                cls._get_value(val, to_dict=to_dict) for val in v
            ]

        return v

    def dict(self) -> Dict[str, Any]:
        result = {}
        for key in self._keys():
            val = getattr(self, key)
            result[key] = type(self)._get_value(val, to_dict=True)
        return result

    def __setattr__(self, key, value):
        annotation = type(self)._get_annotation(key) or Any
        check_pep_type_raise_exception(value, annotation)
        object.__setattr__(self, key, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)
