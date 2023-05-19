from testing_utils import *

from edstem.user import User


class UserTest(BaseTest):
    # TODO test from_dict
    # def test_from_dict(self):
    #    user = User.from_dict(TEST_USER_0_JSON)
    #    self.assertEqual("Example Assignment", user.get_name())
    #    self.assertEqual(60007, user.get_id())
    #    self.assertEqual(38139, user.get_course_id())
    #    self.assertEqual(369, user.get_creator_id())
    #    self.assertEqual(False, user.get_openable())

    #    visibility = user.get_visibility_settings()
    #    self.assertEqual(True, visibility.hidden)
    #    self.assertEqual(False, visibility.unlisted)

    #    access = user.get_access_settings()
    #    self.assertEqual(None, access.password)
    #    self.assertEqual(None, access.tutorial_regex)
    #    self.assertEqual(None, access.timer)
    #    self.assertEqual([], access.prerequisites)

    #    scheduled = user.get_scheduled_settings()
    #    timezone = tz.gettz("America/Los_Angeles")
    #    self.assertEqual(
    #        datetime(2023, 5, 17, 15, 0, 0, 0, tzinfo=timezone), scheduled.available_at
    #    )
    #    self.assertEqual(
    #        datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.due_at
    #    )
    #    self.assertEqual(
    #        datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.locked_at
    #    )
    #    self.assertEqual(
    #        datetime(2023, 5, 18, 15, 0, 0, 0, tzinfo=timezone), scheduled.solutions_at
    #    )

    #    self.assertEqual(True, scheduled.late_submissions)
    #    self.assertEqual(False, scheduled.after_solution_submissions)
    #    self.assertEqual(False, scheduled.release_challenge_feedback)
    #    self.assertEqual(False, scheduled.release_challenge_solutions)
    #    self.assertEqual(False, scheduled.release_quiz_solutions)
    #    self.assertEqual(False, scheduled.release_quiz_correctness_only)

    #    # Low prio, but need to test quiz settings too

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
