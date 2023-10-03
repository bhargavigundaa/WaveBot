import requests
import time
import streamlit as st

# Function to make an API call and fetch JSON data
def fetch_data(data):
    # Define the API URL
    api_url = "http://localhost:5000/api/question"  # Replace with the actual API URL

    try:
        response = requests.post(api_url, json = data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - Unable to fetch data from the API.")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

st.title('🤖💬 WaveBot')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = fetch_data({"question": prompt})
        print(assistant_response, 'assistant_response')
        # Simulate stream of response with milliseconds delay
        for document in assistant_response['source_documents']:
            page_content = document['page_content']
            for chunk in page_content.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response + "\n")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
