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
    get_all_volunteers,
    update_volunteer,
    delete_volunteer,
    get_volunteer_by_id
)

from agents.router_agent import route_query
from agents.mentor_agent import match_mentor
from agents.report_agent import generate_report
from memory_manager import memory_manager
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
model = None
try:
    genai.configure(api_key=api_key)
    model_name = Config.GEMINI_MODEL
    model = genai.GenerativeModel(model_name)
    logger.info(f"Gemini API configured with model: {model_name}")

    # Test API connection
    try:
        test_response = model.generate_content("Test connection")
        st.sidebar.success("✅ Gemini API connected successfully")
    except Exception as e:
        st.sidebar.error(f"❌ Gemini API test failed: {e}")
        logger.error(f"Gemini API test failed: {e}")
        model = None

except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    st.sidebar.error(f"Failed to configure Gemini API: {e}")
    st.sidebar.warning("Chat functionality will be disabled. Please check your API key.")

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
            validate_name(name)
            validate_email(email)
            validate_skills(skills)

            sanitized_name = sanitize_input(name)
            sanitized_email = sanitize_input(email)
            sanitized_skills = sanitize_input(skills)

            add_volunteer(sanitized_name, sanitized_email, sanitized_skills)
            st.sidebar.success("✅ Volunteer Registered Successfully!")
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
        volunteers = get_all_volunteers()
        df = pd.DataFrame(volunteers)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Volunteers", len(df))

        with col2:
            skill_count = df["skills"].nunique() if len(df) > 0 else 0
            st.metric("Unique Skills", skill_count)

        with col3:
            memory_count = memory_manager.get_memory_count()
            st.metric("Memory Entries", memory_count)

        st.subheader("Volunteer Records")

        if len(df) > 0:
            st.dataframe(df.copy(), use_container_width=True)

            st.subheader("Volunteer Management")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Update Volunteer**")
                available_ids = df['id'].tolist() if 'id' in df.columns else list(range(1, len(df) + 1))
                if available_ids:
                    volunteer_id = st.selectbox("Select Volunteer to Update", available_ids)
                    volunteer = get_volunteer_by_id(volunteer_id)

                    if volunteer:
                        update_name = st.text_input("Name", value=volunteer['name'])
                        update_email = st.text_input("Email", value=volunteer['email'])
                        update_skills = st.text_area("Skills", value=volunteer['skills'])

                        if st.button("Update Volunteer", use_container_width=True):
                            try:
                                update_volunteer(volunteer_id, update_name, update_email, update_skills)
                                st.success("✅ Volunteer updated successfully")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Update failed: {e}")
                    else:
                        st.warning("Volunteer not found")
                else:
                    st.info("No volunteers available to update")

            with col2:
                st.write("**Delete Volunteer**")
                if available_ids:
                    delete_id = st.selectbox("Select Volunteer to Delete", available_ids)
                    delete_vol = get_volunteer_by_id(delete_id)

                    if delete_vol:
                        st.write(f"Deleting: {delete_vol['name']} ({delete_vol['email']})")
                        if st.button("Delete Volunteer", type="primary", use_container_width=True):
                            try:
                                delete_volunteer(delete_id)
                                st.success("✅ Volunteer deleted successfully")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Delete failed: {e}")
                    else:
                        st.warning("Volunteer not found")
                else:
                    st.info("No volunteers available to delete")

            st.subheader("Skills Distribution")
            st.bar_chart(df["skills"].value_counts())

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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==================================
# CHAT INPUT
# ==================================

query = st.chat_input("Ask NayePankh AI Assistant...")

if query:
    try:
        if model is None:
            st.error("Chat functionality is not available. Please configure a valid Gemini API key.")
            st.stop()

        validate_query(query)
        sanitized_query = sanitize_input(query)

        st.session_state.messages.append({
            "role": "user",
            "content": sanitized_query
        })

        try:
            memory_manager.add_memory(sanitized_query)
        except Exception as e:
            logger.warning(f"Memory addition failed: {e}")

        try:
            memories = memory_manager.query_memory(sanitized_query, n_results=3)
        except Exception as e:
            logger.warning(f"Memory query failed: {e}")
            memories = []

        agent = route_query(sanitized_query)

        with st.chat_message("user"):
            st.write(sanitized_query)

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
                    response = model.generate_content(prompt)
                    answer = response.text
                    st.write(answer)

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