#!/usr/bin/env python3

""" Session authentication
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    """
    def create_session(self, user_id=None):
        """
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(
                            user_id=user_id,
                            session_id=session_id
                            )
        return session_id