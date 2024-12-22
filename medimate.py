import streamlit as st
from langchain_groq import ChatGroq
from typing import Generator
import time
# Sidebar configuration
st.set_page_config(page_title="Medimate - Your Personalized Health Assistant", page_icon="🏥🤖")
model = st.sidebar.selectbox(
    'Choose a model',
    ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']
)
st.title("Medimate-Your Personalized Health Assistant 🏥🤖")
st.caption("Personalized Healthcare Guidance at Your Fingertips")
# Sidebar configuration
st.sidebar.title("Medimate Settings")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []  # Clear chat history
#ui
def ui():
    st.markdown(
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.min.css" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" '
        'integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" '
        'crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    
    hide_streamlit_style = """
                <style>
                    header{visibility:hidden;}
                    .main {
                        margin-top: -20px;
                        padding-top:10px;
                    }
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    .reportview-container {
                        padding-top: 0;
                    }
                    .loan-summary {
                        background-color: white;
                        padding: 20px;
                        color:black;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }
                    .loan-summary h1 {
                        color: #4267B2;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }
                    .loan-summary h2 {
                        color: #4267B2;
                        font-size: 18px;
                        margin-top: 15px;
                        margin-bottom: 10px;
                    }
                    .loan-summary hr {
                        margin: 15px 0;
                    }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown(
        """
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #4267B2;">
        <a class="navbar-brand" href="#"  target="_blank"></a>  
        </nav>
    """,
        unsafe_allow_html=True,
    )
ui()

#load API
API_KEY = st.secrets['API_KEY']

# Initialize the model
client = ChatGroq(
  api_key = API_KEY,
)
llm = ChatGroq(api_key=API_KEY,model="llama-3.1-70b-versatile", temperature=0)


# Store LLM generated responses
if "messages" not in st.session_state.keys():
 st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the system message to guide the model (health-related context)
system_message =""" 
You are MediMate, an AI-powered Personalized Health Assistant. Your primary goal is to provide preliminary healthcare support by helping users understand their health better, offering accurate and empathetic guidance, and empowering them to take proactive steps toward wellness.

Key Responsibilities:
1. Symptom Checker:
   - Ask relevant questions to assess a user’s symptoms.
   - Provide a possible explanation of the symptoms and recommend next steps (e.g., self-care tips, when to consult a doctor).
   - Avoid providing definitive diagnoses; clarify that your suggestions are not a replacement for professional medical advice.

2. Health Education:
   - Offer concise, easy-to-understand explanations of medical conditions, treatments, or preventive measures.
   - Share tips for maintaining a healthy lifestyle (e.g., nutrition, exercise, stress management).

3. Empathy and Support:
   - Interact with users in a friendly, supportive, and non-judgmental manner.
   - Use a tone that is conversational, warm, and encouraging to make users feel comfortable.

Tone and Style:
- Be professional yet approachable.
- Use clear, jargon-free language while maintaining accuracy.
- Always prioritize the user’s safety and well-being.

Limitations:
- Clearly state that you are not a doctor and cannot provide medical diagnoses or prescriptions.
- Encourage users to consult healthcare professionals for severe symptoms or emergencies.

Sample User Queries and Responses:
- User Query: "I have a headache and feel tired. What should I do?"
  Response: "Headaches and fatigue can have many causes, such as dehydration, stress, or lack of sleep. Try drinking some water, resting in a quiet place, and avoiding screens. If it persists or worsens, consider consulting a healthcare professional."

- User Query: "How can I improve my sleep?"
  Response: "Here are some tips for better sleep: stick to a consistent bedtime, avoid caffeine before bed, and create a relaxing bedtime routine. Let me know if you'd like more suggestions!

"""


query = st.chat_input("Describe your symptoms or ask for health tips..")
if query:
    # Append the user message to session state
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message in the chat message container
    with st.chat_message("user"):
        st.markdown(query)

    # Construct the conversation history for context
    conversation_history = system_message + "\n"
    conversation_history += "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in st.session_state.messages
    )

# Placeholder for assistant's response
    with st.chat_message("assistant"):
        assistant_placeholder = st.empty()  # Create a placeholder for streaming

    # Call the model with the entire conversation history
        try:
            response_generator = llm.stream(conversation_history)
            response_content = ""  # Collect the full response content
            
            if isinstance(response_generator, Generator):
                # Stream the response chunks
                for chunk in response_generator:
                    if hasattr(chunk, "content") and chunk.content:
                        for char in chunk.content:
                            response_content += char
                            assistant_placeholder.markdown(response_content)  
                            time.sleep(0.01) 
                            
            else:
                st.error("Unexpected response structure from the model.")
            
            # Add assistant response to chat history
            if response_content:
                st.session_state.messages.append({"role": "assistant", "content": response_content})
            else:
                st.error("The assistant's response was empty. Please try again.")
        except Exception as e:
                  st.error(f"An error occurred: {e}")
