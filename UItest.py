import streamlit as st
import os
import openai

# Set page configuration
st.set_page_config(
    page_title="COCO Bot Training UI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for Authentication and Title
with st.sidebar:
    st.title("COCO Training UI 🤖")
    auth_token = st.text_input("Enter Authentication Token:")

if auth_token == "your_dummy_token":
    st.write("Authenticated 👍")

    # Initialize conversation history and feedback
    conversation_history = []
    feedback_history = []

    # Configure API
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_base = os.getenv('OPENAI_API_BASE', "https://cocochat.openai-azure.com/")
    openai.api_key = os.getenv("OPENAI_API_KEY", '8aacb253f3ca4c29a44d56ef25cbb51f')

    # Main Chat Window
    st.write("---")

    # Chat window at the bottom
    chatbot_output = st.empty()
    user_input = st.text_input("You (Practitioner) 👨‍⚕️:", key="user_input")

    if st.button("Send "):
        try:
            # API call
            completion = openai.ChatCompletion.create(
                engine="text-davinci-002",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            generated_text = completion.choices[0].message.content

            # Update conversation history
            conversation_history.append({"user": user_input, "chatbot": generated_text})
            chatbot_output.write(f"Coco (Therapist) 🤖: {generated_text}")

        except Exception as e:
            st.write(f"An error occurred: {e} 😢")

        # Record user feedback
        feedback = st.radio("Was this response helpful? 👍👎", ("Yes 👍", "No 👎"))
        explanation = st.text_input("Explanation for your assessment 📝:", key="explanation")
        if st.button("Submit Feedback 📤"):
            feedback_history.append({"feedback": feedback, "explanation": explanation})

        # Save conversation and feedback to a database (dummy function)
        if st.button("Save Conversation 💾"):
            st.write("Saved to database 🎉")

    # Reset conversation
    if st.button("Reset Conversation 🔄"):
        conversation_history = []
        feedback_history = []
        chatbot_output.write("")
        st.write("Conversation reset 🌟")

else:
    st.write("Not Authenticated 😢")
