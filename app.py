"""
NayePankh AI Assistant - Main Streamlit Application
AI-powered NGO Volunteer Management System
"""

import streamlit as st
import sqlite3
import pandas as pd
import uuid

import google.generativeai as genai

from database.db import (
    init_db,
    add_volunteer,
    get_all_volunteers
)

from agents.router_agent import (
    route_query
)

from agents.mentor_agent import (
    match_mentor
)

from agents.report_agent import (
    generate_report
)

from utils.email_service import (
    send_welcome_email
)

from memory_manager import (
    memory_manager
)

from config import Config
from logger import get_logger
from utils.validators import (
    validate_name,
    validate_email,
    validate_skills,
    validate_query,
    validate_mentor_skill,
    sanitize_input
)

logger = get_logger(__name__)

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout=Config.APP_LAYOUT
)

# ==================================
# DATABASE INIT
# ==================================

try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    st.error(f"Failed to initialize database: {str(e)}")
    st.warning("The application will continue with limited functionality.")

# ==================================
# SESSION STATE
# ==================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==================================
# TITLE
# ==================================

st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")

# ==================================
# GEMINI API CONFIGURATION
# ==================================

st.sidebar.header("⚙️ Settings")

# Get API key from config or sidebar input
api_key = Config.GEMINI_API_KEY

if not api_key:
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Generative AI API key"
    )

if not api_key:
    st.sidebar.warning("⚠️ Please enter Gemini API Key to use the AI assistant")
    st.info("Get your API key from: https://makersuite.google.com/app/apikey")
    st.stop()

# Configure Gemini API
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)
    logger.info(f"Gemini API configured with model: {Config.GEMINI_MODEL}")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    st.sidebar.error(f"Failed to configure Gemini API: {e}")
    st.sidebar.warning("Chat functionality will be disabled. Please check your API key.")
    model = None

# ==================================
# SIDEBAR NAVIGATION
# ==================================

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Assistant",
        "Admin Dashboard"
    ]
)

# ==================================
# VOLUNTEER REGISTRATION
# ==================================

st.sidebar.divider()

st.sidebar.header("👤 Volunteer Registration")

name = st.sidebar.text_input("Name", placeholder="Enter your name")
email = st.sidebar.text_input("Email", placeholder="Enter your email")
skills = st.sidebar.text_area("Skills", placeholder="e.g., Python, Teaching, Mentoring", height=100)

if st.sidebar.button("Register Volunteer", use_container_width=True):
    try:
        if name and email and skills:
            # Validate inputs
            validate_name(name)
            validate_email(email)
            validate_skills(skills)
            
            # Sanitize inputs
            sanitized_name = sanitize_input(name)
            sanitized_email = sanitize_input(email)
            sanitized_skills = sanitize_input(skills)
            
            # Add volunteer
            add_volunteer(sanitized_name, sanitized_email, sanitized_skills)
            
            # Send welcome email
            try:
                send_welcome_email(sanitized_name, sanitized_email)
                st.sidebar.success("✅ Volunteer Registered Successfully! Welcome email sent.")
            except Exception as e:
                logger.warning(f"Email failed: {e}")
                st.sidebar.success("✅ Volunteer Registered Successfully! (Email notification failed)")
        else:
            st.sidebar.error("❌ Please fill all required fields")
    except ValueError as e:
        st.sidebar.error(f"❌ {e}")
    except Exception as e:
        logger.error(f"Registration error: {e}")
        st.sidebar.error("❌ Registration failed. Please try again.")

# ==================================
# MENTOR MATCHING
# ==================================

st.sidebar.divider()

st.sidebar.header("🎓 Mentor Matching")

mentor_skill = st.sidebar.text_input("Required Skill", placeholder="e.g., Python, Teaching")

if st.sidebar.button("Find Mentor", use_container_width=True):
    try:
        if mentor_skill:
            validate_mentor_skill(mentor_skill)
            sanitized_skill = sanitize_input(mentor_skill)
            
            mentor = match_mentor(sanitized_skill)
            
            if mentor:
                st.sidebar.success(f"""
                ✅ **Mentor Found**
                
                **Name:** {mentor['name']}
                **Email:** {mentor['email']}
                """)
            else:
                st.sidebar.warning("⚠️ No mentor found with that skill")
        else:
            st.sidebar.error("❌ Please enter a skill to search")
    except ValueError as e:
        st.sidebar.error(f"❌ {e}")
    except Exception as e:
        logger.error(f"Mentor matching error: {e}")
        st.sidebar.error("❌ Mentor matching failed. Please try again.")

# ==================================
# ADMIN DASHBOARD
# ==================================

if page == "Admin Dashboard":
    if not st.session_state.admin_logged_in:
        st.header("🔐 Admin Login")
        
        username = st.text_input("Username", placeholder="Enter admin username")
        password = st.text_input("Password", type="password", placeholder="Enter admin password")
        
        if st.button("Login", use_container_width=True):
            try:
                if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login Successful")
                    logger.info(f"Admin login successful: {username}")
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials")
                    logger.warning(f"Failed admin login attempt: {username}")
            except Exception as e:
                logger.error(f"Login error: {e}")
                st.error("❌ Login failed. Please try again.")
        
        st.stop()
    
    st.header("📊 Volunteer Dashboard")
    
    try:
        # Get volunteer data
        volunteers = get_all_volunteers()
        df = pd.DataFrame(volunteers)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Volunteers", len(df))
        
        with col2:
            skill_count = df["skills"].nunique() if len(df) > 0 else 0
            st.metric("Unique Skills", skill_count)
        
        with col3:
            # Get memory count
            memory_count = memory_manager.get_memory_count()
            st.metric("Memory Entries", memory_count)
        
        # Volunteer Records
        st.subheader("Volunteer Records")
        
        if len(df) > 0:
            st.dataframe(df, use_container_width=True)
            
            # Skills Distribution
            st.subheader("Skills Distribution")
            st.bar_chart(df["skills"].value_counts())
            
            # CSV Export
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇ Download CSV",
                data=csv,
                file_name="volunteers.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No volunteer records found")
        
        # Weekly Report
        st.subheader("Weekly Report")
        
        try:
            report = generate_report()
            st.download_button(
                label="📄 Download Report",
                data=report,
                file_name="weekly_report.txt",
                use_container_width=True
            )
        except Exception as e:
            logger.error(f"Report generation error: {e}")
            st.error("Failed to generate report")
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.success("Logged out successfully")
            logger.info("Admin logged out")
            st.rerun()
        
        st.stop()
    
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        st.error("Failed to load dashboard. Please check the logs.")

# ==================================
# CHAT HISTORY
# ==================================

# Clear chat history on page refresh to prevent duplicate messages
if "chat_initialized" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_initialized = True

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==================================
# CHAT INPUT
# ==================================

query = st.chat_input("Ask NayePankh AI Assistant...")

if query:
    try:
        # Check if model is available
        if model is None:
            st.error("Chat functionality is not available. Please configure a valid Gemini API key.")
            st.stop()
        
        # Validate query
        validate_query(query)
        sanitized_query = sanitize_input(query)
        
        # Add user message to session state
        st.session_state.messages.append({
            "role": "user",
            "content": sanitized_query
        })
        
        # Add to memory
        try:
            memory_manager.add_memory(sanitized_query)
        except Exception as e:
            logger.warning(f"Memory addition failed: {e}")
        
        # Retrieve relevant memories
        try:
            memories = memory_manager.query_memory(sanitized_query, n_results=3)
        except Exception as e:
            logger.warning(f"Memory query failed: {e}")
            memories = []
        
        # Route query to appropriate agent
        agent = route_query(sanitized_query)
        
        # Display user message
        with st.chat_message("user"):
            st.write(sanitized_query)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    prompt = f"""
You are NayePankh Foundation AI Assistant.

Agent: {agent}

Previous Context: {memories}

Responsibilities:
- Help volunteers with registration and questions
- Guide students with career and educational guidance
- Explain NGO activities and programs
- Provide event information and schedules
- Answer beneficiary questions
- Be helpful, friendly, and professional

User Question: {sanitized_query}
"""
                    
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=Config.GEMINI_TEMPERATURE,
                            max_output_tokens=Config.GEMINI_MAX_TOKENS,
                            timeout=Config.GEMINI_TIMEOUT
                        )
                    )
                    
                    answer = response.text
                    st.write(answer)
                    
                    # Add assistant response to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    logger.info(f"AI response generated for query: {sanitized_query[:50]}...")
                
                except Exception as e:
                    logger.error(f"AI generation error: {e}")
                    st.error("I apologize, but I encountered an error generating a response. Please try again.")
    
    except ValueError as e:
        st.error(f"❌ {e}")
    except Exception as e:
        logger.error(f"Chat error: {e}")
        st.error("An error occurred. Please try again.")

