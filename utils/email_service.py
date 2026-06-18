"""
Email service module for NayePankh AI Assistant.
Handles email notifications with error handling and retry logic.
"""

import time
from typing import Optional, Dict, Any
from config import Config
from logger import get_logger

logger = get_logger(__name__)

# Try to import resend, handle if not available
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend package not available - email features will be disabled")


class EmailService:
    """Handles email operations with error handling and retry logic."""
    
    def __init__(self):
        """Initialize the email service."""
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self._configure_api_key()
    
    def _configure_api_key(self) -> None:
        """Configure the Resend API key."""
        if RESEND_AVAILABLE and Config.RESEND_API_KEY:
            resend.api_key = Config.RESEND_API_KEY
            logger.info("Email service configured with API key")
        else:
            logger.warning("Email service not configured - API key missing or resend not installed")
    
    def send_welcome_email(self, name: str, email: str) -> bool:
        """
        Send a welcome email to a new volunteer.
        
        Args:
            name: Volunteer name
            email: Volunteer email address
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not RESEND_AVAILABLE or not Config.RESEND_API_KEY:
            logger.warning("Email service not available - skipping welcome email")
            return False
        
        subject = "Welcome to NayePankh Foundation"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to NayePankh Foundation! 🎉</h1>
                </div>
                <div class="content">
                    <h2>Hello {name},</h2>
                    <p>Thank you for joining NayePankh Foundation as a volunteer.</p>
                    <p>Your registration has been successfully completed. We're excited to have you on board!</p>
                    <p><strong>What's Next?</strong></p>
                    <ul>
                        <li>You'll receive updates about upcoming events</li>
                        <li>We'll match you with mentorship opportunities</li>
                        <li>You can participate in our various programs</li>
                    </ul>
                    <p>If you have any questions, feel free to reach out to us.</p>
                    <p>Best regards,<br>The NayePankh Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 NayePankh Foundation. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    
    def send_admin_alert(self, subject: str, message: str) -> bool:
        """
        Send an alert email to administrators.
        
        Args:
            subject: Alert subject
            message: Alert message
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not RESEND_AVAILABLE or not Config.RESEND_API_KEY:
            logger.warning("Email service not available - skipping admin alert")
            return False
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .alert {{ background-color: #ff4444; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="alert">
                    <h1>⚠️ Admin Alert</h1>
                </div>
                <div class="content">
                    <h2>{subject}</h2>
                    <p>{message}</p>
                    <p><em>This is an automated alert from NayePankh AI Assistant.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email="admin@nayepankh.org",  # Configure this as needed
            subject=f"[ALERT] {subject}",
            html_content=html_content
        )
    
    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """
        Send an email with retry logic.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not RESEND_AVAILABLE:
            logger.error("Resend package not available")
            return False
        
        if not Config.RESEND_API_KEY:
            logger.error("Resend API key not configured")
            return False
        
        for attempt in range(self.max_retries):
            try:
                params = {
                    "from": Config.EMAIL_FROM,
                    "to": [to_email],
                    "subject": subject,
                    "html": html_content
                }
                
                logger.info(f"Sending email to {to_email} (attempt {attempt + 1}/{self.max_retries})")
                
                result = resend.Emails.send(params)
                
                if result:
                    logger.info(f"Email sent successfully to {to_email}")
                    return True
                else:
                    logger.warning(f"Email send returned empty result for {to_email}")
                    
            except Exception as e:
                logger.error(f"Email send attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to send email to {to_email} after {self.max_retries} attempts")
                    return False
        
        return False


# Global email service instance
email_service = EmailService()

# Backward compatibility functions
def send_welcome_email(name: str, email: str) -> bool:
    """
    Send a welcome email to a new volunteer.
    
    Args:
        name: Volunteer name
        email: Volunteer email address
    
    Returns:
        True if email sent successfully, False otherwise
    """
    return email_service.send_welcome_email(name, email)


def send_admin_alert(subject: str, message: str) -> bool:
    """
    Send an alert email to administrators.
    
    Args:
        subject: Alert subject
        message: Alert message
    
    Returns:
        True if email sent successfully, False otherwise
    """
    return email_service.send_admin_alert(subject, message)