import json
import os
from Aqueries import get_academic_answer, load_faqs
from LManagement import handle_leave_request
from email_handler import send_email, get_certificate_path

# Load FAQs for academic queries
faqs = load_faqs()

FEEDBACK_FILE = "feedback.json"
FAQ_FILE = "academics_faqs.json"
REJECTED_FEEDBACK_FILE = "rejected_feedback.json"


def load_data(filename):
    """Loads JSON data from a file."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_data(filename, data):
    """Saves JSON data to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def collect_feedback(user_input, response):
    """Stores feedback and counts occurrences before applying changes."""
    feedback_data = load_data(FEEDBACK_FILE)
    correct_response = input("What should have been the correct response? ").strip()

    if user_input in feedback_data:
        feedback_data[user_input]["count"] += 1
    else:
        feedback_data[user_input] = {
            "received_response": response,
            "suggested_response": correct_response,
            "count": 1
        }

    save_data(FEEDBACK_FILE, feedback_data)
    print("✅ Thank you! Your feedback has been recorded.")


def send_document_request():
    """Handles certificate/NOC/document requests by fetching the appropriate file and sending it via email."""
    roll_number = input("Enter your roll number: ").strip()
    email = input("Enter your email: ").strip()
    doc_type = input("Enter document type (bonafide/noc/certificate): ").strip().lower()

    certificate_path = get_certificate_path(roll_number, doc_type)

    if certificate_path:
        send_email(email, f"Your {doc_type} document", "Please find your requested document attached.", certificate_path)
        print(f"📤 Document sent to {email} successfully!")
        return "Document sent successfully!"
    else:
        print("⚠️ Document not found! Please contact the administration.")
        return "Document not found! Please contact the administration."


def detect_intent(user_input):
    user_input = user_input.lower()
    
    keyword_map = {
        "leave_policy": ["how many leaves", "leave policy", "leave limit"],
        "leave_request": ["leave request", "absent", "vacation", "days off"],
        "academic_query": ["academic", "syllabus", "course", "exam", "grading", "attendance", "evaluation", "registration", "schedule", "transcript"],
        "exam_query": ["exam timing", "exam schedule", "exam date", "exam retake"],
        "holiday_query": ["holiday", "vacation dates", "semester break"],
        "certificate_request": ["certificate", "noc", "document", "bonafide"],
        "placement_query": ["placement", "internship", "job", "companies", "resume", "eligibility"],
        "hostel_query": ["hostel", "accommodation", "curfew", "guest policy", "cook"],
        "library_query": ["library", "borrow books", "digital library", "study room", "opening hours"],
        "sports_query": ["sports", "gym", "athletics", "competitions", "scholarship"],
        "scholarship_query": ["scholarship", "financial aid", "fee waiver", "merit-based aid"],
        "student_life_query": ["clubs", "fest", "events", "counseling", "grievance", "disciplinary"],
        "tech_support_query": ["wi-fi", "it support", "email login"]
    }
    
    for intent, keywords in keyword_map.items():
        if any(word in user_input for word in keywords):
            return intent
    
    return "unknown"


def chatbot_response(user_input):
    intent = detect_intent(user_input)
    
    responses = {
        "leave_policy": "Students can take a maximum of 10 leave days per semester. Additional leaves require special approval.",
        "leave_request": lambda: handle_leave_request(input("Enter Student Roll Number: "), int(input("Enter Number of Leave Days: "))),
        "academic_query": lambda: get_academic_answer(user_input, faqs),
        "exam_query": "Exam schedules are released one month before exams. Check the student portal for details.",
        "holiday_query": "Holidays are listed in the academic calendar. The semester break usually occurs in December and June.",
        "certificate_request": send_document_request,
        "placement_query": "Placement-related queries should be directed to the placement cell. Check the placement portal for company listings and application deadlines.",
        "hostel_query": "Hostel applications, curfews, and guest policies are managed by the hostel office. Visit the student portal for more details.",
        "library_query": "Library hours are 8 AM to 10 PM. You can borrow up to 4 books at a time for 15 days.",
        "sports_query": "The university offers various sports facilities, including football, basketball, and a gym. Tryouts for teams are held at the start of each semester.",
        "scholarship_query": "The university offers scholarships based on merit, sports achievements, and financial need. Visit the scholarship portal for eligibility and application details.",
        "student_life_query": "The university has several student clubs, events, and cultural fests. Visit the student activity portal for details.",
        "tech_support_query": "For Wi-Fi access, IT support, and email issues, visit the IT help desk in the library building."
    }
    
    response = responses.get(intent, "I'm not sure how to help with that. Try asking about academic queries, leave requests, certificates, or other student services.")
    
    if callable(response):
        response = response()
    
    if intent == "unknown":
        print("⚠️ The bot may have misclassified your query.")
        collect_feedback(user_input, response)
    
    return response

if __name__ == "__main__":
    print("Hello! I'm your university assistant. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Chat-bot: {response}")
