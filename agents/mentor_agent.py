"""
Mentor agent module for NayePankh AI Assistant.
Handles mentor matching with fuzzy matching and semantic search.
"""

import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
from difflib import SequenceMatcher
from database.db import get_all_volunteers, search_volunteers_by_skill
from logger import get_logger

logger = get_logger(__name__)


class MentorAgent:
    """Handles mentor matching with fuzzy matching capabilities."""
    
    def __init__(self):
        """Initialize the mentor agent."""
        self.similarity_threshold = 0.6
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings using SequenceMatcher.
        
        Args:
            str1: First string
            str2: Second string
        
        Returns:
            Similarity score between 0 and 1
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def _normalize_skill(self, skill: str) -> str:
        """
        Normalize skill string for matching.
        
        Args:
            skill: Skill string to normalize
        
        Returns:
            Normalized skill string
        """
        # Remove extra spaces and convert to lowercase
        normalized = " ".join(skill.lower().split())
        # Remove common suffixes/prefixes
        suffixes = ["ing", "ed", "er", "or", "tion", "sion"]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
        return normalized
    
    def match_mentor(self, skill: str, top_n: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Find mentors matching the requested skill with fuzzy matching.
        
        Args:
            skill: Skill to search for
            top_n: Maximum number of mentors to return
        
        Returns:
            List of matching mentors with similarity scores, or None if no matches
        """
        if not skill:
            logger.warning("Empty skill provided for mentor matching")
            return None
        
        try:
            # Get all volunteers
            volunteers = get_all_volunteers()
            
            if not volunteers:
                logger.warning("No volunteers found in database")
                return None
            
            # Normalize the search skill
            normalized_skill = self._normalize_skill(skill)
            
            # Calculate similarity scores for each volunteer
            matches = []
            for volunteer in volunteers:
                volunteer_skills = volunteer.get('skills', '')
                
                # Check for exact match first
                if normalized_skill in volunteer_skills.lower():
                    similarity = 1.0
                else:
                    # Calculate fuzzy similarity
                    similarity = self._calculate_similarity(normalized_skill, volunteer_skills)
                
                # Only include if similarity meets threshold
                if similarity >= self.similarity_threshold:
                    matches.append({
                        'id': volunteer.get('id'),
                        'name': volunteer.get('name'),
                        'email': volunteer.get('email'),
                        'skills': volunteer.get('skills'),
                        'similarity': similarity,
                        'created_at': volunteer.get('created_at')
                    })
            
            # Sort by similarity score (descending)
            matches.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Return top N matches
            top_matches = matches[:top_n] if matches else None
            
            if top_matches:
                logger.info(f"Found {len(top_matches)} mentor matches for skill: {skill}")
            else:
                logger.info(f"No mentor matches found for skill: {skill}")
            
            return top_matches
            
        except Exception as e:
            logger.error(f"Error matching mentor: {e}")
            return None
    
    def get_best_mentor(self, skill: str) -> Optional[Dict[str, Any]]:
        """
        Get the single best mentor match for a skill.
        
        Args:
            skill: Skill to search for
        
        Returns:
            Best matching mentor or None if no match
        """
        matches = self.match_mentor(skill, top_n=1)
        return matches[0] if matches else None


# Global mentor agent instance
mentor_agent = MentorAgent()

# Backward compatibility function
def match_mentor(skill: str) -> Optional[Dict[str, Any]]:
    """
    Find the best mentor matching the requested skill.
    
    Args:
        skill: Skill to search for
    
    Returns:
        Best matching mentor or None if no match
    """
    best_match = mentor_agent.get_best_mentor(skill)
    if best_match:
        # Return in the old format for backward compatibility
        return {
            'name': best_match['name'],
            'email': best_match['email']
        }
    return None