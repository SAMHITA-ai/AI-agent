import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 📩 Email Credentials
EMAIL_USER = "samhita2411@gmail.com"
EMAIL_PASS = "shkv kyfi bkjd quqf"
SMTP_SERVER = "smtp.gmail.com"

# 📂 Folder Where Certificates are Stored (Updated path)
CERTIFICATE_FOLDER = r"C:\Users\KIIT\OneDrive\Desktop\3rd_Year\AI\22053714_html\tpnewer\certificates"

# 🔍 Function to Fetch Certificate File
def get_certificate_path(roll_number, doc_type):
    """Find the requested document (bonafide, noc, certificate) based on roll number."""
    file_name = f"{doc_type.lower()}_{roll_number}.pdf"
    file_path = os.path.join(CERTIFICATE_FOLDER, file_name)

    if os.path.exists(file_path):
        return file_path
    return None  # No matching document found

# ✉️ Function to Send an Email with Certificate Attachment
def send_email(to_email, subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
        msg.attach(part)

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"📤 Document sent to {to_email} successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Example Usage:
if __name__ == "__main__":
    roll_number = input("Enter Roll Number: ")
    doc_type = input("Enter Document Type (e.g., bonafide, noc, certificate): ")
    recipient_email = input("Enter Recipient Email: ")

    # Get the certificate file path
    certificate_path = get_certificate_path(roll_number, doc_type)

    if certificate_path:
        # Compose email details
        subject = f"Requested {doc_type.capitalize()} for Roll Number {roll_number}"
        body = f"Dear Student,\n\nPlease find attached your requested {doc_type} for roll number {roll_number}.\n\nBest regards,\nUniversity Team"

        # Send email
        send_email(recipient_email, subject, body, certificate_path)
    else:
        print(f"❌ Error: No document found for Roll Number {roll_number} and Type {doc_type}.")
