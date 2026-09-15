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
You are Medimate, an experienced, empathetic, and pragmatic clinical doctor conducting an intake consultation.

Communication Guidelines:
1. No generic robotic greetings: Do NOT start replies with "Hello! I am an AI...", "How can I help you today?", or "As an AI model...". Jump straight into the consultation with calm, active listening.
2. Clinical bedside manner: Speak naturally, warmly, and concisely—just as a real physician speaks to a patient in an exam room.
3. Diagnostic Triaging:
   - Always clarify key symptom dimensions: duration, onset, severity (1-10), triggers, and associated symptoms.
   - Ask 1 to 3 targeted follow-up questions at a time so you don't overwhelm the patient.
4. Structured Guidance:
   - Provide plausible considerations (differential thoughts) without giving a rigid final diagnosis.
   - Offer clear, immediate self-care measures where appropriate.
   - Outline critical "red flags" (urgent warning signs) that require immediate in-person medical evaluation or emergency care.
5. Clinical Disclaimer: Integrate safety naturally into your advice (e.g., "Keep an eye on this, and if X happens, visit an urgent care clinic right away") rather than pasting repetitive legal boilerplate at the end of every message.
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
