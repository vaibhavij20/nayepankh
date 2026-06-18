# API Keys Setup Guide

## Where to Configure API Keys

There are three ways to configure API keys for the NayePankh AI Assistant:

### 1. Local Development (.env file)

Create or edit the `.env` file in the project root:

```bash
# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Resend API Key (for email notifications)
RESEND_API_KEY=your_resend_api_key_here

# Email Configuration
EMAIL_FROM=onboarding@resend.dev
```

**How to get API keys:**
- **Gemini API Key:** Go to https://makersuite.google.com/app/apikey
- **Resend API Key:** Go to https://resend.com/api-keys

### 2. Streamlit Cloud Deployment

When deploying to Streamlit Cloud, configure secrets in the app settings:

1. Go to your Streamlit Cloud app
2. Click "Settings" → "Secrets"
3. Add the following secrets:

```toml
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password"
GEMINI_API_KEY = "your_gemini_api_key_here"
RESEND_API_KEY = "your_resend_api_key_here"
EMAIL_FROM = "onboarding@resend.dev"
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

### Resend API Key (Optional - for Email)
- **Purpose:** Sends welcome emails to volunteers
- **Get it from:** https://resend.com/api-keys
- **Required for:** Email notifications
- **Note:** If not configured, the app will still work but email notifications will be disabled

## Email Domain Configuration

The email sender address must be a verified domain on Resend:

**For Testing:** Use `onboarding@resend.dev` (Resend-provided domain)
**For Production:** Verify your own domain at https://resend.com/domains

## Troubleshooting

### Chat not working?
- Ensure GEMINI_API_KEY is set
- Check the API key is valid
- Verify the key has proper permissions

### Email not sending?
- Ensure RESEND_API_KEY is set
- Check the email domain is verified on Resend
- Verify the recipient email address is valid
- Check the logs for specific error messages

### Admin login failing?
- Check ADMIN_USERNAME and ADMIN_PASSWORD are set correctly
- Default credentials: admin / changeme (change these in production!)
