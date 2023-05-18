from datetime import datetime
from typing import Optional

from attr import dataclass

from edstem._base import *


@dataclass
class VisibilitySettings:
    hidden: bool
    unlisted: bool


@dataclass
class TimerSettings:
    duration: int
    effective_duration: int  # TODO Unsure
    timer_expiration_access: bool  # TODO Unsure


@dataclass
class Prerequisite:
    lesson_id: LessonID
    created_at: datetime
    completed: bool


@dataclass
class AccessSettings:
    password: Optional[str]
    tutorial_regex: Optional[str]
    timer: Optional[TimerSettings]
    prerequisites: list[Prerequisite]


@dataclass
class ScheduledSettings:
    # Date settings
    available_at: Optional[datetime]
    due_at: Optional[datetime]
    locked_at: Optional[datetime]
    solutions_at: Optional[datetime]
    late_submissions: bool
    after_solution_submissions: bool
    release_challenge_feedback: bool
    release_challenge_solutions: bool
    release_quiz_solutions: bool
    release_quiz_correctness_only: bool


@dataclass
class QuizSettings:
    quiz_question_number_style: str
    quiz_mode: str
    quiz_active_status: str


class Lesson(EdObject[LessonID]):
    number: int
    course_id: CourseID
    creator_id: UserID
    created_at: datetime
    openable: bool  # Can the user open the assignment ()
    visibility_settings: VisibilitySettings
    access_settings: AccessSettings
    scheduled_settings: ScheduledSettings
    quiz_settings: QuizSettings

    def __init__(
        self,
        name: str,
        id: LessonID,
        number: int,
        course_id: CourseID,
        creator_id: UserID,
        created_at: datetime | str,
        openable: bool,
        visibility_settings: Optional[VisibilitySettings] = None,
        access_settings: Optional[AccessSettings] = None,
        scheduled_settings: Optional[ScheduledSettings] = None,
        quiz_settings: Optional[QuizSettings] = None,
        timezone: Optional[str] = None,
        **kwargs
    ) -> None:
        # Currently left out: updated_at (assumed always null?), state, status
        super().__init__(name, id, **kwargs)
        self.number = number
        self.course_id = course_id
        self.creator_id = creator_id
        self.openable = openable

        if type(created_at) is str:
            self.created_at = EdObject.str_to_datetime(created_at, timezone)
        else:
            assert type(created_at) is datetime
            self.created_at = created_at

        # Default to hidden and not unlisted
        if visibility_settings is None:
            visibility_settings = VisibilitySettings(hidden=True, unlisted=False)
        self.visibility_settings = visibility_settings

        # Default access settings
        if access_settings is None:
            access_settings = AccessSettings(
                password=None, tutorial_regex=None, timer=None, prerequisites=[]
            )
        self.access_settings = access_settings

        # Default scheduled settings
        if scheduled_settings is None:
            scheduled_settings = ScheduledSettings(
                available_at=None,
                due_at=None,
                locked_at=None,
                solutions_at=None,
                late_submissions=False,
                after_solution_submissions=False,
                release_challenge_feedback=False,
                release_challenge_solutions=False,
                release_quiz_solutions=False,
                release_quiz_correctness_only=False,
            )
        self.scheduled_settings = scheduled_settings

        # Default quiz settings
        if quiz_settings is None:
            quiz_settings = QuizSettings(
                quiz_question_number_style="",
                quiz_mode="multiple-attempts",
                quiz_active_status="active",
            )
        self.quiz_settings = quiz_settings

    @staticmethod
    def _pull_from_dict(data: JSON, keys: list[str | tuple[str, str]]) -> JSON:
        result = {}
        for key in keys:
            if type(key) is tuple:
                old_key, target_key = key
                result[target_key] = data[old_key]
                del data[old_key]
            else:
                assert type(key) is str
                result[key] = data[key]
                del data[key]

        return result

    @staticmethod
    def from_dict(data: JSON) -> "Lesson":
        data = dict(data)

        ids = Lesson._pull_from_dict(
            data, [("user_id", "creator_id"), ("title", "name")]
        )
        data = data | ids  # In this case we want to put them back in

        # Convert to Visibility
        visibility_data = Lesson._pull_from_dict(
            data, [("is_hidden", "hidden"), ("is_unlisted", "unlisted")]
        )
        data["visibility"] = VisibilitySettings(**visibility_data)

        # Convert to TimerSettings
        timer_data = Lesson._pull_from_dict(
            data,
            [
                "is_timed",
                "timer_duration",
                "timer_effective_duration",
                "timer_expiration_access",
            ],
        )
        if timer_data["is_timed"]:
            timer = TimerSettings(
                duration=timer_data["timer_duration"],
                effective_duration=timer_data["timer_effective_duration"],
                timer_expiration_access=timer_data["timer_expiration_access"],
            )
        else:
            timer = None

        # Convert prereqs
        prereq_data = Lesson._pull_from_dict(data, ["prerequisites"])
        prereqs = []
        for prereq in prereq_data["prerequisites"]:
            prereqs.append(
                Prerequisite(
                    prereq["required_lesson_id"],
                    prereq["created_at"],
                    prereq["completed"],
                )
            )

        # Make access settings
        access_data = Lesson._pull_from_dict(data, ["password", "tutorial_regex"])
        data["access_settings"] = AccessSettings(
            access_data["password"], access_data["tutorial_regex"], timer, prereqs
        )

        # Make ScheduledSettings
        date_data = Lesson._pull_from_dict(
            data, ["available_at", "due_at", "locked_at", "solutions_at"]
        )
        for key in date_data.keys():
            date_data[key] = (
                EdObject.str_to_datetime(date_data[key]) if date_data[key] else None
            )
        other_sched_data = Lesson._pull_from_dict(
            data,
            [
                "late_submissions",
                "release_challenge_feedback",
                "release_challenge_solutions",
                "release_quiz_solutions",
                "release_quiz_correctness_only",
                ("reopen_submissions", "after_solution_submissions"),
            ],
        )
        data["scheduled_settings"] = ScheduledSettings(**date_data, **other_sched_data)

        # Quiz Settings
        quiz_data = Lesson._pull_from_dict(data, ["settings"])["settings"]
        data["quiz_settings"] = QuizSettings(**quiz_data)

        return Lesson(**data)

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
        )
