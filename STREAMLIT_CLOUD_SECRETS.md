# Streamlit Cloud Secrets Configuration

For deploying to Streamlit Cloud, you need to configure the following secrets in the Streamlit Cloud dashboard.

## Required Secrets

Add these secrets in your Streamlit Cloud app settings (Settings → Secrets):

```toml
# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password_here"

# Gemini AI API
GEMINI_API_KEY = "your_gemini_api_key_here"

# Email Service (Resend)
RESEND_API_KEY = "your_resend_api_key_here"
EMAIL_FROM = "onboarding@resend.dev"

# Gemini Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_TEMPERATURE = "0.7"
GEMINI_MAX_TOKENS = "1024"
GEMINI_TIMEOUT = "60"

# Memory Configuration
MEMORY_RETENTION_DAYS = "30"
MEMORY_MAX_RESULTS = "3"

# Session Configuration
SESSION_TIMEOUT_MINUTES = "30"

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = "60"
```

## How to Get API Keys

### Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste into GEMINI_API_KEY

### Resend API Key
1. Go to https://resend.com/api-keys
2. Create a new API key
3. Copy and paste into RESEND_API_KEY

## Deployment Steps

1. **Connect GitHub Repository**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your repository: vaibhavij20/nayepankh
   - Select branch: main
   - Main file path: app.py

2. **Configure Secrets**
   - Go to your app settings in Streamlit Cloud
   - Click "Secrets"
   - Add all the secrets listed above
   - Click "Save"

3. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at: https://your-app-name.streamlit.app

## Important Notes

- **Never commit actual secrets to git** - use Streamlit Cloud secrets
- **Change the default admin password** before deploying
- **Keep API keys secure** - don't share them
- **Changes to secrets take about 1 minute to propagate**
- **Python 3.14 is supported** - no changes needed

## Troubleshooting

If you see errors:
1. Check that all required secrets are configured
2. Verify API keys are valid
3. Check deployment logs in Streamlit Cloud
4. Ensure secrets are properly formatted (TOML format)
