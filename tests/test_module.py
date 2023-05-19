from testing_utils import *

from edstem.module import Module


class ModuleTest(BaseTest):
    # TODO test from_dict
    # def test_from_dict(self):
    #    module = Module.from_dict(TEST_MODULE_0_JSON)
    #    self.assertEqual("Example Assignment", module.get_name())
    #    self.assertEqual(60007, module.get_id())
    #    self.assertEqual(38139, module.get_course_id())
    #    self.assertEqual(369, module.get_creator_id())
    #    self.assertEqual(False, module.get_openable())

    #    visibility = module.get_visibility_settings()
    #    self.assertEqual(True, visibility.hidden)
    #    self.assertEqual(False, visibility.unlisted)

    #    access = module.get_access_settings()
    #    self.assertEqual(None, access.password)
    #    self.assertEqual(None, access.tutorial_regex)
    #    self.assertEqual(None, access.timer)
    #    self.assertEqual([], access.prerequisites)

    #    scheduled = module.get_scheduled_settings()
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

    def test_get_all_modules(self):
        modules = Module.get_all_modules(TEST_COURSE_ID)
        print(modules)
        self.assertEqual(
            set(modules), set(Module.from_dict(l) for l in TEST_MODULE_JSON)
        )

    def test_get_module(self):
        # By ID
        self.assertEqual(
            Module.get_module(TEST_COURSE_ID, 13194),
            Module.from_dict(TEST_MODULE_0_JSON),
        )
        # By name
        self.assertEqual(
            Module.get_module(TEST_COURSE_ID, "Second Module"),
            Module.from_dict(TEST_MODULE_1_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            Module.get_module(TEST_COURSE_ID, "Not a module")
        # ID not found
        with self.assertRaises(ValueError):
            Module.get_module(TEST_COURSE_ID, 3)

    def test_get_lesson(self):
        module = Module.from_dict(TEST_MODULE_0_JSON)

        lessons = module.get_lessons()
        self.assertEqual(1, len(lessons))
        self.assertEqual(60007, lessons[0].get_id())
