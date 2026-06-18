"""
Tests for database operations.
"""

import pytest
import os
import tempfile
from database.db import (
    init_db,
    add_volunteer,
    get_all_volunteers,
    get_volunteer_by_email,
    get_volunteer_by_id,
    update_volunteer,
    delete_volunteer,
    get_volunteer_count,
    search_volunteers_by_skill
)


class TestDatabase:
    """Test cases for database operations."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        # Use a temporary database file
        original_db = "volunteers.db"
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        temp_db.close()
        
        # Temporarily change the database path
        import database.db as db_module
        original_path = db_module.Config.DATABASE_PATH
        db_module.Config.DATABASE_PATH = temp_db.name
        
        # Initialize the database
        init_db()
        
        yield temp_db.name
        
        # Cleanup
        os.unlink(temp_db.name)
        db_module.Config.DATABASE_PATH = original_path
        if os.path.exists(original_db):
            os.unlink(original_db)
    
    def test_init_db(self, temp_db):
        """Test database initialization."""
        assert os.path.exists(temp_db)
    
    def test_add_volunteer(self, temp_db):
        """Test adding a volunteer."""
        volunteer_id = add_volunteer("John Doe", "john@example.com", "Python, Teaching")
        assert volunteer_id > 0
    
    def test_add_duplicate_volunteer(self, temp_db):
        """Test adding duplicate volunteer (same email)."""
        add_volunteer("John Doe", "john@example.com", "Python")
        with pytest.raises(ValueError):
            add_volunteer("Jane Doe", "john@example.com", "Teaching")
    
    def test_get_all_volunteers(self, temp_db):
        """Test retrieving all volunteers."""
        add_volunteer("John Doe", "john@example.com", "Python")
        add_volunteer("Jane Doe", "jane@example.com", "Teaching")
        
        volunteers = get_all_volunteers()
        assert len(volunteers) == 2
    
    def test_get_volunteer_by_email(self, temp_db):
        """Test retrieving volunteer by email."""
        add_volunteer("John Doe", "john@example.com", "Python")
        
        volunteer = get_volunteer_by_email("john@example.com")
        assert volunteer is not None
        assert volunteer["name"] == "John Doe"
    
    def test_get_volunteer_by_id(self, temp_db):
        """Test retrieving volunteer by ID."""
        volunteer_id = add_volunteer("John Doe", "john@example.com", "Python")
        
        volunteer = get_volunteer_by_id(volunteer_id)
        assert volunteer is not None
        assert volunteer["name"] == "John Doe"
    
    def test_update_volunteer(self, temp_db):
        """Test updating volunteer information."""
        volunteer_id = add_volunteer("John Doe", "john@example.com", "Python")
        
        success = update_volunteer(volunteer_id, name="John Smith")
        assert success == True
        
        volunteer = get_volunteer_by_id(volunteer_id)
        assert volunteer["name"] == "John Smith"
    
    def test_delete_volunteer(self, temp_db):
        """Test deleting a volunteer."""
        volunteer_id = add_volunteer("John Doe", "john@example.com", "Python")
        
        success = delete_volunteer(volunteer_id)
        assert success == True
        
        volunteer = get_volunteer_by_id(volunteer_id)
        assert volunteer is None
    
    def test_get_volunteer_count(self, temp_db):
        """Test getting volunteer count."""
        add_volunteer("John Doe", "john@example.com", "Python")
        add_volunteer("Jane Doe", "jane@example.com", "Teaching")
        
        count = get_volunteer_count()
        assert count == 2
    
    def test_search_volunteers_by_skill(self, temp_db):
        """Test searching volunteers by skill."""
        add_volunteer("John Doe", "john@example.com", "Python, Teaching")
        add_volunteer("Jane Doe", "jane@example.com", "Teaching, Mentoring")
        
        results = search_volunteers_by_skill("Python")
        assert len(results) == 1
        assert results[0]["name"] == "John Doe"
