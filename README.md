# NayePankh AI Assistant 🤖

An AI-powered NGO Volunteer Management System built with Streamlit, Google Gemini AI, and ChromaDB.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Testing](#testing)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **AI-Powered Chat Assistant**: Intelligent conversational interface powered by Google Gemini AI
- **Volunteer Registration**: Easy volunteer sign-up with validation and email notifications
- **Mentor Matching**: Fuzzy matching algorithm to connect volunteers with mentors
- **Multi-Agent Routing**: Intelligent query routing to specialized agents (Mentor, Event, Volunteer, NGO, FAQ)
- **Memory System**: ChromaDB-based memory for context-aware conversations
- **Admin Dashboard**: Comprehensive admin panel with metrics, charts, and data export
- **Weekly Reports**: Automated report generation with volunteer statistics
- **Email Notifications**: Welcome emails and admin alerts via Resend

### Technical Features
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: Robust error handling with logging throughout
- **Security**: Environment variable management, input sanitization, SQL injection prevention
- **Performance**: Database indexing, connection pooling, memory cleanup
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Logging**: Centralized logging system for monitoring and debugging

## 🛠 Tech Stack

### Frontend
- **Streamlit 1.58.0**: Web application framework
- **Python 3.11**: Programming language

### AI/ML
- **Google Generative AI 0.8.6**: LLM integration
- **ChromaDB 1.5.9**: Vector database for memory

### Database
- **SQLite**: Lightweight database for volunteer data
- **Pandas 3.0.3**: Data manipulation and analysis

### Email
- **Resend 0.8.0**: Email service API

### Utilities
- **python-dotenv 1.2.2**: Environment variable management
- **python-dateutil 2.9.0**: Date/time utilities

## 📁 Project Structure

```
nayepankhagent/
├── agents/                    # Agent modules
│   ├── __init__.py
│   ├── router_agent.py       # Query routing with intent classification
│   ├── volunteer_agent.py    # Volunteer registration
│   ├── mentor_agent.py       # Mentor matching with fuzzy search
│   ├── faq_agent.py          # FAQ handling
│   └── report_agent.py       # Report generation
├── database/                  # Database operations
│   ├── __init__.py
│   └── db.py                 # SQLite operations with error handling
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── email_service.py      # Email notifications
│   └── validators.py         # Input validation and sanitization
├── memory/                    # ChromaDB storage (auto-created)
├── logs/                      # Application logs (auto-created)
├── data/                      # Data files (auto-created)
├── .streamlit/               # Streamlit configuration
│   └── secrets.toml          # Streamlit secrets (use env vars)
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration management
├── logger.py                 # Logging configuration
├── memory_manager.py         # ChromaDB memory management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Google Gemini API key
- Resend API key (for email notifications)

### Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd nayepankhagent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# Gemini AI API
GEMINI_API_KEY=your_gemini_api_key_here

# Email Service (Resend)
RESEND_API_KEY=your_resend_api_key_here
EMAIL_FROM=NayePankh <onboarding@yourdomain.com>

# Gemini Configuration
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1024

# Memory Configuration
MEMORY_RETENTION_DAYS=30
MEMORY_MAX_RESULTS=3

# Session Configuration
SESSION_TIMEOUT_MINUTES=30

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
```

### Getting API Keys

**Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

**Resend API Key:**
1. Visit [Resend](https://resend.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

## 📖 Usage

### For Volunteers

1. **Register**: Use the sidebar form to register as a volunteer
2. **Chat**: Ask questions about volunteering, events, or NGO activities
3. **Find Mentors**: Use the mentor matching feature to find mentors with specific skills

### For Administrators

1. **Login**: Navigate to "Admin Dashboard" and log in with admin credentials
2. **View Metrics**: See total volunteers, unique skills, and memory entries
3. **Export Data**: Download volunteer data as CSV
4. **Generate Reports**: Download weekly reports
5. **Monitor**: Check logs in the `logs/` directory

## 🐳 Deployment

### Docker Deployment

1. **Build the Docker image**
```bash
docker build -t nayepankh-assistant .
```

2. **Run with Docker**
```bash
docker run -p 8501:8501 --env-file .env nayepankh-assistant
```

### Docker Compose Deployment

1. **Start the application**
```bash
docker-compose up -d
```

2. **View logs**
```bash
docker-compose logs -f
```

3. **Stop the application**
```bash
docker-compose down
```

### Production Deployment Considerations

- **Environment Variables**: Never commit `.env` file to version control
- **Database**: Use volume mounts to persist SQLite database
- **Memory**: Use volume mounts to persist ChromaDB memory
- **Logs**: Use volume mounts to persist application logs
- **Security**: Use strong admin passwords and rotate API keys regularly
- **Monitoring**: Set up log aggregation and monitoring
- **Backup**: Regularly backup the SQLite database

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_database.py

# Run with coverage
pytest --cov=. tests/
```

### Test Structure

```
tests/
├── __init__.py
├── test_database.py       # Database operation tests
├── test_agents.py         # Agent functionality tests
├── test_memory.py         # Memory system tests
├── test_validators.py     # Validation tests
└── test_email.py          # Email service tests
```

## 🔒 Security

### Security Features Implemented

- **Input Validation**: All user inputs are validated before processing
- **Input Sanitization**: SQL injection and XSS prevention
- **Environment Variables**: Sensitive data stored in environment variables
- **SQL Injection Prevention**: Parameterized queries for all database operations
- **Error Handling**: Graceful error handling without exposing sensitive information
- **Logging**: Comprehensive logging for security monitoring
- **Session Management**: Admin session state management

### Security Best Practices

1. **Never commit secrets**: Use `.env` file and `.gitignore`
2. **Use strong passwords**: Minimum 8 characters for admin credentials
3. **Rotate API keys**: Regularly update API keys
4. **Monitor logs**: Regularly review logs for suspicious activity
5. **Keep dependencies updated**: Regularly update Python packages
6. **Use HTTPS**: Deploy behind a reverse proxy with SSL/TLS

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License.


## 🙏 Acknowledgments

- Google Generative AI for the powerful LLM
- Streamlit for the amazing web framework
- ChromaDB for the vector database
- Resend for the email service

---

**Built with ❤️ for NayePankh Foundation**
