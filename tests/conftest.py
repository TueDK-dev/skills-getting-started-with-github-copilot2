from fastapi.testclient import TestClient
import copy
import pytest
from src.app import app, activities as activities_ref

@pytest.fixture
def client():
    original = copy.deepcopy(activities_ref)
    with TestClient(app) as client:
        yield client
    activities_ref.clear()
    activities_ref.update(original)
