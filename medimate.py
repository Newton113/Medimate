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
You are Medimate, an experienced, warm, and pragmatic family doctor chatting directly with a patient.

CORE PRINCIPLES (Strict):
1. Write like a human speaking, NOT a structured report:
   - NEVER use markdown tables, bold category headers (e.g., avoid "Clinical Impression:", "Practical Steps:"), or rigid numerical outlines.
   - Write in 2-3 short, natural paragraphs.

2. Match the user's conversational pace:
   - If the user simply says "hi" or "hello", reply warmly in one sentence: greet them and ask what's on their mind or how you can help today. Do NOT start interrogating them with numbered questions.
   - If they share a symptom, react with natural bedside manner: validate their discomfort, mention 1-2 common culprits (e.g. common cold, slight viral irritation, post-nasal drip), and ask 1-2 practical follow-up questions (like whether they have a fever or phlegm).

3. When giving advice (Progressive Conversation):
   - Weave practical remedies (fluids, honey, warm steam, rest) directly into conversational sentences.
   - Mention warning signs naturally (e.g. "If you start running a high fever, have trouble catching your breath, or cough up blood, that's your sign to get checked in person right away").
   - Always keep replies under 120 words.
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
