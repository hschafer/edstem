from unittest.mock import MagicMock

from edstem import EdCourse, User
from edstem.ed_api import EdStemAPI


def MockAPI(token):
    mock_api = MagicMock(spec=EdStemAPI)
    mock_api.get_users.return_value = []
    return mock_api



def test_get_all_users():
    course = EdCourse(1234, "fake_token", api_constructor=MockAPI)
    users = course.get_all_users()
    assert users == []
