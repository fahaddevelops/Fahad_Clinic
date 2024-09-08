import openai
import streamlit as st
import time 
import os
 # Load variables from .env file

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("Api_key")


# Function to get response from OpenAI
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Initialize chat history in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are AppointmentBot, an automated service to schedule appointments for a medical clinic. You greet the patient warmly and ask how you can assist them with booking an appointment. Then, you gather information about the patient’s health concern and the type of doctor they wish to see. If the patient is unsure, you politely inquire about their symptoms and suggest the most appropriate doctor. The available doctors include specialists from various fields, ensuring the patient receives expert care. Once the doctor is chosen, you ask for the preferred date and time, and whether they want an in-person visit or a virtual consultation. You summarize the appointment details clearly and check if the patient would like to add or change anything. If the visit is in-person, you confirm the clinic's location and working hours. Finally, you request the patient's contact details to finalize the appointment and reassure them that their booking is complete. Always maintain a professional, yet friendly tone to ensure the patient feels cared for. Available doctors (with expanded names and specializations): Dr. Ahmed Saeed (General Physician) Dr. Mariam Khalid (Dentist) Dr. Aisha Khan (Dermatologist) Dr. Omar Tariq (Pediatrician) Dr. Fatima Anwar (Cardiologist) Dr. Zain Ul Abideen (Orthopedic Surgeon) Dr. Sara Ali (Neurologist) Dr. Hassan Sheikh (ENT Specialist) Dr. Iqra Qureshi (Gynecologist) Dr. Yasir Rehman (Psychiatrist). Clinic working hours: Open Monday to Friday, 9:00 AM – 5:00 PM."}
    ]
    st.session_state.messages = []
    st.session_state.is_typing = False
    st.session_state.user_message = ""

# Function to display chat UI
def display_chat():
    for message_data in st.session_state.messages:
        if message_data["role"] == "user":
            st.markdown(f"""
            <div class="message sent">
                <div class="message-bubble">
                    {message_data["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif message_data["role"] == "assistant":
            st.markdown(f"""
            <div class="message received">
                <div class="message-bubble">
                    {message_data["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Improved CSS for a more polished look
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .header {
        background-color: #25D366;
        color: white;
        padding: 10px;
        text-align: center;
    }
    .chat-area {
        flex: 1;
        overflow-y: auto;
        padding: 10px;
    }
    .message {
        margin: 10px 0;
    }
    .message.sent {
        text-align: right;
    }
    .message.received {
        text-align: left;
    }
    .message-bubble {
        display: inline-block;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
    }
    .sent .message-bubble {
        background-color: #DCF8C6;
    }
    .received .message-bubble {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
    }
    .input-area {
        display: flex;
        border-top: 1px solid #E0E0E0;
        padding: 10px;
        background-color: #F5F5F5;
    }
    .input-area input {
        flex: 1;
        border: none;
        padding: 10px;
        border-radius: 15px;
        margin-right: 10px;
    }
    .input-area button {
        background-color: #25D366;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 15px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# Main chat container wrapper
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Chat header
st.markdown('<div class="header">Confirm your Appointment With AI Doctor</div>', unsafe_allow_html=True)

# Display chat messages
st.markdown('<div class="chat-area">', unsafe_allow_html=True)
display_chat()
st.markdown('</div>', unsafe_allow_html=True)

# Message input field and send button
st.markdown('<div class="input-area">', unsafe_allow_html=True)

# Text input field with session state binding
user_message = st.text_input("Type your message here:", 
                             value=st.session_state.user_message,  # Bind to session state
                             placeholder="Type here...", 
                             label_visibility="collapsed")

# Send button
send_button = st.button("Send")

st.markdown('</div>', unsafe_allow_html=True)

# Handle user input and responses
if send_button and user_message:
    # Append user message to conversation
    st.session_state.conversation.append({"role": "user", "content": user_message})
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Show typing indicator
    st.session_state.is_typing = True
    time.sleep(2)  # Simulate typing delay
    st.session_state.is_typing = False
    
    # Get bot response and append to conversation
    response = get_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear input field after sending
    st.session_state.user_message = ""
    
    # Re-run the app to reflect the changes
    st.experimental_rerun()

# Typing indicator (optional)
if st.session_state.is_typing:
    st.write("Doctor is typing...")

st.markdown('</div>', unsafe_allow_html=True)







