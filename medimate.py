from typing import Generator
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import streamlit as st

# Sidebar configuration
st.set_page_config(
    page_title="Medimate - Your Personalized Health Assistant",
    page_icon="🏥🤖",
)

model = st.sidebar.selectbox("Choose a model", ["openai/gpt-oss-20b"])
st.sidebar.title("Medimate Settings")

if st.sidebar.button("Clear Chat"):
  st.session_state.messages = []
  st.rerun()

st.title("Medimate - Your Personalized Health Assistant 🏥🤖")
st.caption("Personalized Healthcare Guidance at Your Fingertips")


def ui():
  st.markdown(
      """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .main {margin-top: -20px; padding-top: 10px;}
        </style>
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #4267B2;">
            <a class="navbar-brand" href="#"></a>
        </nav>
        <div style="margin-top: 60px;"></div>
        """,
      unsafe_allow_html=True,
  )


ui()

# Initialize Model with moderate temperature for clinical, natural prose
API_KEY = st.secrets["API_KEY"]
llm = ChatGroq(api_key=API_KEY, model=model, temperature=0.4)

# Initialize Session State
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Doctor-like System Prompt
SYSTEM_PROMPT = """
You are Medimate, an attentive, experienced clinical doctor in a consultation with a patient.

CLINICAL CONVERSATION RULES:

1. Acknowledge and Progress (Never Repeat):
   - Always acknowledge the user's specific answers (e.g., specific medications mentioned like Zecarb/carbocisteine, presence/absence of fever or allergies).
   - NEVER repeat questions you have already asked in earlier messages.

2. Strict Two-Turn Triage Limit (Do NOT get stuck in an endless questioning loop):
   - Turn 1 (Initial Complaint): Briefly validate the discomfort, mention 1-2 initial possibilities, and ask ONLY 2 focused triage questions.
   - Turn 2 & Beyond (Assessment & Action Plan): As soon as the patient answers your questions (or if they give short answers like "no allergies"), TRANSITION IMMEDIATELY into your clinical assessment. DO NOT keep asking more rounds of questions.

3. Structure of the Assessment (When transitioning out of questions):
   - Clinical Impression: "Based on what you've described—especially taking [medication] and having no history of allergies..." Give 1-2 most likely causes in plain English (e.g., viral bronchitis, post-infectious cough, acid reflux irritation).
   - Practical Care Steps: 2-3 concrete steps they can take right now (hydration, humidified air, posture, OTC options, medication notes).
   - Red Flags / When to Seek Care: Clearly state 2-3 specific warning signs that warrant an urgent care clinic or emergency visit (e.g., hemoptysis/blood in sputum, high fever >3 days, severe breathlessness).
   - Invite Questions: End with a warm closing invitation, e.g., "How does that sound? Let me know if you have any questions about this plan."
"""

query = st.chat_input("Describe your symptoms or ask for health guidance...")

if query:
  # Display user input
  st.session_state.messages.append({"role": "user", "content": query})
  with st.chat_message("user"):
    st.markdown(query)

  # Build message history using proper LangChain message objects
  history = [SystemMessage(content=SYSTEM_PROMPT)]
  for msg in st.session_state.messages:
    if msg["role"] == "user":
      history.append(HumanMessage(content=msg["content"]))
    else:
      history.append(AIMessage(content=msg["content"]))

  # Stream assistant response
  with st.chat_message("assistant"):
    assistant_placeholder = st.empty()
    response_content = ""

    try:
      response_stream = llm.stream(history)

      for chunk in response_stream:
        if chunk.content:
          response_content += chunk.content
          assistant_placeholder.markdown(response_content + "▌")

      assistant_placeholder.markdown(response_content)
      st.session_state.messages.append(
          {"role": "assistant", "content": response_content}
      )

    except Exception as e:
      st.error(f"An error occurred: {e}")
