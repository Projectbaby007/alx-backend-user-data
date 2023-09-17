#!/usr/bin/env python3
"""Session authentication"""

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Authentication
    """
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session_id for user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self,
            session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        """
        from models.user import User

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        """
        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]
        return True