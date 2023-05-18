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

JSON = dict[str, Any]

# Discussion? Slide? Quiz Question? Challenge?

IdType = TypeVar("IdType", bound=int)


class EdObject(Generic[IdType]):
    name: str
    id: IdType
    extra_props: JSON
    _api: EdStemAPI

    def __init__(self, name: str, id: IdType, **kwargs):
        self.name = name
        self.id = id
        self.extra_props = kwargs
        self._api = EdStemAPI()

    @staticmethod
    def from_dict(d: JSON) -> "EdObject":
        raise NotImplemented

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

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> IdType:
        return self.id

    def get_extra_props(self, key=None) -> JSON | Any:
        if key is None:
            return self.extra_props
        else:
            return self.extra_props[key]

    def _tuple(self) -> tuple:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if self.__class__ == other.__class__:
            return self._tuple() == other._tuple()
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self._tuple())
