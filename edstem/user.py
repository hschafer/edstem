from typing import Any, NotRequired, Optional, TypedDict

import edstem._base as base
from edstem.ed_api import EdStemAPI


class UserData(TypedDict):
    id: base.UserID
    name: str
    email: str
    role: str
    tutorial: str | None
    accepted: bool
    source_id: NotRequired[str]


class User(base.EdObject[base.UserID]):
    _data: dict[str, Any]

    def __init__(
        self,
        name: str,
        id: base.UserID,
        email: str,
        role: str,
        tutorial: Optional[str] = None,
        accepted: bool = False,
        source_id: str = "",
        **kwargs,
    ) -> None:
        # Currently left out: username, lab_id, lti_synced
        super().__init__(name, id, **kwargs)
        self._data: UserData = {
            "id": id,
            "name": name,
            "email": email,
            "role": role,
            "tutorial": tutorial,
            "accepted": accepted,
            "source_id": source_id,
        }

    @staticmethod
    def from_dict(data: base.JSON) -> "User":
        base._proper_keys(data, UserData)
        return User(**data)

    # TODO Set name, email, role?

    @property
    def id(self) -> base.UserID:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @name.setter
    def name(self, value: str) -> None:
        self._changes.add("name")
        self._data["name"] = value

    @property
    def email(self) -> str:
        return self._data["name"]

    @property
    def role(self) -> str:
        return self._data["role"]

    @role.setter
    def role(self, value: str) -> None:
        self._changes.add("role")
        self._data["role"] = value

    @property
    def tutorial(self) -> str | None:
        return self._data["tutorial"]

    @tutorial.setter
    def tutorial(self, value: str | None) -> None:
        self._changes.add("tutorial")
        self._data["tutorial"] = value

    @property
    def accepted(self) -> bool:
        return self._data["accepted"]

    @property
    def source_id(self) -> str:
        return self._data["source_id"]

    def _tuple(self) -> tuple:
        return (
            self._name,
            self._id,
            self.email,
            self.role,
            self.tutorial,
            self.accepted,
            self.source_id,
        )

    def __repr__(self) -> str:
        return f"User(id={self._id}, name={self._name})"

    # API Methods
    @staticmethod
    def get_all_users(course_id: base.CourseID) -> list["User"]:
        api = EdStemAPI()
        users = api.get_all_users(course_id)
        return [User.from_dict(u) for u in users]

    @staticmethod
    def get_user(course_id: base.CourseID, id_or_name: base.UserID | str) -> "User":
        users = User.get_all_users(course_id)
        return base.EdObject._filter_single_id_or_name(users, id_or_name)
