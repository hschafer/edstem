from edstem._base import *


class User(EdObject[UserID]):
    email: str
    role: str
    tutorial: str
    accepted: bool
    source_id: str

    def __init__(
        self,
        name: str,
        id: UserID,
        email: str = "",
        role: str = "",
        tutorial: str = "",
        accepted: bool = False,
        source_id: str = "",
        **kwargs
    ) -> None:
        # Currently left out: username, lab_id, lti_synced
        super().__init__(name, id, **kwargs)
        self.email = email
        self.role = role
        self.tutorial = tutorial
        self.accepted = accepted
        self.source_id = source_id

    @staticmethod
    def from_dict(data: JSON) -> "User":
        return User(**data)

    def get_tutorial(self) -> str:
        return self.tutorial

    def set_tutorail(self, tutorial: str) -> None:
        self.tutorial = tutorial

    def get_role(self) -> str:
        return self.role

    def set_role(self, role) -> None:
        self.role = role

    def get_accepted(self) -> bool:
        return self.accepted

    def get_source_id(self) -> str:
        return self.source_id
