"""
AI Career Companion - Automated Email Dispatch Service
Sends 2FA Security Verification codes and notification emails to students and administrators.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SENDER_NAME = os.environ.get('SENDER_NAME', 'AI Career Companion Security')


def send_2fa_email(recipient_email: str, recipient_name: str, otp_code: str, portal_type: str = "Student Profile") -> tuple:
    """
    Sends a formatted 2FA verification email to the specified recipient.
    Returns (success: bool, status_message: str)
    """
    if not recipient_email or "@" not in recipient_email:
        return False, "Invalid recipient email address."

    subject = f"🔒 Your 2FA Verification Code: {otp_code} - AI Career Companion"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6fb; margin: 0; padding: 20px; color: #1e293b; }}
            .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }}
            .header {{ background: linear-gradient(135deg, #6366F1, #4F46E5); padding: 30px 20px; text-align: center; color: #ffffff; }}
            .header h1 {{ margin: 0; font-size: 22px; font-weight: 800; }}
            .header p {{ margin: 6px 0 0 0; font-size: 13px; opacity: 0.9; }}
            .body {{ padding: 30px 25px; }}
            .greeting {{ font-size: 16px; font-weight: 600; margin-bottom: 12px; }}
            .otp-box {{ background: #f0fdf4; border: 2px dashed #22c55e; border-radius: 10px; padding: 18px; text-align: center; margin: 24px 0; }}
            .otp-code {{ font-family: 'Courier New', monospace; font-size: 32px; font-weight: 800; letter-spacing: 8px; color: #15803d; }}
            .timer {{ font-size: 13px; color: #64748b; margin-top: 8px; }}
            .security-note {{ font-size: 12.5px; color: #64748b; line-height: 1.5; background: #f8fafc; border-left: 4px solid #6366F1; padding: 10px 14px; border-radius: 0 6px 6px 0; margin-top: 20px; }}
            .footer {{ background: #f8fafc; padding: 18px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 AI Career Companion</h1>
                <p>Two-Factor Authentication (2FA) Verification</p>
            </div>
            <div class="body">
                <div class="greeting">Hello {recipient_name},</div>
                <p style="font-size: 14px; line-height: 1.5; color: #475569;">
                    A request was received to log into your <strong>{portal_type}</strong>. Use the 6-digit verification code below to complete your authentication:
                </p>
                <div class="otp-box">
                    <div class="otp-code">{otp_code}</div>
                    <div class="timer">⏱️ Valid for 5 minutes</div>
                </div>
                <div class="security-note">
                    <strong>Security Notice:</strong> If you did not initiate this login request, please disregard this email or notify your campus placement administrator immediately.
                </div>
            </div>
            <div class="footer">
                Developed by <strong>Riya Modi & Diksha Durgapal</strong> for Placement Guidance & Analytics.<br>
                This is an automated system notification.
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = f"""
    AI Career Companion - 2FA Security Code
    
    Hello {recipient_name},
    
    Your 6-digit 2FA verification code to log into your {portal_type} is:
    
    {otp_code}
    
    (Valid for 5 minutes)
    
    If you did not request this login, please contact your administrator.
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SMTP_EMAIL if SMTP_EMAIL else 'security@careercompanion.edu'}>"
    msg["To"] = recipient_email

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    # Attempt live SMTP dispatch if credentials configured
    if SMTP_EMAIL and SMTP_PASSWORD:
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.sendmail(SMTP_EMAIL, [recipient_email], msg.as_string())
            print(f"[MAIL SERVICE] Successfully dispatched 2FA email to {recipient_email}")
            return True, f"2FA code sent to {recipient_email}"
        except Exception as e:
            print(f"[MAIL SERVICE SMTP ERROR] Failed to send via SMTP: {e}")
            print(f"[MAIL SERVICE LOCAL DISPATCH] 2FA Code for {recipient_email} ({recipient_name}): {otp_code}")
            return False, f"SMTP connection error: {e}"
    else:
        print(f"[MAIL SERVICE LOCAL DISPATCH] 2FA Code sent to {recipient_email} ({recipient_name}): {otp_code}")
        return True, f"2FA code generated for {recipient_email}"


def send_welcome_student_email(recipient_email: str, recipient_name: str, enrollment_no: str, password: str, department: str) -> tuple:
    """
    Sends account creation welcome email with login instructions to the student's email.
    """
    if not recipient_email or "@" not in recipient_email:
        return False, "Invalid recipient email"

    subject = f"🎓 Welcome to AI Career Companion - Your Student Login Credentials"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6fb; margin: 0; padding: 20px; color: #1e293b; }}
            .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }}
            .header {{ background: linear-gradient(135deg, #10B981, #059669); padding: 30px 20px; text-align: center; color: #ffffff; }}
            .header h1 {{ margin: 0; font-size: 22px; font-weight: 800; }}
            .header p {{ margin: 6px 0 0 0; font-size: 13px; opacity: 0.9; }}
            .body {{ padding: 30px 25px; }}
            .cred-card {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; margin: 20px 0; }}
            .cred-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }}
            .cred-lbl {{ color: #64748b; font-weight: 600; }}
            .cred-val {{ font-weight: 700; color: #0f172a; font-family: 'Courier New', monospace; }}
            .footer {{ background: #f8fafc; padding: 18px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 AI Career Companion</h1>
                <p>Official Student Portal Account Registration</p>
            </div>
            <div class="body">
                <p>Hello <strong>{recipient_name}</strong>,</p>
                <p>Your student login account has been created by the placement administration. You can now log into your student dashboard to track your resume ATS score, practice placement questions, and monitor your placement journey.</p>
                
                <div class="cred-card">
                    <div class="cred-row"><span class="cred-lbl">Enrollment No:</span> <span class="cred-val">{enrollment_no}</span></div>
                    <div class="cred-row"><span class="cred-lbl">Department:</span> <span class="cred-val">{department}</span></div>
                    <div class="cred-row"><span class="cred-lbl">Temporary Password:</span> <span class="cred-val">{password}</span></div>
                    <div class="cred-row"><span class="cred-lbl">2FA Protection:</span> <span class="cred-val">Enabled (Email OTP)</span></div>
                </div>

                <p style="font-size: 13px; color: #64748b;">
                    When logging in, a 6-digit Two-Factor Authentication (2FA) verification code will be sent to this email address ({recipient_email}).
                </p>
            </div>
            <div class="footer">
                Developed by <strong>Riya Modi & Diksha Durgapal</strong> for Placement Guidance & Analytics.
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = f"Welcome {recipient_name}! Your student account is created. Enrollment: {enrollment_no}, Password: {password}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SMTP_EMAIL if SMTP_EMAIL else 'security@careercompanion.edu'}>"
    msg["To"] = recipient_email

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    if SMTP_EMAIL and SMTP_PASSWORD:
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.sendmail(SMTP_EMAIL, [recipient_email], msg.as_string())
            print(f"[MAIL SERVICE] Dispatched welcome credentials to {recipient_email}")
            return True, f"Welcome email sent to {recipient_email}"
        except Exception as e:
            print(f"[MAIL SERVICE SMTP ERROR] {e}")
            return False, str(e)
    else:
        print(f"[MAIL SERVICE LOCAL DISPATCH] Welcome email dispatched to {recipient_email} for {recipient_name}")
        return True, f"Welcome email generated for {recipient_email}"
