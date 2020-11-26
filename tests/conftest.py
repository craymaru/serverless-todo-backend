import pytest

from app import app as chalice_app


@pytest.fixture
def app():
    return chalice_app