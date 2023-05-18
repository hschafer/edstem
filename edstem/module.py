from datetime import datetime
from typing import Optional

from edstem._base import *


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
        **kwargs
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

    # TODO Set name?

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
