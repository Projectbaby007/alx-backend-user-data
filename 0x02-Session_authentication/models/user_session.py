#!/usr/bin/env python3

""" User sessions stored in a file
"""

from .base import Base


class UserSession(Base):
    """ Stores all sessions in a file
    """
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')