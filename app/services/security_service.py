"""
----------------------------------------------------------
Security Service (SAFE FIX VERSION)
Supports both plain text + hashed passwords
----------------------------------------------------------
"""

import bcrypt
import time


class SecurityService:

    failed_attempts = 0
    lock_time = 0

    # ==========================================
    # PASSWORD HASH
    # ==========================================
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    # ==========================================
    # VERIFY PASSWORD (FIXED)
    # ==========================================
    @staticmethod
    def verify_password(password: str, stored_password: str) -> bool:
        """
        Works for BOTH:
        - plain text (your current DB)
        - bcrypt hashed passwords (future safe)
        """

        # CASE 1: bcrypt hash
        if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
            return bcrypt.checkpw(
                password.encode('utf-8'),
                stored_password.encode('utf-8')
            )

        # CASE 2: plain text (current DB)
        return password == stored_password

    # ==========================================
    # LOGIN ATTEMPT CONTROL (SAFE SIMPLE)
    # ==========================================
    @staticmethod
    def is_account_locked():
        return time.time() < SecurityService.lock_time

    @staticmethod
    def remaining_lock_time():
        return int(SecurityService.lock_time - time.time())

    @staticmethod
    def record_failed_attempt():
        SecurityService.failed_attempts += 1

        if SecurityService.failed_attempts >= 5:
            SecurityService.lock_time = time.time() + 60  # 1 min lock
            SecurityService.failed_attempts = 0

    @staticmethod
    def reset_login_attempts():
        SecurityService.failed_attempts = 0
        SecurityService.lock_time = 0

    @staticmethod
    def clear_csrf_token():
        pass