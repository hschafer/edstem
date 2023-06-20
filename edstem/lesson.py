import copy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, NotRequired, Optional, Sequence, TypedDict

import edstem._base as base
from edstem.ed_api import EdStemAPI
from edstem.slide import Slide, SlideData


@dataclass(frozen=True)
class Prerequisite:
    lesson_id: base.LessonID
    created_at: datetime
    completed: bool


class LessonData(TypedDict):
    id: base.UserID
    title: str
    lesson_number: int
    course_id: base.CourseID
    module_id: base.ModuleID | None
    creator_id: base.UserID
    created_at: datetime
    openable: bool  # Can the user open the assignment
    slides: list[SlideData]


# Note: The implementation below is pretty complicated to achieve
# two primary design goals
# 1) Lessons on Ed have lots of settings groups, want this reflected in Python wrapper
# 2) Want all edits to be done via properties that change the underlying dict that Ed understands
# To achieve this, the settings objects need to be aware of their parent lesson to edit it
# A "simpler" implementation would require storing a separate set of state and marshalling in/out
# to Ed objects.


class Lesson(base.EdObject[base.LessonID]):
    _data: dict[str, Any]
    _cached_created_at: datetime | None
    _timezone: str | None
    _slides: list[Slide]

    class VisibilitySettings:
        def __init__(self, lesson: "Lesson") -> None:
            self._lesson = lesson

        @property
        def hidden(self) -> bool:
            return self._lesson._data["is_hidden"]

        @hidden.setter
        def hidden(self, value: bool) -> None:
            self._lesson._changes.add("is_hidden")
            self._lesson._data["is_hidden"] = value

        @property
        def unlisted(self) -> bool:
            return self._lesson._data["is_unlisted"]

        @unlisted.setter
        def unlisted(self, value: bool) -> None:
            self._lesson._changes.add("is_unlisted")
            self._lesson._data["is_unlisted"] = value

    class TimerSettings:
        def __init__(self, lesson: "Lesson"):
            self._lesson = lesson

        @property
        def duration(self) -> int:
            return self._lesson._data["timer_duration"]

        @duration.setter
        def duration(self, value: int) -> None:
            self._lesson._changes.add("timer_duration")
            self._lesson._data["timer_duration"] = value

        @property
        def effective_duration(self) -> int:
            return self._lesson._data["timer_effective_duration"]

        @effective_duration.setter
        def effective_duration(self, value: int) -> None:
            self._lesson._changes.add("timer_effective_duration")
            self._lesson._data["timer_effective_duration"] = value

        @property
        def expiration_access(self) -> bool:
            return self._lesson._data["timer_expiration_access"]

        @expiration_access.setter
        def expiration_access(self, value: bool) -> None:
            self._lesson._changes.add("timer_expiration_access")
            self._lesson._data["timer_expiration_access"] = value

    class AccessSettings:
        def __init__(self, lesson: "Lesson"):
            self._lesson = lesson
            self._timer: Lesson.TimerSettings | None
            if lesson._data["is_timed"]:
                self._timer = Lesson.TimerSettings(lesson)
            else:
                self._timer = None

        @property
        def password(self) -> str | None:
            return self._lesson._data["password"]

        @password.setter
        def password(self, value: str | None) -> None:
            self._lesson._changes.add("password")
            self._lesson._data["password"] = value

        @property
        def tutorial_regex(self) -> str | None:
            return self._lesson._data["tutorial_regex"]

        @tutorial_regex.setter
        def tutorial_regex(self, value: str | None) -> None:
            self._lesson._changes.add("tutorial_regex")
            self._lesson._data["tutorial_regex"] = value

        @property
        def timer(self) -> Optional["Lesson.TimerSettings"]:
            return self._timer

        @timer.setter
        def timer(self, value: Optional["Lesson.TimerSettings"]) -> None:
            self._lesson._changes.add("is_timed")
            self._lesson._data["is_timed"] = value is not None

            if value is None:
                if self._timer is not None:
                    self._timer.duration = 0
                    self._timer.effective_duration = 0
                    self._timer.expiration_access = False
            else:
                if self._timer is None:
                    self._timer = Lesson.TimerSettings(self._lesson)
                self._timer.duration = value.duration
                self._timer.effective_duration = value.effective_duration
                self._timer.expiration_access = value.expiration_access

        @property
        def prerequisites(self) -> tuple[Prerequisite, ...]:
            # TODO document immutable
            return tuple(
                Prerequisite(
                    prereq["required_lesson_id"],
                    prereq["created_at"],
                    prereq["completed"],
                )
                for prereq in self._lesson._data["prerequisites"]
            )

        @prerequisites.setter
        def prerequisites(self, value: Sequence[Prerequisite]):
            self._lesson._changes.add("prererquisites")
            self._lesson._data["prerequisites"] = [
                {
                    "required_lesson_id": prereq.lesson_id,
                    "created_at": prereq.created_at,
                    "completed": prereq.completed,
                }
                for prereq in value
            ]

    class ScheduledSettings:
        def __init__(self, lesson: "Lesson") -> None:
            self._lesson = lesson

        @property
        def available_at(self) -> datetime | None:
            return base.EdObject.str_to_datetime(self._lesson._data["available_at"])

        @available_at.setter
        def available_at(self, value: str | datetime | None) -> None:
            self._lesson._changes.add("available_at")
            self._lesson._data["available_at"] = value

        @property
        def due_at(self) -> datetime | None:
            return base.EdObject.str_to_datetime(self._lesson._data["due_at"])

        @due_at.setter
        def due_at(self, value: str | datetime | None) -> None:
            self._lesson._changes.add("due_at")
            self._lesson._data["due_at"] = value

        @property
        def locked_at(self) -> datetime | None:
            return base.EdObject.str_to_datetime(self._lesson._data["locked_at"])

        @locked_at.setter
        def locked_at(self, value: str | datetime | None) -> None:
            self._lesson._changes.add("locked_at")
            self._lesson._data["locked_at"] = value

        @property
        def solutions_at(self) -> datetime | None:
            return base.EdObject.str_to_datetime(self._lesson._data["solutions_at"])

        @solutions_at.setter
        def solutions_at(self, value: str | datetime | None) -> None:
            self._lesson._changes.add("solutions_at")
            self._lesson._data["solutions_at"] = value

        @property
        def late_submissions(self) -> bool:
            return self._lesson._data["late_submissions"]

        @late_submissions.setter
        def late_submissions(self, value: bool) -> None:
            self._lesson._changes.add("late_submissions")
            self._lesson._data["late_submissions"] = value

        @property
        def after_solution_submissions(self) -> bool:
            return self._lesson._data["reopen_submissions"]

        @after_solution_submissions.setter
        def after_solution_submissions(self, value: bool) -> None:
            self._lesson._changes.add("reopen_submissions")
            self._lesson._data["reopen_submissions"] = value

        @property
        def release_challenge_feedback(self) -> bool:
            return self._lesson._data["release_challenge_feedback"]

        @release_challenge_feedback.setter
        def release_challenge_feedback(self, value: bool) -> None:
            self._lesson._changes.add("release_challenge_feedback")
            self._lesson._data["release_challenge_feedback"] = value

        @property
        def release_challenge_solutions(self) -> bool:
            return self._lesson._data["release_challenge_solutions"]

        @release_challenge_solutions.setter
        def release_challenge_solutions(self, value: bool) -> None:
            self._lesson._changes.add("release_challenge_solutions")
            self._lesson._data["release_challenge_solutions"] = value

        @property
        def release_quiz_solutions(self) -> bool:
            return self._lesson._data["release_quiz_solutions"]

        @release_quiz_solutions.setter
        def release_quiz_solutions(self, value: bool) -> None:
            self._lesson._changes.add("release_quiz_solutions")
            self._lesson._data["release_quiz_solutions"] = value

        @property
        def release_quiz_correctness_only(self) -> bool:
            return self._lesson._data["release_quiz_correctness_only"]

        @release_quiz_correctness_only.setter
        def release_quiz_correctness_only(self, value: bool) -> None:
            self._lesson._changes.add("release_quiz_correctness_only")
            self._lesson._data["release_quiz_correctness_only"] = value

    class QuizSettings:
        def __init__(self, lesson: "Lesson") -> None:
            self._lesson = lesson

        # TODO Verify values
        @property
        def quiz_question_number_style(self) -> str:
            return self._lesson._data["settings"]["quiz_question_number_style"]

        @quiz_question_number_style.setter
        def quiz_question_number_style(self, value: str) -> None:
            self._lesson._changes.add("settings")
            self._lesson._data["settings"]["quiz_question_number_style"] = value

        @property
        def quiz_mode(self) -> str:
            return self._lesson._data["settings"]["quiz_mode"]

        @quiz_mode.setter
        def quiz_mode(self, value: bool) -> None:
            self._lesson._changes.add("settings")
            self._lesson._data["settings"]["quiz_mode"] = value

        @property
        def quiz_active_status(self) -> bool:
            return self._lesson._data["settings"]["quiz_active_status"]

        @quiz_active_status.setter
        def quiz_active_status(self, value: bool) -> None:
            self._lesson._changes.add("settings")
            self._lesson._data["settings"]["quiz_active_status"] = value

    # TODO Right now we don't allow constructor setting of many settings and the setters need
    # To be called. Figure out a good interface for specifying settings at beginning if desired
    def __init__(self, data: dict[str, Any]) -> None:
        # Currently left out: updated_at (assumed always null?), state, status
        super().__init__()

        # Set simple properties
        self._data = copy.deepcopy(data)

        # Change some default values
        if self._data["password"] == "":
            self._data["password"] = None
        if self._data["tutorial_regex"] == "":
            self._data["tutorial_regex"] = None

        self._visibility = Lesson.VisibilitySettings(self)
        self._access = Lesson.AccessSettings(self)
        self._schedule = Lesson.ScheduledSettings(self)
        self._quiz = Lesson.QuizSettings(self)

        # Set up slides
        self._slides = [
            Slide.from_dict(slide_data) for slide_data in self._data["slides"]
        ]

    @staticmethod
    def from_dict(data: base.JSON) -> "Lesson":
        return Lesson(data)

    @property
    def id(self) -> base.LessonID:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["title"]

    @name.setter
    def name(self, value: str) -> None:
        self._changes.add("title")
        self._data["title"] = value

    @property
    def course_id(self) -> base.CourseID:
        return self._data["course_id"]

    @property
    def module_id(self) -> base.ModuleID | None:
        return self._data["module_id"]

    @property
    def creator_id(self) -> base.UserID:
        return self._data["user_id"]

    @property
    def timezone(self) -> str | None:
        return self._timezone

    @timezone.setter
    def timezone(self, value: str | None) -> None:
        self._timezone = value
        self._cached_created_at = None

    @property
    def created_at(self) -> datetime:
        if self._cached_created_at is None:
            self._cached_created_at = base.EdObject.str_to_datetime(
                self._data["created_at"], self.timezone
            )
        assert self._cached_created_at is not None
        return self._cached_created_at

    @property
    def openable(self) -> bool:
        return self._data["openable"]

    @property
    def visibility(self) -> VisibilitySettings:
        return self._visibility

    @property
    def access_settings(self) -> AccessSettings:
        return self._access

    @property
    def schedule(self) -> ScheduledSettings:
        return self._schedule

    @property
    def quiz_settings(self) -> QuizSettings:
        return self._quiz

    @property
    def slides(self) -> list[Slide]:
        return self._slides

    def get_slide(self, id_or_name: base.SlideID | str):
        return base.EdObject._filter_single_id_or_name(self._slides, id_or_name)

    def _tuple(self) -> tuple:
        return (
            self.name,
            self.id,
        )

    def __repr__(self) -> str:
        return f"Lesson(id={self.id}, name={self.name})"

    # API Methods
    @staticmethod
    def get_all_lessons(course_id: base.CourseID) -> list["Lesson"]:
        api = base.EdStemAPI()
        lessons = api.get_all_lessons(course_id)
        return [Lesson.from_dict(l) for l in lessons]

    @staticmethod
    def get_lesson(
        course_id: base.CourseID, id_or_name: base.LessonID | str
    ) -> "Lesson":
        lessons = Lesson.get_all_lessons(course_id)
        return base.EdObject._filter_single_id_or_name(lessons, id_or_name)

    def get_module(self) -> Optional["Module"]:
        if self.module_id is None:
            return None
        else:
            return Module.get_module(self.course_id, self.module_id)

    def post_changes(self):
        # Have each slide post changes
        for slide in self._slides:
            slide.post_changes()

        lesson_data = self._to_dict(changes_only=True)
        new_lesson_data = self._api.edit_lesson(self.id, lesson_data)
        self._data.update(new_lesson_data)


from edstem.module import (
    Module,
)  # Kind of a hack to avoid circular dependency being unresolvable
