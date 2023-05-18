import unittest
from unittest.mock import MagicMock, patch

import edstem.auth
from edstem import EdCourse, User
from edstem.ed_api import EdStemAPI

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


def MockAPI():
    mock_api = MagicMock(spec=EdStemAPI)
    mock_api().get_users.return_value = TEST_USER_JSON
    return mock_api


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        # sedstem.auth.set_token("Fake Token")

        self.mock_patchers = {}
        modules_to_patch = ["_base", "course", "user"]
        for to_patch in modules_to_patch:
            patcher = patch(f"edstem.{to_patch}.EdStemAPI", MockAPI())
            self.mock_patchers[to_patch] = patcher
            patcher.start()

    def tearDown(self) -> None:
        for patcher in self.mock_patchers.values():
            patcher.stop()

    def test_get_all_users(self):
        course = EdCourse(1234)
        users = course.get_all_users()
        self.assertEqual(set(users), set(User.from_dict(u) for u in TEST_USER_JSON))

    def test_get_user(self):
        course = EdCourse(1234)
        # By ID
        print(
            course.get_user(555).__class__,
            User.from_dict(TEST_USER_SABRINA_JSON).__class__,
        )
        self.assertEqual(course.get_user(555), User.from_dict(TEST_USER_SABRINA_JSON))
        # By name
        self.assertEqual(
            course.get_user("Archie Andrews"), User.from_dict(TEST_USER_ARCHIE_JSON)
        )
