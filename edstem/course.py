from ed_api import EdStemAPI
from user import User


class EdCourse:
    course_id: int

    def __init__(self, course_id: int, auth_token_or_file: str):
        self.course_id = course_id
        self._api = EdStemAPI(auth_token_or_file)

    # Users

    def get_users(self) -> list[User]:
        return self._api.get_users(self.course_id)

    def get_user(self, user: int | str) -> User:
        users = self.get_users()
        users = [u for u in users
                 if u["id"] == user or
                 u["name"] == user]

        if len(users) == 0:
            raise ValueError("Does not specify any users")
        elif len(users) > 1:
            raise ValueError("Specifies more than one user")

        return users[0]

    ## TODO Get analytics users?