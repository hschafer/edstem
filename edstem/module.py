from datetime import datetime
from typing import Any, Iterable, NotRequired, TypedDict

import edstem._base as base
from edstem.ed_api import EdStemAPI
from edstem.lesson import Lesson


# Not used explicitly because mypy is too strict, but good documentation for the expected keys to/from Ed
class ModuleData(TypedDict):
    id: base.ModuleID
    name: str
    course_id: base.CourseID
    user_id: base.UserID
    created_at: str | None
    updated_at: NotRequired[str | None]


class Module(base.EdObject[base.ModuleID]):
    _data: dict[str, Any]

    def __init__(
        self,
        id: base.ModuleID,
        name: str,
        course_id: base.CourseID,
        creator_id: base.UserID,
        created_at: str | None,  # TODO datetime input?
        updated_at: str | None,  # TODO datetime input?
        timezone: str | None = None,
    ) -> None:
        super().__init__(name, id)
        # Currently left out: updated_at (assumed always null?)
        self._data: ModuleData = {
            "id": id,
            "name": name,
            "course_id": course_id,
            "user_id": creator_id,
            "created_at": created_at,
            "updated_at": updated_at,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Module":
        base._proper_keys(data, ModuleData)
        rename_data = base._rename_dict(data, [("user_id", "creator_id")])  # type: ignore
        return Module(**rename_data)

    @property
    def id(self) -> base.ModuleID:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @name.setter
    def name(self, value: str) -> None:
        self._changes.add("name")
        self._data["name"] = value

    @property
    def course_id(self) -> base.CourseID:
        return self._data["course_id"]

    @property
    def creator_id(self) -> base.UserID:
        return self._data["user_id"]

    @property
    def created_at(self) -> datetime | None:
        # Cache?
        return Module.str_to_datetime(self._data["created_at"])

    def _tuple(self) -> tuple:
        return (
            self.name,
            self.id,
            self.creator_id,
            self.created_at,
        )

    def __repr__(self) -> str:
        return f"Module(id={self.id}, name={self.name})"

    # API Methods
    @staticmethod
    def get_all_modules(course_id: base.CourseID) -> list["Module"]:
        api = EdStemAPI()
        modules = api.get_all_modules(course_id)
        return [Module.from_dict(m) for m in modules]

    @staticmethod
    def get_module(
        course_id: base.CourseID, id_or_name: base.ModuleID | str
    ) -> "Module":
        modules = Module.get_all_modules(course_id)
        return Module._filter_single_id_or_name(modules, id_or_name)  # type: ignore

    def get_lessons(self) -> list[Lesson]:
        lessons = Lesson.get_all_lessons(self.course_id)
        return [lesson for lesson in lessons if lesson.get_module_id() == self.id]

    def get_lesson(self, id_or_name: base.LessonID | str) -> Lesson:
        lessons = self.get_lessons()
        return Module._filter_single_id_or_name(lessons, id_or_name)  # type: ignore

    def _to_dict(self, changes_only=True) -> dict[str, Any]:
        data: dict[str, Any]
        if changes_only:
            data = {k: self._data[k] for k in self._changes}
        else:
            data = self._data
        return data

    def post_changes(self, ignore_errors: bool = False) -> bool:
        try:
            module_data = self._to_dict(changes_only=True)
            module_data = self._api.edit_module(self.course_id, self.id, module_data)
            self.__dict__.update(module_data)
            return True
        except Exception as e:
            if ignore_errors:
                return False
            else:
                raise e
