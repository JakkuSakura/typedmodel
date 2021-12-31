import pytest
from typedmodel.utils import TypeException, MissingArgumentException, ExtraArgumentException

from typedmodel import BaseModel


def test_base_model_type_checking():
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
    class Foo(BaseModel):
        def foo(self, s: str) -> int:
            return int(s)

    with pytest.raises(TypeException):
        foo = Foo()
        foo.foo(1)


def test_base_class_classmethod():
    import beartype
    class Bar:
        @beartype.beartype
        @classmethod
        def foo(cls, s: str) -> int:
            return int(s)

    class Foo(BaseModel):
        @classmethod
        def foo(cls, s: str) -> int:
            return int(s)

    with pytest.raises(TypeException):
        Foo.foo(1)


def test_inheritance():
    class Foo(BaseModel):
        foo: str = 'test'

    class Bar(Foo):
        bar: int

    assert Bar._keys() == {'foo', 'bar'}
    Bar(bar=1)
    Bar(bar=1, foo='foo')
    assert Bar._can_be_set('foo')


def test_inheritance2():
    class Foo(BaseModel):
        foo: str

    class Bar(Foo):
        bar: int

    assert Bar._can_be_set('foo')
    Bar(bar=1, foo='foo')
