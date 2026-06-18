"""
FAQ agent module for NayePankh AI Assistant.
Handles frequently asked questions with improved responses.
"""

from typing import Optional, Dict, Any
from logger import get_logger

logger = get_logger(__name__)


class FAQAgent:
    """Handles frequently asked questions with structured responses."""
    
    # FAQ knowledge base
    FAQ_KNOWLEDGE_BASE = {
        "volunteer": {
            "keywords": ["volunteer", "register", "sign up", "join", "participate"],
            "response": """
            **Volunteer Registration**
            
            You can register as a volunteer through the registration form in the sidebar. 
            Simply provide your name, email, and skills to get started.
            
            **Benefits of Volunteering:**
            - Make a positive impact in your community
            - Develop new skills and gain experience
            - Network with like-minded individuals
            - Receive mentorship opportunities
            
            After registration, you'll receive a welcome email with next steps.
            """
        },
        "event": {
            "keywords": ["event", "workshop", "seminar", "session", "meeting", "schedule"],
            "response": """
            **Upcoming Events**
            
            **Career Guidance Session**
            - Date: Every Saturday
            - Time: 10:00 AM - 12:00 PM
            - Location: Virtual (Zoom)
            - Topic: Career planning and skill development
            
            **Volunteer Orientation**
            - Date: First Sunday of every month
            - Time: 2:00 PM - 4:00 PM
            - Location: NayePankh Foundation Office
            - Topic: Introduction to our programs and activities
            
            To register for events, please contact us through the chat assistant.
            """
        },
        "donate": {
            "keywords": ["donate", "contribution", "fund", "support", "charity"],
            "response": """
            **Donation Information**
            
            Thank you for your interest in supporting NayePankh Foundation!
            
            **Ways to Donate:**
            1. **Online Donation**: Visit our website (coming soon)
            2. **Bank Transfer**: Contact us for bank details
            3. **In-Kind Donation**: Books, educational materials, equipment
            
            **Donation Usage:**
            - Educational programs for underprivileged children
            - Skill development workshops
            - Community outreach initiatives
            - Operational expenses
            
            For detailed donation information and tax benefits, please email us at: donate@nayepankh.org
            """
        },
        "contact": {
            "keywords": ["contact", "reach", "email", "phone", "address"],
            "response": """
            **Contact Information**
            
            **Email:** info@nayepankh.org
            **Phone:** +91-XXXXXXXXXX
            **Address:** NayePankh Foundation Office, [City], [State]
            
            **Office Hours:**
            Monday - Friday: 9:00 AM - 6:00 PM
            Saturday: 10:00 AM - 2:00 PM
            Sunday: Closed
            
            For urgent matters, please use the chat assistant or email us directly.
            """
        },
        "mentor": {
            "keywords": ["mentor", "guidance", "teach", "coach", "advisor"],
            "response": """
            **Mentorship Program**
            
            Our mentorship program connects volunteers with experienced professionals in their field of interest.
            
            **How it Works:**
            1. Register as a volunteer with your skills
            2. Use the "Mentor Matching" feature in the sidebar
            3. Get matched with a mentor based on your skills
            4. Schedule mentorship sessions
            
            **Mentorship Areas:**
            - Career guidance
            - Skill development
            - Academic support
            - Professional networking
            
            To find a mentor, use the Mentor Matching feature in the sidebar.
            """
        }
    }
    
    def answer_faq(self, query: str) -> Optional[str]:
        """
        Answer a frequently asked question based on the query.
        
        Args:
            query: User query string
        
        Returns:
            FAQ response or None if no match found
        """
        if not query:
            logger.warning("Empty query provided to FAQ agent")
            return None
        
        try:
            query_lower = query.lower()
            
            # Check each FAQ category
            for category, config in self.FAQ_KNOWLEDGE_BASE.items():
                for keyword in config["keywords"]:
                    if keyword in query_lower:
                        logger.debug(f"FAQ matched: {category}")
                        return config["response"]
            
            # No match found
            logger.debug(f"No FAQ match for query: {query[:50]}...")
            return None
            
        except Exception as e:
            logger.error(f"Error answering FAQ: {e}")
            return None


# Global FAQ agent instance
faq_agent = FAQAgent()

# Backward compatibility function
def answer_faq(query: str) -> Optional[str]:
    """
    Answer a frequently asked question.
    
    Args:
        query: User query string
    
    Returns:
        FAQ response or None if no match found
    """
    return faq_agent.answer_faq(query)