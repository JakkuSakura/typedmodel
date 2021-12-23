import logging
import sys
from abc import *
from enum import Enum
from typing import (Any, Callable, Dict, Generic, Iterable, Iterator, List,
                    Optional, Set, Tuple, TypeVar, Union, cast)
from types import (FunctionType, MethodType)
# handle type annotation changes in PEP 3107, 484, 526, 544, 560, 563, 585
if sys.version_info >= (3, 8, 8):
    Dict = dict
    List = list
    Set = set
    Tuple = tuple
    import collections.abc

    Iterable = collections.abc.Iterable
    Iterator = collections.abc.Iterator
    if sys.version_info >= (3, 9, 2):
        Callable = collections.abc.Callable
    else:
        Callable = collections.abc.Callable
        logging.warning("collections.abc.Callable in Python 3.9.1 is broken")

