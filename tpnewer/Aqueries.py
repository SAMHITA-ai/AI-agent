import json
import os
from rapidfuzz import process, fuzz

# Load FAQs from JSON file
def load_faqs(file_path="C:/Users/KIIT/OneDrive/Desktop/3rd_Year/AI/22053714_html/tpnewer/Afaqs.json"):
    """Load the FAQ data from a JSON file."""
    try:
        # Check if file exists at the given path
        if not os.path.exists(file_path):
            print(f"❌ Error: The file {file_path} does not exist.")
            return {}

        print(f"📂 Loading FAQ file from: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Print the loaded data for debugging
        print(f"📄 FAQ data loaded: {data}")

        # Ensure that "faqs" is present in the loaded JSON data
        return data.get("faqs", {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error: Could not load FAQ file. {str(e)}")
        return {}

# Refined Matching Logic
def refine_matching_logic(query, faqs):
    """Refine the logic for better classification of queries."""
    # A list of common words/phrases and their synonyms
    synonyms = {
        "holidays": ["holiday", "vacation", "break", "leave"],
        "academic calendar": ["academic year", "semester", "schedule", "calendar"],
        "grading system": ["grading", "grades", "cgpa", "marks", "evaluation"],
        "attendance": ["attendance", "present", "absent"],
        "exam": ["exam", "test", "assessment", "paper"]
    }
    
    # Check for exact matches or partial matches
    matches = process.extract(query, faqs.keys(), scorer=fuzz.partial_ratio, limit=3)

    if not matches:
        return "❌ No matching FAQs found."

    best_match, score, _ = matches[0]
    
    # If the best match is above a threshold, return the FAQ
    if score >= 50:
        return faqs[best_match]
    
    # If no clear match, try checking for synonyms
    for key, values in synonyms.items():
        if any(synonym in query for synonym in values):
            if key in faqs:
                return faqs[key]
    
    return "❌ Sorry, I couldn't find an exact match for your question. Please check the university website or contact the administration."

# Get best-matching FAQ answer
def get_academic_answer(question, faqs):
    """Find the best-matching FAQ answer based on the user's question."""
    faq_keys = list(faqs.keys())  # Extract all FAQ question keys
    
    if not faq_keys:
        return "❌ No FAQs found. Please check if the FAQ file exists and has valid data."
    
    # Refined matching logic with synonyms and partial matching
    return refine_matching_logic(question, faqs)

# New function to be used in chatbot.py
def handle_academic_query(question):
    """Handles academic queries by fetching the appropriate FAQ answer."""
    faqs = load_faqs()  # Load FAQs from the provided path
    if not faqs:  # If no FAQs were found, return an error message
        return "❌ Unable to load FAQs."
    
    return get_academic_answer(question, faqs)

# Main interactive loop (Optional: Remove or integrate as needed)
if __name__ == "__main__":  # Corrected the typo here
    faqs = load_faqs()  # Load FAQs once
    while True:
        question = input("Enter your academic query (or type 'exit' to quit): ").strip().lower()
        if question == "exit":
            break
        response = get_academic_answer(question, faqs)
        print(response)
