from typing import Any, NewType

CourseID = NewType("CourseID", int)


class Foo:
    data: dict[str, Any]

    def __init__(self):
        self.data = {"a": 1, "b": 2}

    @property
    def foo(self) -> CourseID:
        return self.data["a"]

    @foo.setter
    def foo(self, _):
        raise NotImplementedError


f = Foo()
print(f.foo)
print(getattr(f, "foo"))
f.foo = 3
