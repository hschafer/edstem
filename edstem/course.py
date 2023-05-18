import itertools
from typing import Any, Optional, TypeVar

from edstem._base import *
from edstem.ed_api import EdStemAPI
from edstem.module import Module
from edstem.user import User

I = TypeVar("I", bound=int)
V = TypeVar("V", bound=EdObject)


def _filter_id_or_name(values: list[V], id_or_name: I | str) -> list[V]:
    return [v for v in values if v.get_id() == id_or_name or v.get_name() == id_or_name]


def _filter_single_id_or_name(values: list[V], id_or_name: I | str) -> V:
    filtered = _filter_id_or_name(values, id_or_name)
    if len(filtered) == 0:
        raise ValueError(f"Identifier failed to identify any objects: {id_or_name}")
    elif len(filtered) > 1:
        raise ValueError(
            f"Identifier identified too many objects: {id_or_name} (found {len(filtered)})"
        )
    return filtered[0]


class EdCourse(EdObject[CourseID]):
    course_id: int
    _api: EdStemAPI

    def __init__(
        self, course_id: CourseID
    ):  # , api_constructor: Optional[Callable[[str], EdStemAPI]] = None):
        self.course_id = course_id
        self._api = EdStemAPI()

    # Users
    def get_all_users(self) -> list[User]:
        return [User.from_dict(u) for u in self._api.get_users(self.course_id)]

    def get_user(self, user: UserID | str) -> User:
        users = self.get_all_users()
        return _filter_single_id_or_name(users, user)

    def get_all_tutorials(self) -> set[str]:
        users = self.get_all_users()

        # Annoying but helpful for typing
        def get_default(u: User) -> str:
            tutorial = u.get_tutorial()
            return "" if tutorial is None else tutorial

        return set(get_default(u) for u in users)

    def get_tutorial(self, id_or_name: UserID | str) -> Optional[str]:
        user = self.get_user(id_or_name)
        return user.get_tutorial()

    ## TODO Get analytics users?

    # Modules
    def get_all_modules(self) -> list[Module]:
        return [Module.from_dict(m) for m in self._api.get_all_modules()]

    def get_module(self, id_or_name: ModuleID | str) -> Module:
        modules = self.get_all_modules()
        return _filter_single_id_or_name(modules, id_or_name)
