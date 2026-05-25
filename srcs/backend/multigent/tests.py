import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Review
from agents_ai.github.context_builder import build_context_from_file, build_context_from_pasted_code


@pytest.fixture
def client():
    """
    Unauthenticated DRF API client.
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    A standard test user persisted in the database.
    """
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def other_user(db):
    """
    A second user used to verify ownership isolation.
    """
    return User.objects.create_user(username="otheruser", password="testpass123")


@pytest.fixture
def auth_client(client, user):
    """
    API client with a valid JWT Bearer token for testuser.
    """
    res = client.post("/api/auth/token/", {"username": "testuser", "password": "testpass123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client


@pytest.fixture
def review(user, db):
    """
    A Review record owned by testuser, created directly in the DB.
    """
    return Review.objects.create(user=user, source="pasted_code", label="snippet")


@pytest.mark.django_db
def test_register_success(client):
    """
    Valid registration data should create a user and return 201.
    """
    res = client.post("/api/auth/register/", {"username": "newuser", "password": "pass1234"}, format="json")
    assert res.status_code == 201


@pytest.mark.django_db
def test_register_duplicate_username(client, user):
    """
    Registering with an already-taken username should return 400.
    """
    res = client.post("/api/auth/register/", {"username": "testuser", "password": "pass1234"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_register_missing_password(client):
    """
    Omitting the password field should return 400.
    """
    res = client.post("/api/auth/register/", {"username": "newuser"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_register_missing_username(client):
    """
    Omitting the username field should return 400.
    """
    res = client.post("/api/auth/register/", {"password": "pass1234"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_login_success(client, user):
    """
    Correct credentials should return 200 with access and refresh tokens.
    """
    res = client.post("/api/auth/token/", {"username": "testuser", "password": "testpass123"}, format="json")
    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data


@pytest.mark.django_db
def test_login_wrong_password(client, user):
    """
    A wrong password should be rejected with 401.
    """
    res = client.post("/api/auth/token/", {"username": "testuser", "password": "wrongpass"}, format="json")
    assert res.status_code == 401


@pytest.mark.django_db
def test_login_nonexistent_user(client):
    """
    A username that does not exist should return 401.
    """
    res = client.post("/api/auth/token/", {"username": "ghost", "password": "pass1234"}, format="json")
    assert res.status_code == 401


@pytest.mark.django_db
def test_login_missing_fields(client):
    """
    Submitting an empty body should return 400.
    """
    res = client.post("/api/auth/token/", {}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_review_create_success(auth_client):
    """
    An authenticated request with valid code should return 202 and a review id.
    """
    res = auth_client.post("/api/reviews/", {"code": "print('hello')"}, format="json")
    assert res.status_code == 202
    assert "id" in res.data


@pytest.mark.django_db
def test_review_create_unauthenticated(client):
    """
    An unauthenticated request should be rejected with 401.
    """
    res = client.post("/api/reviews/", {"code": "print('hello')"}, format="json")
    assert res.status_code == 401


@pytest.mark.django_db
def test_review_create_empty_code(auth_client):
    """
    Submitting a whitespace-only code string should return 400.
    """
    res = auth_client.post("/api/reviews/", {"code": "   "}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_review_create_missing_code(auth_client):
    """
    Omitting the code field entirely should return 400.
    """
    res = auth_client.post("/api/reviews/", {}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_review_list_empty(auth_client):
    """
    A user with no reviews should receive an empty list.
    """
    res = auth_client.get("/api/reviews/all/")
    assert res.status_code == 200
    assert res.data == []


@pytest.mark.django_db
def test_review_list_contains_own_reviews(auth_client, review):
    """
    A user's own reviews should appear in the list.
    """
    res = auth_client.get("/api/reviews/all/")
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["id"] == review.id


@pytest.mark.django_db
def test_review_list_unauthenticated(client):
    """
    An unauthenticated request should be rejected with 401.
    """
    res = client.get("/api/reviews/all/")
    assert res.status_code == 401


@pytest.mark.django_db
def test_review_list_excludes_other_users(auth_client, other_user, db):
    """
    Reviews belonging to another user should not appear in the list.
    """
    Review.objects.create(user=other_user, source="pasted_code", label="snippet")
    res = auth_client.get("/api/reviews/all/")
    assert res.status_code == 200
    assert len(res.data) == 0


@pytest.mark.django_db
def test_review_detail_success(auth_client, review):
    """
    Requesting an owned review by id should return 200 with the review data.
    """
    res = auth_client.get(f"/api/reviews/{review.id}/")
    assert res.status_code == 200
    assert res.data["id"] == review.id


@pytest.mark.django_db
def test_review_detail_not_found(auth_client):
    """
    Requesting a non-existent review id should return 404.
    """
    res = auth_client.get("/api/reviews/99999/")
    assert res.status_code == 404


@pytest.mark.django_db
def test_review_detail_unauthenticated(client, review):
    """
    An unauthenticated request for a review should return 401.
    """
    res = client.get(f"/api/reviews/{review.id}/")
    assert res.status_code == 401


@pytest.mark.django_db
def test_review_detail_other_user_review(auth_client, other_user, db):
    """
    Requesting another user's review should return 404, not 403, to avoid leaking ids.
    """
    other_review = Review.objects.create(user=other_user, source="pasted_code", label="snippet")
    res = auth_client.get(f"/api/reviews/{other_review.id}/")
    assert res.status_code == 404


def test_build_context_from_file_returns_bundle():
    """
    File names and contents should both appear in the assembled code bundle.
    """
    files = [
        {"name": "foo.py", "content": "print('hello')"},
        {"name": "bar.py", "content": "x = 1"},
    ]
    result = build_context_from_file(files)
    assert "foo.py" in result["code_bundle"]
    assert "print('hello')" in result["code_bundle"]
    assert "bar.py" in result["code_bundle"]


def test_build_context_from_file_returns_file_names():
    """
    The files_included list should contain the name of each provided file.
    """
    files = [{"name": "a.py", "content": "pass"}]
    result = build_context_from_file(files)
    assert result["files_included"] == ["a.py"]


def test_build_context_from_file_empty_list():
    """
    An empty file list should produce an empty bundle and no included files.
    """
    result = build_context_from_file([])
    assert result["code_bundle"] == ""
    assert result["files_included"] == []


def test_build_context_from_pasted_code_returns_code():
    """
    Pasted code should be returned unchanged as the code bundle.
    """
    code = "def foo():\n    return 42"
    result = build_context_from_pasted_code(code)
    assert result["code_bundle"] == code


def test_build_context_from_pasted_code_files_included_empty():
    """
    Pasted code has no associated filenames, so files_included should be empty.
    """
    result = build_context_from_pasted_code("some code")
    assert result["files_included"] == []


def test_build_context_from_pasted_code_empty_string():
    """
    An empty paste should produce an empty code bundle.
    """
    result = build_context_from_pasted_code("")
    assert result["code_bundle"] == ""
