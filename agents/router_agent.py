"""
Router agent module for NayePankh AI Assistant.
Routes user queries to appropriate agents based on intent classification.
"""

from typing import Optional, Dict, Any
from logger import get_logger

logger = get_logger(__name__)


class RouterAgent:
    """Routes queries to appropriate agents with intent classification."""
    
    # Intent patterns with weights for confidence scoring
    INTENT_PATTERNS = {
        "Mentor": {
            "keywords": ["mentor", "guidance", "teach", "coach", "advisor", "training"],
            "weight": 1.0
        },
        "Event": {
            "keywords": ["event", "workshop", "seminar", "session", "meeting", "schedule"],
            "weight": 1.0
        },
        "Volunteer": {
            "keywords": ["volunteer", "register", "sign up", "join", "participate", "help"],
            "weight": 1.0
        },
        "NGO": {
            "keywords": ["ngo", "organization", "foundation", "mission", "vision", "about"],
            "weight": 0.8
        },
        "Donation": {
            "keywords": ["donate", "contribution", "fund", "support", "charity"],
            "weight": 0.9
        },
        "FAQ": {
            "keywords": ["faq", "question", "how", "what", "why", "when", "where"],
            "weight": 0.5
        }
    }
    
    def __init__(self):
        """Initialize the router agent."""
        self.fallback_route = "General"
    
    def route_query(self, query: str) -> str:
        """
        Route a query to the appropriate agent based on intent classification.
        
        Args:
            query: User query string
        
        Returns:
            Route name (agent type)
        """
        if not query or not isinstance(query, str):
            logger.warning("Invalid query provided to router")
            return self.fallback_route
        
        try:
            query_lower = query.lower()
            
            # Calculate confidence scores for each intent
            scores = {}
            for intent, config in self.INTENT_PATTERNS.items():
                score = 0
                for keyword in config["keywords"]:
                    if keyword in query_lower:
                        score += config["weight"]
                scores[intent] = score
            
            # Find the intent with highest score
            max_score = max(scores.values())
            
            if max_score > 0:
                # Get all intents with the max score (handle ties)
                best_intents = [intent for intent, score in scores.items() if score == max_score]
                
                # Return the first best intent
                selected_route = best_intents[0]
                logger.debug(f"Query routed to: {selected_route} (score: {max_score})")
                return selected_route
            
            # No intent matched, use fallback
            logger.debug(f"No intent matched, using fallback: {self.fallback_route}")
            return self.fallback_route
            
        except Exception as e:
            logger.error(f"Error routing query: {e}")
            return self.fallback_route
    
    def get_route_confidence(self, query: str) -> Dict[str, Any]:
        """
        Get the route and confidence score for a query.
        
        Args:
            query: User query string
        
        Returns:
            Dictionary with route and confidence score
        """
        if not query or not isinstance(query, str):
            return {"route": self.fallback_route, "confidence": 0.0}
        
        try:
            query_lower = query.lower()
            
            # Calculate confidence scores
            scores = {}
            for intent, config in self.INTENT_PATTERNS.items():
                score = 0
                for keyword in config["keywords"]:
                    if keyword in query_lower:
                        score += config["weight"]
                scores[intent] = score
            
            max_score = max(scores.values())
            best_intents = [intent for intent, score in scores.items() if score == max_score]
            
            # Normalize confidence score (0-1)
            normalized_confidence = min(max_score / 2.0, 1.0) if max_score > 0 else 0.0
            
            return {
                "route": best_intents[0] if best_intents else self.fallback_route,
                "confidence": normalized_confidence,
                "all_scores": scores
            }
            
        except Exception as e:
            logger.error(f"Error calculating route confidence: {e}")
            return {"route": self.fallback_route, "confidence": 0.0}


# Global router instance
router = RouterAgent()

# Backward compatibility function
def route_query(query: str) -> str:
    """
    Route a query to the appropriate agent.
    
    Args:
        query: User query string
    
    Returns:
        Route name (agent type)
    """
    return router.route_query(query)