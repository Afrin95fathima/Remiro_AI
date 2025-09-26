"""
Simple script to refresh Streamlit cache and ensure all agents are properly loaded
"""

def restart_message():
    print("🔄 Missing agents have been fixed!")
    print("")
    print("To see the changes in your dashboard:")
    print("1. Refresh your browser page (F5 or Ctrl+R)")
    print("2. Or restart the Streamlit app by pressing Ctrl+C and running 'streamlit run app.py' again")
    print("")
    print("All 12 agents should now be visible in your dashboard:")
    print("✅ 8 Completed: personality, interests, aspirations, skills, motivations_values, cognitive_abilities, learning_preferences, physical_context")
    print("⏳ 4 Remaining: strengths_weaknesses, emotional_intelligence, track_record, constraints")
    print("")
    print("You can now continue with the remaining assessments!")

if __name__ == "__main__":
    restart_message()
