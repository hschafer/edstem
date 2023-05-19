from datetime import datetime

from dateutil import tz
from testing_utils import *

from edstem.lesson import Lesson


class LessonTest(BaseTest):
    def test_from_dict(self):
        lesson = Lesson.from_dict(TEST_LESSON_0_JSON)
        self.assertEqual("Example Assignment", lesson.get_name())
        self.assertEqual(60007, lesson.get_id())
        self.assertEqual(38139, lesson.get_course_id())
        self.assertEqual(369, lesson.get_creator_id())
        self.assertEqual(False, lesson.get_openable())

        visibility = lesson.get_visibility_settings()
        self.assertEqual(True, visibility.hidden)
        self.assertEqual(False, visibility.unlisted)

        access = lesson.get_access_settings()
        self.assertEqual(None, access.password)
        self.assertEqual(None, access.tutorial_regex)
        self.assertEqual(None, access.timer)
        self.assertEqual([], access.prerequisites)

        scheduled = lesson.get_scheduled_settings()
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
