#!/usr/bin/env python3
""" End-to-end integration test."""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """ Test Register user."""
    url = f"{BASE_URL}/users"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests loging with in wrong password."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Tests log in method."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """ Tests information when profile logged out."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Tests information when profile is logged in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url, cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["email"] == "guillaume@holberton.io"


def log_out(session_id: str) -> None:
    """ Tests logging out of a session."""
    url = f"{BASE_URL}/sessions"
    response = requests.delete(url, cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Bienvenue"


def reset_password_token(email: str) -> str:
    """ Tests requesting a password reset token."""
    url = f"{BASE_URL}/reset_password"
    response = requests.post(url, data={"email": email})
    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == email
    assert "reset_token" in payload

    return payload["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests the updating of user's password."""
    url = f"{BASE_URL}/reset_password"
    response = requests.put(url, data={
                "email": email,
                "reset_token": reset_token,
                "new_password": new_password
                })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
