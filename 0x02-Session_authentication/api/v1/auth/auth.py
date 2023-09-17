#!/usr/bin/env python3
"""
    Module Author implemenation
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
        Author class implementation
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is None or not excluded_paths:
            return True
        for excl_path in excluded_paths:
            if excl_path.endswith('*') and path.startswith(excl_path[:-1]):
                return False
            elif excl_path in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """that returns None - request will be the Flask request object

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is None:
            return None
        if request.headers.get('Authorization'):
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None