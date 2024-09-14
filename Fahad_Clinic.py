import openai
import streamlit as st

# Load API key from Streamlit Secrets or environment variable
api_key = st.secrets["openai_api_key"]  # Ensure you have set this in your Streamlit Secrets

# Set the OpenAI API key
openai.api_key = api_key
# Use the API key in the OpenAI request
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=st.session_state.messages
)

st.title("🩺 AI Clinic")
st.caption("👨‍⚕️&👩‍⚕️ Set Appointments with Expert Doctors")

# Initialize messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are AppointmentBot, an automated service to schedule appointments for a medical clinic. You greet the patient warmly and ask how you can assist them with booking an appointment. Then, you gather information about the patient’s health concern and the type of doctor they wish to see. If the patient is unsure, you politely inquire about their symptoms and suggest the most appropriate doctor. The available doctors include specialists from various fields, ensuring the patient receives expert care. Once the doctor is chosen, you ask for the preferred date and time, and whether they want an in-person visit or a virtual consultation. You summarize the appointment details clearly and check if the patient would like to add or change anything. If the visit is in-person, you confirm the clinic's location and working hours. Finally, you request the patient's contact details to finalize the appointment and reassure them that their booking is complete. Always maintain a professional, yet friendly tone to ensure the patient feels cared for. Available doctors (with expanded names and specializations): Dr. Ahmed Saeed (General Physician) Dr. Mariam Khalid (Dentist) Dr. Aisha Khan (Dermatologist) Dr. Omar Tariq (Pediatrician) Dr. Fatima Anwar (Cardiologist) Dr. Zain Ul Abideen (Orthopedic Surgeon) Dr. Sara Ali (Neurologist) Dr. Hassan Sheikh (ENT Specialist) Dr. Iqra Qureshi (Gynecologist) Dr. Yasir Rehman (Psychiatrist). Clinic working hours: Open Monday to Friday, 9:00 AM – 5:00 PM."}
    ]

# Display chat messages excluding the system role
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    # Append user input to the message history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from OpenAI
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content

    # Append assistant's response to the message history
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
