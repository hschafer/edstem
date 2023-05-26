from datetime import datetime

from dateutil import tz
from testing_utils import *

from edstem.lesson import Lesson


class LessonTest(BaseTest):
    def test_from_dict(self):
        lesson = Lesson.from_dict(TEST_LESSON_0_JSON)
        self.assertEqual("Example Assignment", lesson.name)
        self.assertEqual(60007, lesson.id)
        self.assertEqual(38139, lesson.course_id)
        self.assertEqual(369, lesson.creator_id)
        self.assertEqual(False, lesson.openable)

        self.assertEqual(True, lesson.visibility.hidden)
        self.assertEqual(False, lesson.visibility.unlisted)

        self.assertEqual(None, lesson.access_settings.password)
        self.assertEqual(None, lesson.access_settings.tutorial_regex)
        self.assertEqual(None, lesson.access_settings.timer)
        self.assertEqual(tuple(), lesson.access_settings.prerequisites)

        scheduled = lesson.schedule
        timezone = tz.gettz("America/Los_Angeles")
        self.assertEqual(
            datetime(2023, 5, 17, 15, 0, 0, 0, tzinfo=timezone), scheduled.available_at
        )
        self.assertEqual(
            datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.due_at
        )
        self.assertEqual(
            datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.locked_at
        )
        self.assertEqual(
            datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.solutions_at
        )

        self.assertEqual(True, scheduled.late_submissions)
        self.assertEqual(False, scheduled.after_solution_submissions)
        self.assertEqual(False, scheduled.release_challenge_feedback)
        self.assertEqual(False, scheduled.release_challenge_solutions)
        self.assertEqual(False, scheduled.release_quiz_solutions)
        self.assertEqual(False, scheduled.release_quiz_correctness_only)

        # Low prio, but need to test quiz settings too

    def test_get_all_lessons(self):
        lessons = Lesson.get_all_lessons(TEST_COURSE_ID)
        print(lessons)
        self.assertEqual(
            set(lessons), set(Lesson.from_dict(l) for l in TEST_LESSON_JSON)
        )

    def test_get_lesson(self):
        # By ID
        self.assertEqual(
            Lesson.get_lesson(TEST_COURSE_ID, 60007),
            Lesson.from_dict(TEST_LESSON_0_JSON),
        )
        # By name
        self.assertEqual(
            Lesson.get_lesson(TEST_COURSE_ID, "Example Lesson"),
            Lesson.from_dict(TEST_LESSON_1_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            Lesson.get_lesson(TEST_COURSE_ID, "Not a lesson")
        # ID not found
        with self.assertRaises(ValueError):
            Lesson.get_lesson(TEST_COURSE_ID, 3)
