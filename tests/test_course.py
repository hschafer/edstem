import unittest
from unittest.mock import MagicMock, patch

import edstem.auth
from edstem import EdCourse, Module, User
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


def MockAPI():
    mock_api = MagicMock(spec=EdStemAPI)
    mock_api().get_users.return_value = TEST_USER_JSON
    mock_api().get_all_modules.return_value = TEST_MODULE_JSON
    return mock_api


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        # sedstem.auth.set_token("Fake Token")

        self.mock_patchers = {}
        modules_to_patch = ["_base", "course", "user", "module"]
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
