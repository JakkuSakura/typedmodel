from .compat import *
from .exceptions import *
import functools

def check_pep_type(obj, annotation) -> bool:
    try:
        return check_pep_type_raise_exception(obj, annotation)
    except Exception as e:
        return False


try:
    from beartype import is_bearable as check_pep_type_raise_exception
except ImportError:
    def check_pep_type_raise_exception(obj, annotation):
        import beartype.roar
        import beartype
        import typing
        old_type_checking = typing.TYPE_CHECKING
        typing.TYPE_CHECKING = False
        @beartype.beartype
        def check(o) -> annotation:
            return o

        typing.TYPE_CHECKING = old_type_checking
        try:
            check(obj)
            reason = None
        except beartype.roar.BeartypeCallHintPepReturnException as e:
            reason = e.args[0].split('return ')[-1]
        if reason:
            raise TypeException(reason)
        return True


def my_beartype(func) -> Callable:
    import beartype
    import beartype.roar
    enhanced = beartype.beartype(func)

    @functools.wraps(func)
    def convert(*args, **kwargs):
        try:
            return enhanced(*args, **kwargs)
        except beartype.roar.BeartypeException as e:
            args = e.args[0]

        raise TypeException(args)
    return convert


def abstract(cls):
    old_init = cls.__init__

    @functools.wraps(old_init)
    def new_init(self, *args, **kwargs):
        if type(self) == cls:
            raise TypeError(f"{cls} is abstract and cannot be initialized here")
        old_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls

def reannotate(value):
    if type(value) is FunctionType:
        return my_beartype(value)
    elif isinstance(value, classmethod):
        return classmethod(my_beartype(value.__func__))
    elif isinstance(value, staticmethod):
        return staticmethod(my_beartype(value.__func__))
    else: # more missing
        return value
        