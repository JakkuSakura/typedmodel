import beartype

from compat import *
from utils import *


class MetaClass(type):
    def __new__(cls, name, bases, attr):
        # Replace each function with type checked one
        for name, value in attr.items():
            if not name.startswith("_") and type(value) is FunctionType or type(value) is MethodType:
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

    def _keys(self):
        keys = set(hasattr(self, "__annotations__") and self.__annotations__.keys() or [])
        for key, value in type(self).__dict__.items():
            if not key.startswith("_") and not isinstance(value, Callable):
                keys.add(key)
        return keys

    def _has_default(self, key: str):
        return key in type(self).__dict__

    def _get_default(self, key: str):
        import copy
        return copy.copy(type(self).__dict__.get(key))

    def _can_be_set(self, key: str):
        return self._get_annotation(key) or hasattr(type(self), key)

    def _get_annotation(self, key: str):
        if hasattr(self, "__annotations__"):
            return self.__annotations__.get(key)

    def __setattr__(self, key, value):
        annotation = self._get_annotation(key) or Any
        check_pep_type_raise_exception(value, annotation)
        object.__setattr__(self, key, value)


def test_base_model_type_checking():
    import pytest

    class Foo(BaseModel):
        a: str
        b: str
        d = 'default'
        e: str = 'default'

    foo = Foo(a='test', b='test')
    assert foo.d == 'default'
    assert foo.e == 'default'
    with pytest.raises(TypeException):
        Foo(a=1, b=2)

    with pytest.raises(ExtraArgumentException):
        # it should fail due to extra argument 'c'
        Foo(a='test', b='test', c='test')

    with pytest.raises(MissingArgumentException):
        Foo(a='test')


def test_base_class_typed_function_call():
    import pytest
    class Foo(BaseModel):
        def foo(self, s: str) -> int:
            return int(s)

    with pytest.raises(TypeException):
        foo = Foo()
        foo.foo(1)
