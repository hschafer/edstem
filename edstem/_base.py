from datetime import datetime
from typing import Any, Generic, NewType, Optional, TypeVar

from pandas import to_datetime

from edstem.ed_api import EdStemAPI

# Types
EdID = NewType("EdID", int)
CourseID = NewType("CourseID", int)
UserID = NewType("UserID", int)
ModuleID = NewType("ModuleID", int)
LessonID = NewType("LessonID", int)
# Discussion? Slide? Quiz Question? Challenge?

JSON = dict[str, Any]

# Helper functions
IdType = TypeVar("IdType", bound=int)
ValueType = TypeVar("ValueType", bound="EdObject")


class EdObject(Generic[IdType]):
    name: str
    id: IdType
    extra_props: JSON
    _changes: set[str]
    _api: EdStemAPI

    def __init__(self, name: str, id: IdType, **kwargs):
        self.name = name
        self.id = id
        self.extra_props = kwargs
        self._api = EdStemAPI()
        self._changes = set()

    @staticmethod
    def from_dict(d: JSON) -> "EdObject":
        raise NotImplemented

    @staticmethod
    def _filter_id_or_name(
        values: list[ValueType], id_or_name: IdType | str
    ) -> list[ValueType]:
        return [
            v for v in values if v.get_id() == id_or_name or v.get_name() == id_or_name
        ]

    @staticmethod
    def _filter_single_id_or_name(
        values: list[ValueType], id_or_name: IdType | str
    ) -> ValueType:
        filtered = EdObject._filter_id_or_name(values, id_or_name)
        if len(filtered) == 0:
            raise ValueError(f"Identifier failed to identify any objects: {id_or_name}")
        elif len(filtered) > 1:
            raise ValueError(
                f"Identifier identified too many objects: {id_or_name} (found {len(filtered)})"
            )
        return filtered[0]

    @staticmethod
    def str_to_datetime(timestamp: str, timezone: Optional[str] = None) -> datetime:
        result = to_datetime(timestamp)
        if timezone:
            if result.tz:
                result = result.tz_localize(timezone)
            else:
                result = result.tz_convert(timezone)
        return result

    # TODO need to go back to Ed String format?

    # Getters
    def get_name(self) -> str:
        return self.name

    def get_id(self) -> IdType:
        return self.id

    def get_extra_props(self) -> JSON:
        return self.extra_props

    def get_extra_prop(self, key: str) -> Any:
        return self.extra_props[key]

    # General functions
    def _tuple(self) -> tuple:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if self.__class__ == other.__class__:
            return self._tuple() == other._tuple()
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self._tuple())
