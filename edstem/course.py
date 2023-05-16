class EdCourse:
    course_id: int

    def __init__(self, course_id: int):
        self.course_id = course_id

    def users(refresh: bool=False) -> list[User]:

