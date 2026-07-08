"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: base.py
Purpose: Base Database Model
----------------------------------------------------------
"""

from app.utils.db_helper import get_db_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseModel:
    """
    Base model providing common database operations.

    All other model classes should inherit from this class.
    """

    @staticmethod
    def execute_query(query, params=None):
        """
        Execute INSERT, UPDATE, DELETE queries.

        Returns:
            lastrowid (int) on success
            None on failure
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            connection.commit()

            return cursor.lastrowid

        except Exception as error:
            logger.exception(
                "Database Execute Error: %s",
                error
            )

            # Safely attempt rollback - connection may be broken
            if connection:
                try:
                    connection.rollback()
                except Exception:
                    logger.exception("Rollback also failed (connection may be lost)")
                    # Do NOT let rollback exceptions propagate and mask the original error
                    pass

            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    @staticmethod
    def fetch_one(query, params=None):
        """
        Execute SELECT query.

        Returns one record.
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchone()

        except Exception as error:
            logger.exception(
                "Database Fetch One Error: %s",
                error
            )

            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    @staticmethod
    def fetch_all(query, params=None):
        """
        Execute SELECT query.

        Returns multiple records.
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()

        except Exception as error:
            logger.exception(
                "Database Fetch All Error: %s",
                error
            )

            return []

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:
                try:
                    connection.close()
                except Exception:
                    pass