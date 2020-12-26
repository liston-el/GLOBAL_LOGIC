import json
import uuid
from typing import Callable


def test_user_update(post_command: Callable, get_response: Callable, patch_user: Callable, create_user):
    user_id = create_user()
    command = {
        "name": f"test__changed_user_name_{uuid.uuid4()}",
        "gender": "Male",
        "email": f"p{uuid.uuid4()}@gmail.com",
        "status": "Active"
    }
    response = patch_user(json.dumps(command), user_id)
    response = json.loads(response)
    assert response["data"]["name"] == command.get("name")
