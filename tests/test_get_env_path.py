# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.patch."""


def test_env_path():
    from autoread_dotenv.autoread import get_dotenv_path


    env_path = get_dotenv_path()
    assert env_path


