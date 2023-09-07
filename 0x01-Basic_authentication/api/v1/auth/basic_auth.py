#!/usr/bin/env python3
"""
    Module Author implemenation
"""
from .auth import Auth
import base64
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """
        BasicAuth class implementation
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header"""

        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):

            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decodes the Basic Authorization header value from Base64"""

        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):

            return None
        try:
            value = base64.b64decode(base64_authorization_header)
            return value.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Returns the user email and password from
        the Base64 decoded value
        """

        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ":" not in decoded_base64_authorization_header:

            return (None, None)
        else:
            email, pwd = decoded_base64_authorization_header.split(":", 1)
            return (email, pwd)

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Returns the user email and password from
        the Base64 decoded value
        """

        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ":" not in decoded_base64_authorization_header:

            return (None, None)
        else:
            email, pwd = decoded_base64_authorization_header.split(":", 1)
            return (email, pwd)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on their email and password
        """

        if user_email is None or not isinstance(user_email, str) or\
                user_pwd is None or not isinstance(user_pwd, str):

            return None
        try:
            from models.user import User
            users = User.search({"email": user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        req_auth_header = self.authorization_header(request)
        auth_header_base64 = self.extract_base64_authorization_header(
                                    req_auth_header)
        auth_header = self.decode_base64_authorization_header(
                                    auth_header_base64)
        email, pwd = self.extract_user_credentials(auth_header)
        user = self.user_object_from_credentials(email, pwd)
        return user