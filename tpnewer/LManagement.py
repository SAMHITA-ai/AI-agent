import json
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Absolute path to the data file
DATA_FILE = "C:/Users/KIIT/OneDrive/Desktop/3rd_Year/AI/22053714_html/tpnewer/Ldata.json"  # Corrected file path

def load_data():
    """Load student attendance and leave data from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"employees": {}}

def save_data(data):
    """Save updated student leave data."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_leave_eligibility(student_id, requested_days):
    """Check if student is eligible for leave based on attendance and balance."""
    data = load_data()
    student = data["employees"].get(str(student_id))  # Ensure student_id is a string for lookup

    if not student:
        return f"❌ Student ID {student_id} not found in records."

    if student["attendance"] < 75:
        return f"❌ Leave request denied: Attendance too low ({student['attendance']}%). Minimum required: 75%."

    if student["leave_balance"] < requested_days:
        return f"❌ Leave request denied: Insufficient leave balance ({student['leave_balance']} days left)."

    # Deduct leave balance if approved
    student["leave_balance"] -= requested_days
    save_data(data)
    
    return f"✅ Leave approved for {requested_days} days. Remaining balance: {student['leave_balance']} days."

# Ensure the chatbot can import this function
def handle_leave_request(student_id, requested_days):
    return check_leave_eligibility(student_id, requested_days)

# Restore interactive functionality
if __name__ == "__main__":
    student_id = input("Enter Student Roll Number: ")
    requested_days = int(input("Enter Number of Leave Days: "))
    result = check_leave_eligibility(student_id, requested_days)
    print(result)
