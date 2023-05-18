from typing import Generic, NewType, TypeVar

from edstem.ed_api import EdStemAPI

EdID = NewType("EdID", int)
CourseID = NewType("CourseID", EdID)
UserID = NewType("UserID", EdID)
ModuleID = NewType("ModuleID", EdID)
LessonID = NewType("LessonID", EdID)
# Discussion? Slide? Quiz Question? Challenge?

IdType = TypeVar("IdType", bound=EdID)

class EdObject(Generic[IdType]):
    name: str
    id: IdType

    def __init__(self, name: str, id: IdType):
        self.name = name
        self.id = id
        self._api = EdStemAPI()

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> IdType:
        return self.id
