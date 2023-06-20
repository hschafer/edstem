import copy
from datetime import datetime
from typing import Any, NotRequired, Optional, TypedDict

import edstem._base as base
from edstem.ed_api import EdStemAPI


class SlideData(TypedDict):
    id: base.SlideID
    original_id: base.SlideID
    lesson_id: base.LessonID
    user_id: base.UserID
    course_id: base.CourseID
    type: str  # TODO Enum?
    title: str  # name
    points: int
    index: int
    is_hidden: bool
    status: str  # TODO Enum? unseen, completed, ...?
    created_at: str
    passage: base.XML
    is_survey: bool
    mode: str  # TODO Enum
    active_status: str  # TODO Enum

    # These fields seem to always be null
    correct: None
    response: None
    updated_at: None


class Slide(base.EdObject[base.SlideID]):
    _data: dict[str, Any]

    def __init__(self, data: SlideData) -> None:
        super().__init__()
        base._proper_keys(data, SlideData)  # type: ignore
        self._data = copy.deepcopy(data)  # type: ignore

    @staticmethod
    def from_dict(data: base.JSON) -> "Slide":
        base._proper_keys(data, SlideData)
        return Slide(**data)

    @property
    def id(self) -> base.SlideID:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["title"]

    @name.setter
    def name(self, value: str) -> None:
        self._changes.add("title")
        self._data["title"] = value

    @property
    def original_id(self) -> base.SlideID:
        return self._data["original_id"]

    @property
    def lesson_id(self) -> base.LessonID:
        return self._data["lesson_id"]

    @property
    def course_id(self) -> base.CourseID:
        return self._data["course_id"]

    @property
    def creator_id(self) -> base.UserID:
        return self._data["user_id"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def points(self) -> int:
        return self._data["points"]

    @property
    def index(self) -> int:
        return self._data["index"]

    @property
    def hidden(self) -> bool:
        return self._data["is_hidden"]

    @hidden.setter
    def hidden(self, value: bool) -> None:
        self._changes.add("is_hidden")
        self._data["is_hidden"] = value

    @property
    def status(self) -> str:
        return self._data["status"]

    @property
    def created_at(self) -> datetime:
        value = base.EdObject.str_to_datetime(self._data["created_at"])
        assert value is not None
        return value

    @property
    def passage(self) -> base.XML:
        return self._data["passage"]

    @passage.setter
    def passage(self, value: base.XML) -> None:
        self._changes.add("passage")
        self._data["passage"] = value

    @property
    def is_survey(self) -> bool:
        return self._data["is_survey"]

    @property
    def mode(self) -> str:
        return self._data["mode"]

    @property
    def active_status(self) -> str:
        return self._data["active_status"]

    def _tuple(self) -> tuple:
        return (
            self.name,
            self.id,
        )

    def __repr__(self) -> str:
        return f"Slide(id={self.id}, name={self.name})"

    # API Methods
    @staticmethod
    def slide(slide_id: base.SlideID) -> "Slide":
        api = EdStemAPI()
        return Slide.from_dict(api.get_slide(slide_id))

    def post_changes(self):
        slide_data = self._to_dict(changes_only=True)
        new_slide_data = self._api.edit_slide(self.id, slide_data)
        self._data.update(new_slide_data)

    def delete(self) -> None:
        self._api.delete_slide(self.id)
