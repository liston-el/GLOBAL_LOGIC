import json
import logging
import os
import uuid
from typing import Callable
import logging.handlers

import pytest
import requests

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper(),
                    format="[%(asctime)s.%(msecs)03d][%(levelname)s]: %(message)s",
                    datefmt="%H:%M:%S")


url = "https://gorest.co.in/public-api/users"
headers = {"Authorization": "Bearer 9c4e798cc9e663d3b6ee329346329cb4a58fa597ea3d4dafafe24589253e89e9",
           "Content-Type": "application/json",
           "Cache-Control": "no-cache"}


@pytest.fixture(scope="session")
def post_command() -> Callable:
    def _post_command(command=None, result="passed"):
        response = requests.post(url, headers=headers, data=command)
        logging.info(f"Response status code: {response.status_code}")
        if result == "passed":
            assert response.status_code == requests.codes.ok
        else:
            assert response.status_code != requests.codes.ok  # here is bug
        logging.info(f"Posted: {command}")
        return response.content

    return _post_command


@pytest.fixture(scope="session")
def get_response() -> Callable:
    def _get_response(user_id=None):
        response = requests.get(url=url + f"/{user_id}", headers=headers)
        logging.info(f"Response status code: {response.status_code}")
        assert response.status_code == requests.codes.ok
        logging.info(f"Response: {response.content}")
        return response.content

    return _get_response


@pytest.fixture(scope="session")
def patch_user() -> Callable:
    def _patch_user(command=None, user_id=None):
        patch_url = "https://gorest.co.in/public-api/users" + f"/{user_id}"
        response = requests.patch(url=patch_url, headers=headers, data=command)
        logging.info(f"Response status code: {response.status_code}")
        assert response.status_code == requests.codes.ok
        logging.info(f"Response: {response.content}")
        return response.content

    return _patch_user


@pytest.fixture(scope="session")
def delete_user() -> Callable:
    def _delete_user(user_id=None):
        patch_url = "https://gorest.co.in/public-api/users" + f"/{user_id}"
        response = requests.delete(url=patch_url, headers=headers)
        logging.info(f"Response status code: {response.status_code}")
        assert response.status_code == requests.codes.ok
        logging.info(f"Response: {response.content}")
        return response.content

    return _delete_user


@pytest.fixture(scope="session")
def create_user(post_command, get_response) -> Callable:
    def _create_user(email=f"{uuid.uuid4()}@gmail.com"):
        command = {
            "name": f"test_user_name_{uuid.uuid4()}",
            "gender": "Male",
            "email": email,
            "status": "Active"
        }

        create_response = post_command(json.dumps(command))
        create_json_response = json.loads(create_response)

        user_id = create_json_response["data"]["id"]

        user_response = get_response(user_id)
        json_user_response = json.loads(user_response)
        assert json_user_response["code"] == 200

        return user_id

    return _create_user

