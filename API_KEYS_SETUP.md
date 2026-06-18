# API Keys Setup Guide

## Where to Configure API Keys

There are two ways to configure API keys for the NayePankh AI Assistant:

### 1. Local Development (.env file)

Create or edit the `.env` file in the project root:

```bash
# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

**How to get API keys:**
- **Gemini API Key:** Go to https://makersuite.google.com/app/apikey

### 2. Streamlit Cloud Deployment

When deploying to Streamlit Cloud, configure secrets in the app settings:

1. Go to your Streamlit Cloud app
2. Click "Settings" → "Secrets"
3. Add the following secrets:

```toml
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password"
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 3. Sidebar Input (Runtime)

You can also enter the Gemini API key directly in the app sidebar:

1. Open the application
2. Look for "⚙️ Settings" in the sidebar
3. Enter your Gemini API Key in the password field
4. The app will use this key for the session

## Required API Keys

### Gemini API Key (Required for Chat)
- **Purpose:** Powers the AI chat functionality
- **Get it from:** https://makersuite.google.com/app/apikey
- **Required for:** Chat responses, AI-powered assistance

## Troubleshooting

### Chat not working?
- Ensure GEMINI_API_KEY is set
- Check the API key is valid
- Verify the key has proper permissions

### Admin login failing?
- Check ADMIN_USERNAME and ADMIN_PASSWORD are set correctly
- Default credentials: admin / changeme (change these in production!)
