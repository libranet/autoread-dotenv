# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.autoread."""
import os

def test_env_path():
    from autoread_dotenv.autoread import get_dotenv_path


    env_path = get_dotenv_path()
    assert env_path



def test_autoread_dotenv():
    from autoread_dotenv.autoread import autoread_dotenv

    foo = os.getenv("FOO")
    assert  foo is None

    autoread_dotenv()

    foo = os.getenv("FOO")
    assert  foo == "foo"