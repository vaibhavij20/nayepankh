"""
Tests for agent modules.
"""

import pytest
from agents.router_agent import route_query, router
from agents.mentor_agent import match_mentor, mentor_agent
from agents.faq_agent import answer_faq, faq_agent
from agents.report_agent import generate_report, report_agent
from agents.volunteer_agent import register_volunteer, volunteer_agent


class TestRouterAgent:
    """Test cases for router agent."""
    
    def test_route_mentor_query(self):
        """Test routing mentor-related queries."""
        assert route_query("I need a mentor for Python") == "Mentor"
        assert route_query("Find me a mentor") == "Mentor"
    
    def test_route_event_query(self):
        """Test routing event-related queries."""
        assert route_query("What events are coming up?") == "Event"
        assert route_query("Tell me about the workshop") == "Event"
    
    def test_route_volunteer_query(self):
        """Test routing volunteer-related queries."""
        assert route_query("How do I volunteer?") == "Volunteer"
        assert route_query("I want to sign up") == "Volunteer"
    
    def test_route_ngo_query(self):
        """Test routing NGO-related queries."""
        assert route_query("What does the NGO do?") == "NGO"
        assert route_query("Tell me about the foundation") == "NGO"
    
    def test_route_general_query(self):
        """Test routing general queries."""
        assert route_query("Hello") == "General"
        assert route_query("Random question") == "General"
    
    def test_route_empty_query(self):
        """Test routing empty query."""
        assert route_query("") == "General"
        assert route_query(None) == "General"
    
    def test_get_route_confidence(self):
        """Test getting route confidence score."""
        result = router.get_route_confidence("I need a mentor for Python")
        assert "route" in result
        assert "confidence" in result
        assert result["route"] == "Mentor"
        assert result["confidence"] >= 0.0


class TestMentorAgent:
    """Test cases for mentor agent."""
    
    def test_match_mentor_empty_database(self):
        """Test mentor matching with empty database."""
        result = match_mentor("Python")
        assert result is None
    
    def test_match_mentor_no_match(self):
        """Test mentor matching with no matching skill."""
        result = match_mentor("NonExistentSkill")
        assert result is None


class TestFAQAgent:
    """Test cases for FAQ agent."""
    
    def test_answer_volunteer_faq(self):
        """Test answering volunteer-related FAQ."""
        result = answer_faq("How do I volunteer?")
        assert result is not None
        assert "register" in result.lower()
    
    def test_answer_event_faq(self):
        """Test answering event-related FAQ."""
        result = answer_faq("What events are coming up?")
        assert result is not None
        assert "event" in result.lower()
    
    def test_answer_donate_faq(self):
        """Test answering donation-related FAQ."""
        result = answer_faq("How can I donate?")
        assert result is not None
        assert "donate" in result.lower()
    
    def test_answer_unknown_faq(self):
        """Test answering unknown FAQ."""
        result = answer_faq("Random question")
        assert result is None
    
    def test_answer_empty_faq(self):
        """Test answering empty FAQ."""
        result = answer_faq("")
        assert result is None


class TestReportAgent:
    """Test cases for report agent."""
    
    def test_generate_weekly_report(self):
        """Test generating weekly report."""
        report = generate_report()
        assert report is not None
        assert "NAYEPANKH" in report
        assert "WEEKLY REPORT" in report
    
    def test_generate_summary_report(self):
        """Test generating summary report."""
        report = report_agent.generate_summary_report()
        assert report is not None
        assert "NAYEPANKH" in report
        assert "SYSTEM SUMMARY" in report


class TestVolunteerAgent:
    """Test cases for volunteer agent."""
    
    def test_register_volunteer_invalid_email(self):
        """Test registering volunteer with invalid email."""
        result = volunteer_agent.register_volunteer("John", "invalid-email", "Python")
        assert result["success"] == False
    
    def test_register_volunteer_missing_fields(self):
        """Test registering volunteer with missing fields."""
        result = volunteer_agent.register_volunteer("", "", "")
        assert result["success"] == False
