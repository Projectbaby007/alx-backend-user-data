#!/usr/bin/env python3
"""Module used to encrypt passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """function used to encrypt passwords"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'), salt)

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if the password inserted matched the hashed password stored"""
    return bcrypt.checkpw(bytes(password, encoding='utf-8'), hashed_password)
