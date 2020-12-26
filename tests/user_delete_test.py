import json
from typing import Callable


def test_delete_user(post_command: Callable, get_response: Callable, delete_user: Callable, create_user):
    user_id = create_user()

    delete_user(user_id)
    check_deleted_user = get_response(user_id)
    json_check_deleted_user = json.loads(check_deleted_user)
    assert json_check_deleted_user["code"] == 404
