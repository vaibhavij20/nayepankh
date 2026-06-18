"""
Input validation module for NayePankh AI Assistant.
Provides validation functions for user inputs.
"""

import re
from typing import Optional, List
from logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    """
    if not email:
        raise ValidationError("Email is required")
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
    
    return True


def validate_name(name: str) -> bool:
    """
    Validate name format.
    
    Args:
        name: Name to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    """
    if not name:
        raise ValidationError("Name is required")
    
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters")
    
    if len(name) > 100:
        raise ValidationError("Name must be less than 100 characters")
    
    # Allow only letters, spaces, and common name characters
    if not re.match(r'^[a-zA-Z\s\-\'\.]+$', name):
        raise ValidationError("Name contains invalid characters")
    
    return True


def validate_skills(skills: str) -> bool:
    """
    Validate skills input.
    
    Args:
        skills: Skills string to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    """
    if not skills:
        raise ValidationError("Skills are required")
    
    if len(skills) > 1000:
        raise ValidationError("Skills must be less than 1000 characters")
    
    return True


def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks.
    
    Args:
        input_string: Input string to sanitize
    
    Returns:
        Sanitized string
    """
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_string)
    
    # Remove SQL injection patterns
    sql_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|ALTER)\b)',
        r'(;\s*(DROP|DELETE|UPDATE|INSERT))',
        r'(--|#|\/\*|\*\/)',
    ]
    
    for pattern in sql_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def validate_query(query: str) -> bool:
    """
    Validate user query for chat interface.
    
    Args:
        query: Query string to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    """
    if not query:
        raise ValidationError("Query cannot be empty")
    
    if len(query) > 2000:
        raise ValidationError("Query must be less than 2000 characters")
    
    # Check for prompt injection patterns
    injection_patterns = [
        r'ignore\s+(all\s+)?(previous\s+)?instructions',
        r'system\s*:\s*ignore',
        r'override\s+(all\s+)?(previous\s+)?',
        r'forget\s+(all\s+)?(previous\s+)?',
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            logger.warning(f"Potential prompt injection detected: {query[:100]}")
            raise ValidationError("Invalid query format")
    
    return True


def validate_mentor_skill(skill: str) -> bool:
    """
    Validate mentor skill search input.
    
    Args:
        skill: Skill to search for
    
    Returns:
        True if valid, raises ValidationError if invalid
    """
    if not skill:
        raise ValidationError("Skill is required")
    
    if len(skill) > 100:
        raise ValidationError("Skill must be less than 100 characters")
    
    return True


def validate_admin_credentials(username: str, password: str) -> bool:
    """
    Validate admin login credentials format.
    
    Args:
        username: Admin username
        password: Admin password
    
    Returns:
        True if format is valid
    """
    if not username or not password:
        raise ValidationError("Username and password are required")
    
    if len(username) > 50:
        raise ValidationError("Username too long")
    
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    
    return True
