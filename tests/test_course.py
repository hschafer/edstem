import unittest
from unittest.mock import MagicMock, patch

import edstem.auth
from edstem import EdCourse, Lesson, Module, User
from edstem._base import *
from edstem.ed_api import EdStemAPI

TEST_COURSE_ID = 1234

TEST_USER_AANG_JSON = {
    "id": 123,
    "role": "student",
    "name": "Aang Airbender",
    "email": "aang@uw.edu",
    "sourced_id": "F19BD9DD7624A73EBF3EF562A06BEF4A",
    "username": None,
    "tutorial": None,
    "lab_id": None,
    "accepted": True,
    "lti_synced": True,
}
TEST_USER_ARCHIE_JSON = {
    "id": 321,
    "role": "student",
    "name": "Archie Andrews",
    "email": "archie@cs.washington.edu",
    "sourced_id": "E9BBC48BE8AA8E3E9DBD743619A35B6F",
    "username": None,
    "tutorial": "AE",
    "lab_id": None,
    "accepted": True,
    "lti_synced": False,
}
TEST_USER_SABRINA_JSON = {
    "id": 555,
    "role": "mentor",
    "name": "Sabrina Spellman",
    "email": "itssabrina@gmail.com",
    "sourced_id": "",
    "username": None,
    "tutorial": None,
    "lab_id": None,
    "accepted": True,
    "lti_synced": False,
}
TEST_USER_JSON = [TEST_USER_AANG_JSON, TEST_USER_ARCHIE_JSON, TEST_USER_SABRINA_JSON]

TEST_MODULE_0_JSON = {
    "id": 13194,
    "course_id": TEST_COURSE_ID,
    "user_id": 369,
    "name": "First Module",
    "created_at": "2023-03-27T12:25:16.543002+11:00",
    "updated_at": None,
}
TEST_MODULE_1_JSON = {
    "id": 13196,
    "course_id": TEST_COURSE_ID,
    "user_id": 369,
    "name": "Second Module",
    "created_at": "2023-03-27T12:25:18.086026+11:00",
    "updated_at": None,
}
TEST_MODULE_JSON = [TEST_MODULE_0_JSON, TEST_MODULE_1_JSON]

TEST_LESSON_0_JSON: JSON = {
    "attempted_at": None,
    "available_at": "2023-05-18T08:00:00+10:00",
    "course_id": 38139,
    "created_at": "2023-03-29T11:04:36.691113+11:00",
    "due_at": "2023-05-19T08:00:00+10:00",
    "first_viewed_at": "2023-04-25T11:23:16.108332+10:00",
    "id": 60007,
    "index": None,
    "is_hidden": True,
    "is_timed": False,
    "is_unlisted": False,
    "last_viewed_slide_id": 335934,
    "late_submissions": True,
    "locked_at": "2023-05-19T08:00:00+10:00",
    "module_id": None,
    "number": -1,
    "openable": False,
    "original_id": None,
    "outline": "",
    "password": "",
    "prerequisites": [],
    "release_challenge_feedback": False,
    "release_challenge_feedback_while_active": False,
    "release_challenge_solutions": False,
    "release_challenge_solutions_while_active": False,
    "release_quiz_correctness_only": False,
    "release_quiz_solutions": False,
    "reopen_submissions": False,
    "settings": {
        "quiz_question_number_style": "",
        "quiz_mode": "multiple-attempts",
        "quiz_active_status": "active",
    },
    "slide_count": 9,
    "solutions_at": "2023-05-19T08:00:00+10:00",
    "state": "scheduled",
    "status": "unattempted",
    "timer_duration": 60,
    "timer_effective_duration": 60,
    "timer_expiration_access": False,
    "title": "Example Assignment",
    "tutorial_regex": "",
    "type": "general",
    "updated_at": None,
    "user_id": 369,
}
TEST_LESSON_1_JSON: JSON = {
    "attempted_at": None,
    "available_at": None,
    "course_id": 38139,
    "created_at": "2023-05-05T05:51:36.969591+10:00",
    "due_at": None,
    "first_viewed_at": None,
    "id": 62178,
    "index": None,
    "is_hidden": True,
    "is_timed": False,
    "is_unlisted": False,
    "last_viewed_slide_id": None,
    "late_submissions": True,
    "locked_at": None,
    "module_id": None,
    "number": -1,
    "openable": False,
    "original_id": None,
    "outline": "",
    "password": "",
    "prerequisites": [],
    "release_challenge_feedback": False,
    "release_challenge_feedback_while_active": False,
    "release_challenge_solutions": False,
    "release_challenge_solutions_while_active": False,
    "release_quiz_correctness_only": False,
    "release_quiz_solutions": False,
    "reopen_submissions": False,
    "settings": {
        "quiz_question_number_style": "",
        "quiz_mode": "multiple-attempts",
        "quiz_active_status": "active",
    },
    "slide_count": 0,
    "solutions_at": None,
    "state": "active",
    "status": "unattempted",
    "timer_duration": 60,
    "timer_effective_duration": 60,
    "timer_expiration_access": False,
    "title": "Example Lesson",
    "tutorial_regex": "",
    "type": "general",
    "updated_at": None,
    "user_id": 65209,
}
TEST_LESSON_JSON = [TEST_LESSON_0_JSON, TEST_LESSON_1_JSON]


def MockAPI():
    mock_api = MagicMock(spec=EdStemAPI)
    mock_api().get_users.return_value = TEST_USER_JSON
    mock_api().get_all_modules.return_value = TEST_MODULE_JSON
    mock_api().get_all_lessons.return_value = TEST_LESSON_JSON
    return mock_api


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        # sedstem.auth.set_token("Fake Token")

        self.mock_patchers = {}
        modules_to_patch = [
            "_base",
            "course",
            "lesson",
            "module",
            "user",
        ]
        for to_patch in modules_to_patch:
            patcher = patch(f"edstem.{to_patch}.EdStemAPI", MockAPI())
            self.mock_patchers[to_patch] = patcher
            patcher.start()

        self.course = EdCourse(CourseID(TEST_COURSE_ID))

    def tearDown(self) -> None:
        for patcher in self.mock_patchers.values():
            patcher.stop()

    def test_get_all_users(self):
        users = self.course.get_all_users()
        self.assertEqual(set(users), set(User.from_dict(u) for u in TEST_USER_JSON))

    def test_get_user(self):
        # By ID
        self.assertEqual(
            self.course.get_user(555), User.from_dict(TEST_USER_SABRINA_JSON)
        )
        # By name
        self.assertEqual(
            self.course.get_user("Archie Andrews"),
            User.from_dict(TEST_USER_ARCHIE_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            self.course.get_user("Not a user")
        # ID not found
        with self.assertRaises(ValueError):
            self.course.get_user(3)

    def test_get_all_modules(self):
        modules = self.course.get_all_modules()
        self.assertEqual(
            set(modules), set(Module.from_dict(m) for m in TEST_MODULE_JSON)
        )

    def test_get_module(self):
        # By ID
        self.assertEqual(
            self.course.get_module(13194), Module.from_dict(TEST_MODULE_0_JSON)
        )
        # By name
        self.assertEqual(
            self.course.get_module("Second Module"),
            Module.from_dict(TEST_MODULE_1_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            self.course.get_module("Not a module")
        # ID not found
        with self.assertRaises(ValueError):
            self.course.get_module(3)

    def test_get_all_lessons(self):
        lessons = self.course.get_all_lessons()
        print(lessons)
        self.assertEqual(
            set(lessons), set(Lesson.from_dict(l) for l in TEST_LESSON_JSON)
        )
