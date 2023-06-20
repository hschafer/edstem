import copy

import responses
from testing_utils import *

from edstem.user import User


class UserTest(BaseTest):
    def test_get_all_users(self):
        users = User.get_all_users(TEST_COURSE_ID)
        print(users)
        self.assertEqual(set(users), set(User.from_dict(l) for l in TEST_USER_JSON))

    def test_get_user(self):
        # By ID
        self.assertEqual(
            User.get_user(TEST_COURSE_ID, 555),
            User.from_dict(TEST_USER_SABRINA_JSON),
        )
        # By name
        self.assertEqual(
            User.get_user(TEST_COURSE_ID, "Archie Andrews"),
            User.from_dict(TEST_USER_ARCHIE_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            User.get_user(TEST_COURSE_ID, "Not a user")
        # ID not found
        with self.assertRaises(ValueError):
            User.get_user(TEST_COURSE_ID, 3)

    @responses.activate
    def test_user_edit(self):
        # Stop other API patches
        self._stop_api_patch()
        edstem.auth.set_token("Fake Token")

        test_user_id = 555

        # Patch the specific request methods instead to check their inputs/outputs
        expected_data = TEST_USER_SABRINA_JSON | {"name": "Sabrina New"}
        get_response = responses.Response(
            method="GET",
            url=f"https://us.edstem.org/api/courses/{TEST_COURSE_ID}/admin",
            json={"users": copy.deepcopy(TEST_USER_JSON)},
        )
        patch_response = responses.Response(
            method="PATCH",
            url=f"https://us.edstem.org/api/users/{test_user_id}",
            json={"user": expected_data},
        )
        responses.add(get_response)
        responses.add(patch_response)

        user = User.get_user(TEST_COURSE_ID, test_user_id)
        user.name = "Sabrina New"
        user.post_changes()

        current_data = user._to_dict(changes_only=False)
        print(current_data)
        print(expected_data)
        self.assertEqual(expected_data, current_data)
