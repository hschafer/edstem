import unittest
from unittest.mock import MagicMock, patch

import edstem.auth
from edstem import EdCourse, User
from edstem.ed_api import EdStemAPI


def MockAPI():
    mock_api = MagicMock(spec=EdStemAPI)
    mock_api().get_users.return_value = []
    return mock_api

class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        edstem.auth.set_token("Fake Token")

        self.mock_api_patcher = patch("edstem.course.EdStemAPI", MockAPI())
        self.mock_api_patcher.start()

    def tearDown(self) -> None:
        self.mock_api_patcher.stop()

    def test_get_all_users(self):
        course = EdCourse(1234)
        users = course.get_all_users()
        self.assertEqual(users, [])
