import unittest
from unittest.mock import patch

from testing_utils import *

from edstem import EdCourse, Lesson, Module, User
from edstem._base import *
from edstem.ed_api import EdStemAPI


class TestCourse(BaseTest):
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

    def test_get_lesson(self):
        # By ID
        self.assertEqual(
            self.course.get_lesson(60007), Lesson.from_dict(TEST_LESSON_0_JSON)
        )
        # By name
        self.assertEqual(
            self.course.get_lesson("Example Lesson"),
            Lesson.from_dict(TEST_LESSON_1_JSON),
        )

        # Name not found
        with self.assertRaises(ValueError):
            self.course.get_lesson("Not a lesson")
        # ID not found
        with self.assertRaises(ValueError):
            self.course.get_lesson(3)
