import streamlit as st
import json
import requests
import openai

# Dummy authentication token verification
auth_token = st.text_input("Enter Authentication Token:")
if auth_token == "your_dummy_token":
    st.write("Authenticated")

    # Initialize conversation history and feedback
    conversation_history = []
    feedback_history = []

    # Chat window
    st.title("COCO Training UI")
    user_input = st.text_input("You (Practitioner):")
    chatbot_output = st.empty()
    if st.button("Send"):
        # API call to GPT endpoint
        openai.api_key = '8aacb253f3ca4c29a44d56ef25cbb51f'
        openai.api_base = "https://cocochat.openai-azure.com/"
        openai.api_version = "2023-05-15"
        deployment_name = 'cocoGPT'
        
        # Making API call using openai library
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
        chatbot_output.write(f"Coco (Therapist): {generated_text}")

        # Record user feedback
        feedback = st.radio("Was this response helpful?", ("Thumb Up", "Thumb Down"))
        explanation = st.text_input("Explanation for your assessment:")
        if st.button("Submit Feedback"):
            feedback_history.append({"feedback": feedback, "explanation": explanation})

        # Save conversation and feedback to a database (dummy function)
        if st.button("Save Conversation"):
            # Replace with your actual database saving logic
            st.write("Saved to database")

    # Reset conversation
    if st.button("Reset Conversation"):
        conversation_history = []
        feedback_history = []
        chatbot_output.write("")
        st.write("Conversation reset")

else:
    st.write("Not Authenticated")
