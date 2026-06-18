"""
Volunteer agent module for NayePankh AI Assistant.
Handles volunteer registration with validation and error handling.
"""

from typing import Dict, Any
from database.db import add_volunteer, get_volunteer_by_email
from utils.validators import validate_name, validate_email, validate_skills, sanitize_input
from logger import get_logger

logger = get_logger(__name__)


class VolunteerAgent:
    """Handles volunteer registration and management."""
    
    def register_volunteer(self, name: str, email: str, skills: str) -> Dict[str, Any]:
        """
        Register a new volunteer with validation.
        
        Args:
            name: Volunteer name
            email: Volunteer email
            skills: Volunteer skills
        
        Returns:
            Dictionary with success status and message
        """
        try:
            # Validate inputs
            validate_name(name)
            validate_email(email)
            validate_skills(skills)
            
            # Sanitize inputs
            sanitized_name = sanitize_input(name)
            sanitized_email = sanitize_input(email)
            sanitized_skills = sanitize_input(skills)
            
            # Check if volunteer already exists
            existing = get_volunteer_by_email(sanitized_email)
            if existing:
                logger.warning(f"Registration attempt with existing email: {sanitized_email}")
                return {
                    "success": False,
                    "message": "A volunteer with this email already exists",
                    "volunteer_id": None
                }
            
            # Add volunteer to database
            volunteer_id = add_volunteer(sanitized_name, sanitized_email, sanitized_skills)
            
            logger.info(f"Volunteer registered successfully: {sanitized_email} (ID: {volunteer_id})")
            
            return {
                "success": True,
                "message": "Volunteer Registered Successfully!",
                "volunteer_id": volunteer_id
            }
            
        except ValueError as e:
            logger.warning(f"Validation error during registration: {e}")
            return {
                "success": False,
                "message": str(e),
                "volunteer_id": None
            }
        except Exception as e:
            logger.error(f"Error registering volunteer: {e}")
            return {
                "success": False,
                "message": "An error occurred during registration. Please try again.",
                "volunteer_id": None
            }


# Global volunteer agent instance
volunteer_agent = VolunteerAgent()

# Backward compatibility function
def register_volunteer(name: str, email: str, skills: str) -> str:
    """
    Register a new volunteer.
    
    Args:
        name: Volunteer name
        email: Volunteer email
        skills: Volunteer skills
    
    Returns:
        Success message
    """
    result = volunteer_agent.register_volunteer(name, email, skills)
    return result["message"]