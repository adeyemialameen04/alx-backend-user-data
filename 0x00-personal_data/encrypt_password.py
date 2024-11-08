#!/usr/bin/env python3
""" encrypt password module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ method to has data using bcrypt"""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ function to validate that hashed pass
     matches password """
    return bcrypt.checkpw(password.encode(), hashed_password)
