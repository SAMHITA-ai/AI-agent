import json
import os

FEEDBACK_FILE = "feedback.json"
FAQ_FILE = "academics_faqs.json"

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

def collect_feedback():
    """Collects user feedback on bot responses."""
    faq_data = load_data(FAQ_FILE).get("faqs", {})
    feedback_data = load_data(FEEDBACK_FILE)

    print("\n💬 Enter your feedback on bot responses:")
    question = input("What was your query? ").strip()
    response = input("What response did you receive? ").strip()
    suggestion = input("What should have been the correct response? ").strip()

    feedback_data[question] = {
        "received_response": response,
        "suggested_response": suggestion
    }

    save_data(FEEDBACK_FILE, feedback_data)
    print("✅ Thank you! Your feedback has been recorded.\n")

def update_faqs():
    """Allows admins to update FAQ responses based on feedback."""
    feedback_data = load_data(FEEDBACK_FILE)
    faq_data = load_data(FAQ_FILE)

    if not feedback_data:
        print("⚠️ No feedback found for improvements.")
        return

    print("\n🔄 Updating FAQs based on feedback...\n")
    for question, details in feedback_data.items():
        suggested_response = details["suggested_response"]
        if question in faq_data:
            print(f"🔹 Updating: {question}")
            faq_data[question] = suggested_response
        else:
            print(f"➕ Adding new entry: {question}")
            faq_data[question] = suggested_response

    save_data(FAQ_FILE, {"faqs": faq_data})
    os.remove(FEEDBACK_FILE)  # Clear feedback after updating
    print("✅ FAQ updates completed!\n")

def main():
    """Main function to collect feedback or update FAQs."""
    while True:
        print("\n📌 Feedback Improvement System")
        print("1️⃣ Submit Feedback")
        print("2️⃣ Update FAQs (Admin)")
        print("3️⃣ Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            collect_feedback()
        elif choice == "2":
            update_faqs()
        elif choice == "3":
            print("👋 Exiting feedback system.")
            break
        else:
            print("⚠️ Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
