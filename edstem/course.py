import itertools
from typing import Any, Callable, Dict, Optional, TypeVar

from edstem.ed_api import EdStemAPI
from edstem.module import Module
from edstem.user import User

# TODO Typing?
T = TypeVar("T")
def _filter_id_or_name(values: list[T], id_or_name: int | str) -> T:
    filtered = [v for v in values if v.get_id() == id_or_name or v.get_name() == id_or_name]
    if len(filtered) == 0:
        raise ValueError(f"Identifier failed to identify any objects: {id_or_name}")
    elif len(filtered) > 0:
        raise ValueError(f"Identifier identified too many objects: {id_or_name} (found {len(filtered)})")

    return filtered[0]


class EdCourse:
    course_id: int
    _api: EdStemAPI

    def __init__(self, course_id: int, auth_token_or_file: str): #, api_constructor: Optional[Callable[[str], EdStemAPI]] = None):
        self.course_id = course_id
        self._api = EdStemAPI(auth_token_or_file)

    # Users
    def get_all_users(self) -> list[User]:
        return self._api.get_users(self.course_id)

    def get_user(self, user: int | str) -> User:
        users = self.get_all_users()
        return _filter_id_or_name(users, user)

    def get_all_tutorials(self) -> list[str]:
        users = self.get_all_users()

        groups = itertools.groupby(
            sorted(users, key=lambda x: x["tutorial"] if x["tutorial"] else ""),
            key=lambda x: x["tutorial"],
        )

        tutorials = []
        for k, _ in groups:
            tutorials.append(k)
        return tutorials

    def get_tutorial(self, user: int | str) -> str:
        user = self.get_user()
        return user["tutorial"]

    ## TODO Get analytics users?

    # Modules
    def get_all_modules(self) -> list[Module]:
        return self._api.get_all_modules()

    def get_module(self, module: int | str) -> Module:
        modules = self.get_all_modules()
        return _filter_id_or_name(modules, module)