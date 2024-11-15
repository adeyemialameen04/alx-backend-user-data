#!/usr/bin/env python3
"""session auth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """session db auth"""

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        usersession = UserSession(session_id=session_id, user_id=user_id)
        usersession.save()
        return session_id
    
    def user_id_for_session_id(self, session_id=None):
        """user id for session"""
        get_session = UserSession.search({'session_id': session_id})
        if get_session is None:
            return None
        return super().user_id_for_session_id(session_id)
    
    def destroy_session(self, request=None) -> bool:
        """destroy session from database"""
        if request is None:
            return False
        get_sessionid = self.session_cookie(request)
        if get_sessionid is None:
            return False
        get_session = UserSession.search({'session_id': get_sessionid})
        if get_session is None:
            return False
        get_session[0].remove()
        return True
