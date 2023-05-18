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
        super().__init__(name, id)
        self.email = email
        self.role = role
        self.tutorial = tutorial
        self.accepted = accepted
        self.source_id = source_id
        self.extra_props = kwargs

    @staticmethod
    def from_dict(data: JSON) -> "User":
        return User(**data)

    def get_tutorial(self) -> str:
        return self.tutorial
