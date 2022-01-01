# TypedModel

TypedModel aims to provide strict type checking for dataclass and pydantic model.

dataclass is useful, but provides no type checking

pydantic is useful, but sometimes it bugs out

https://github.com/samuelcolvin/pydantic/issues/3189

https://github.com/samuelcolvin/pydantic/issues/3569

## Usage

```shell
pip install typedmodel
```

```python3
from typedmodel import BaseModel


class Foo(BaseModel):
    a: str
    b: str
    d = 'default'
    e: str = 'default'


foo = Foo(a="a", b="b")

```
check `tests` for more use cases