#!/usr/bin/env python3
"""set expiry for session"""
import datetime
import os
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """sets expiry for session"""
    def __init__(self):
        self.session_duration = int(os.getenv('SESSION_DURATION', '0'))

    def create_session(self, user_id=None):
        """creates session based on userid"""
        get_session_id = super().create_session(user_id)
        if get_session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.datetime.now()}  # noqa
        self.user_id_by_session_id[get_session_id] = session_dictionary
        return get_session_id

    def user_id_for_session_id(self, session_id=None):
        """get user based on session id"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        get_user = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return get_user.get('user_id')
        if get_user.get('created_at') is None:
            return None
        expires_at = get_user.get('created_at') + datetime.timedelta(seconds=self.session_duration)  # noqa
        if datetime.datetime.now() > expires_at:
            return None
        return get_user.get('user_id')
