from .compat import *
from .exceptions import *


def check_pep_type(obj, annotation) -> bool:
    try:
        return check_pep_type_raise_exception(obj, annotation)
    except:
        return False


try:
    from beartype import is_bearable as check_pep_type_raise_exception
except ImportError:
    def check_pep_type_raise_exception(obj, annotation):
        import beartype.roar
        import beartype
        @beartype.beartype
        def check(o) -> annotation:
            return o

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

    def convert(*args, **kwargs):
        try:
            return enhanced(*args, **kwargs)
        except beartype.roar.BeartypeException as e:
            args = e.args[0]

        raise TypeException(args)

    return convert


def abstract(cls):
    old_init = cls.__init__

    def new_init(self, *args, **kwargs):
        if type(self) == cls:
            raise TypeError(f"{cls} is abstract and cannot be initialized here")
        old_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
