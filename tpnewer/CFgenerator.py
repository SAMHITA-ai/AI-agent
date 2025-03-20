import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

CERTIFICATE_TEMPLATES = {
    "bonafide": "This is to certify that {name}, Roll No. {roll_no}, is a bonafide student of {university}.",
    "noc": "This is to certify that {name}, Roll No. {roll_no}, has no objection from {university} for the purpose mentioned.",
    "custom": "{custom_text}"
}

CERTIFICATE_FOLDER = "certificates"

# Ensure the certificates folder exists
os.makedirs(CERTIFICATE_FOLDER, exist_ok=True)

def generate_certificate(cert_type, name, roll_no, university, custom_text=""):
    """Generates a certificate PDF."""
    if cert_type not in CERTIFICATE_TEMPLATES:
        print("⚠️ Invalid certificate type!")
        return

    text = CERTIFICATE_TEMPLATES[cert_type].format(
        name=name,
        roll_no=roll_no,
        university=university,
        custom_text=custom_text
    )

    filename = f"{CERTIFICATE_FOLDER}/{cert_type}_{roll_no}.pdf"
    pdf = canvas.Canvas(filename, pagesize=A4)

    # Formatting the PDF
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(300, 770, f"{cert_type.upper()} CERTIFICATE")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Date: {datetime.today().strftime('%d-%m-%Y')}")
    pdf.drawString(100, 690, f"To Whom It May Concern,")

    pdf.setFont("Helvetica", 14)
    text_lines = text.split("\n")
    y_position = 660
    for line in text_lines:
        pdf.drawString(100, y_position, line)
        y_position -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position - 40, "Signature:")
    pdf.drawString(100, y_position - 60, "(Authorized Signatory)")

    pdf.save()
    print(f"✅ Certificate generated: {filename}")

def main():
    """Main function to generate certificates."""
    while True:
        print("\n📜 Certificate Generator")
        print("1️⃣ Generate Bonafide Certificate")
        print("2️⃣ Generate NOC")
        print("3️⃣ Generate Custom Certificate")
        print("4️⃣ Exit")
        choice = input("Choose an option: ").strip()

        if choice in ["1", "2", "3"]:
            name = input("Enter Student Name: ").strip()
            roll_no = input("Enter Roll Number: ").strip()
            university = input("Enter University Name: ").strip()
            custom_text = ""

            if choice == "3":
                custom_text = input("Enter Custom Certificate Text: ").strip()

            cert_type = "bonafide" if choice == "1" else "noc" if choice == "2" else "custom"
            generate_certificate(cert_type, name, roll_no, university, custom_text)

        elif choice == "4":
            print("👋 Exiting Certificate Generator.")
            break
        else:
            print("⚠️ Invalid choice! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
