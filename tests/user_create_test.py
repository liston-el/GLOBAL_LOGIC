import json
import uuid
from typing import Callable
import pytest


def test_create_user(post_command: Callable, get_response: Callable):
    command = {
        "name": f"test_user_name_{uuid.uuid4()}",
        "gender": "Male",
        "email": f"{uuid.uuid4()}@gmail.com",
        "status": "Active"
    }

    create_response = post_command(json.dumps(command))
    create_json_response = json.loads(create_response)

    user_id = create_json_response["data"]["id"]
    user_response = get_response(user_id)
    user_json_response = json.loads(user_response)

    assert user_json_response["data"] == create_json_response["data"]


@pytest.mark.parametrize("email", (25, "QWE"))
def test_create_user_invalid_email(post_command: Callable, email, create_user: Callable):
    create_user(email)
