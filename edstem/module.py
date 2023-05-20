from collections.abc import Iterable
from datetime import datetime
from typing import Optional

from edstem._base import *
from edstem.lesson import Lesson


class Module(EdObject[ModuleID]):
    course_id: CourseID
    creator_id: UserID
    created_at: datetime

    def __init__(
        self,
        name: str,
        id: ModuleID,
        course_id: CourseID,
        creator_id: UserID,
        created_at: datetime | str,
        timezone: Optional[str] = None,
        **kwargs,
    ) -> None:
        # Currently left out: updated_at (assumed always null?)
        super().__init__(name, id, **kwargs)
        self.course_id = course_id
        self.creator_id = creator_id

        if type(created_at) is str:
            self.created_at = EdObject.str_to_datetime(created_at, timezone)
        else:
            assert type(created_at) is datetime
            self.created_at = created_at

    @staticmethod
    def from_dict(data: JSON) -> "Module":
        data = dict(data)
        data["creator_id"] = data["user_id"]
        del data["user_id"]
        return Module(**data)

    def _to_dict(
        self, changes_only: bool = False, rename_ed: bool = False
    ) -> dict[str, Any]:
        props: Iterable[str]
        if changes_only:
            props = self._changes
        else:
            props = [
                "id",
                "name",
                "course_id",
                "creator_id",
                "created_at",
            ]

        # Turn to dict
        data = {}
        for prop in props:
            data[prop] = getattr(self, prop)

        # Add in extra props
        for prop in self.extra_props.keys():
            data[prop] = self.extra_props[prop]

        if rename_ed:
            # Rename keys in dict
            if "creator_id" in data:
                data["user_id"] = data["creator_id"]
                del data["creator_id"]
        return data

    def set_name(self, name: str) -> "Module":
        self._changes.add("name")
        self.name = name
        return self

    def get_course_id(self) -> CourseID:
        return self.course_id

    def get_creator_id(self) -> UserID:
        return self.creator_id

    def get_created_at(self) -> datetime:
        return self.created_at

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
    def get_all_modules(course_id: CourseID) -> list["Module"]:
        api = EdStemAPI()
        modules = api.get_all_modules(course_id)
        return [Module.from_dict(m) for m in modules]

    @staticmethod
    def get_module(course_id: CourseID, id_or_name: ModuleID | str) -> "Module":
        modules = Module.get_all_modules(course_id)
        return EdObject._filter_single_id_or_name(modules, id_or_name)

    def get_lessons(self) -> list[Lesson]:
        lessons = Lesson.get_all_lessons(self.course_id)
        return [lesson for lesson in lessons if lesson.get_module_id() == self.id]

    def get_lesson(self, id_or_name: LessonID | str) -> Lesson:
        lessons = self.get_lessons()
        return EdObject._filter_single_id_or_name(lessons, id_or_name)

    def post_changes(self, ignore_errors: bool = False) -> bool:
        try:
            module_data = self._to_dict(changes_only=True, rename_ed=True)
            module_data = self._api.edit_module(self.course_id, self.id, module_data)
            self.__dict__.update(module_data)
            return True
        except Exception as e:
            if ignore_errors:
                return False
            else:
                raise e
