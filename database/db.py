"""
Database module for NayePankh AI Assistant.
Handles all database operations with proper error handling and security.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from datetime import datetime
from config import Config
from logger import get_logger

logger = get_logger(__name__)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and cleanup.
    """
    conn = None
    try:
        conn = sqlite3.connect(
            Config.DATABASE_PATH,
            timeout=Config.DB_TIMEOUT
        )
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def init_db() -> None:
    """
    Initialize the database with proper schema, indexes, and constraints.
    Creates tables if they don't exist and adds necessary indexes.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create volunteers table with constraints
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS volunteers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK(length(name) >= 2),
                    email TEXT NOT NULL UNIQUE,
                    skills TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_volunteers_email 
                ON volunteers(email)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_volunteers_skills 
                ON volunteers(skills)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_volunteers_created_at 
                ON volunteers(created_at)
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
            
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise


def add_volunteer(name: str, email: str, skills: str) -> int:
    """
    Add a new volunteer to the database.
    
    Args:
        name: Volunteer name
        email: Volunteer email (must be unique)
        skills: Volunteer skills
    
    Returns:
        ID of the inserted volunteer
    
    Raises:
        sqlite3.IntegrityError: If email already exists
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO volunteers (name, email, skills, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, email, skills, datetime.now(), datetime.now())
            )
            conn.commit()
            volunteer_id = cursor.lastrowid
            logger.info(f"Volunteer added successfully: {email} (ID: {volunteer_id})")
            return volunteer_id
            
    except sqlite3.IntegrityError as e:
        logger.warning(f"Duplicate email attempt: {email}")
        raise ValueError("A volunteer with this email already exists")
    except sqlite3.Error as e:
        logger.error(f"Error adding volunteer: {e}")
        raise


def get_all_volunteers(limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Retrieve all volunteers from the database.
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        List of volunteer dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM volunteers ORDER BY created_at DESC"
            params = []
            
            if limit:
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            volunteers = [dict(row) for row in rows]
            logger.debug(f"Retrieved {len(volunteers)} volunteers")
            return volunteers
            
    except sqlite3.Error as e:
        logger.error(f"Error retrieving volunteers: {e}")
        raise


def get_volunteer_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a volunteer by email address.
    
    Args:
        email: Volunteer email address
    
    Returns:
        Volunteer dictionary or None if not found
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM volunteers WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            
            if row:
                logger.debug(f"Volunteer found: {email}")
                return dict(row)
            return None
            
    except sqlite3.Error as e:
        logger.error(f"Error retrieving volunteer by email: {e}")
        raise


def get_volunteer_by_id(volunteer_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a volunteer by ID.
    
    Args:
        volunteer_id: Volunteer ID
    
    Returns:
        Volunteer dictionary or None if not found
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM volunteers WHERE id = ?",
                (volunteer_id,)
            )
            row = cursor.fetchone()
            
            if row:
                logger.debug(f"Volunteer found: ID {volunteer_id}")
                return dict(row)
            return None
            
    except sqlite3.Error as e:
        logger.error(f"Error retrieving volunteer by ID: {e}")
        raise


def update_volunteer(volunteer_id: int, name: Optional[str] = None, 
                    email: Optional[str] = None, skills: Optional[str] = None) -> bool:
    """
    Update volunteer information.
    
    Args:
        volunteer_id: Volunteer ID
        name: New name (optional)
        email: New email (optional)
        skills: New skills (optional)
    
    Returns:
        True if update was successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if email:
                updates.append("email = ?")
                params.append(email)
            if skills:
                updates.append("skills = ?")
                params.append(skills)
            
            if not updates:
                logger.warning("No fields to update")
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.now())
            params.append(volunteer_id)
            
            query = f"UPDATE volunteers SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            logger.info(f"Volunteer updated: ID {volunteer_id}")
            return cursor.rowcount > 0
            
    except sqlite3.Error as e:
        logger.error(f"Error updating volunteer: {e}")
        raise


def delete_volunteer(volunteer_id: int) -> bool:
    """
    Delete a volunteer from the database.
    
    Args:
        volunteer_id: Volunteer ID
    
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM volunteers WHERE id = ?",
                (volunteer_id,)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Volunteer deleted: ID {volunteer_id}")
                return True
            logger.warning(f"Volunteer not found for deletion: ID {volunteer_id}")
            return False
            
    except sqlite3.Error as e:
        logger.error(f"Error deleting volunteer: {e}")
        raise


def get_volunteer_count() -> int:
    """
    Get the total count of volunteers.
    
    Returns:
        Number of volunteers
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM volunteers")
            count = cursor.fetchone()[0]
            logger.debug(f"Volunteer count: {count}")
            return count
            
    except sqlite3.Error as e:
        logger.error(f"Error getting volunteer count: {e}")
        raise


def search_volunteers_by_skill(skill: str) -> List[Dict[str, Any]]:
    """
    Search for volunteers by skill (case-insensitive).
    
    Args:
        skill: Skill to search for
    
    Returns:
        List of matching volunteer dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM volunteers WHERE LOWER(skills) LIKE LOWER(?)",
                (f"%{skill}%",)
            )
            rows = cursor.fetchall()
            
            volunteers = [dict(row) for row in rows]
            logger.debug(f"Found {len(volunteers)} volunteers with skill: {skill}")
            return volunteers
            
    except sqlite3.Error as e:
        logger.error(f"Error searching volunteers by skill: {e}")
        raise