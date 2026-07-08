"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: db_helper.py
Purpose: Centralized MySQL Database Connection Manager
----------------------------------------------------------
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

from app.utils.logger import app_logger

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """
    Centralized MySQL Database Connection Class.
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Establish MySQL database connection.
        """

        try:
            if self.connection is None or not self.connection.is_connected():

                self.connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=int(os.getenv("DB_PORT")),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                    autocommit=False
                )

                app_logger.info("Database connection established.")

            return self.connection

        except Error as error:
            app_logger.error(f"Database Connection Error : {error}")
            raise

    def get_cursor(self, dictionary=True):
        """
        Returns MySQL cursor.
        """

        connection = self.connect()
        return connection.cursor(dictionary=dictionary)

    def commit(self):
        """
        Commit current transaction.
        """

        if self.connection and self.connection.is_connected():
            self.connection.commit()

    def rollback(self):
        """
        Rollback current transaction.
        """

        if self.connection and self.connection.is_connected():
            self.connection.rollback()

    def close(self):
        """
        Close database connection.
        """

        if self.connection and self.connection.is_connected():
            self.connection.close()
            app_logger.info("Database connection closed.")


# ==========================================================
# Global Database Object
# ==========================================================

db = DatabaseConnection()


# ==========================================================
# Compatibility Helper
# ==========================================================

def get_db_connection():
    """
    Returns an active MySQL connection.

    This function is used by BaseModel.
    """
    return db.connect()