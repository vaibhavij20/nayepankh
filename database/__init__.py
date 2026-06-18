"""
Database module for NayePankh AI Assistant.
Handles all database operations including initialization and volunteer management.
"""

from database.db import init_db, add_volunteer, get_all_volunteers, get_volunteer_by_email, update_volunteer, delete_volunteer

__all__ = [
    "init_db",
    "add_volunteer",
    "get_all_volunteers",
    "get_volunteer_by_email",
    "update_volunteer",
    "delete_volunteer",
]
