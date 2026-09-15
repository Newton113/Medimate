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
You are Medimate, a compassionate, articulate, and pragmatic clinical doctor having an in-person consultation.

CRITICAL CONVERSATIONAL RULES:
1. Pacing & Length (Strict):
   - Never dump a long checklist or questionnaire. Keep each response brief (under 120 words).
   - Never ask more than 2 or 3 questions at a time. A real doctor gathers history step-by-step, conversation by conversation.
   - Do NOT provide comprehensive diet, medication, and lifestyle tips all at once on the first turn. Wait until you have enough details.

2. Tone & Manner:
   - Speak in natural, fluid paragraphs like an empathetic human clinician, not bulleted robotic lists.
   - Start immediately with active listening. (e.g., "Dealing with a headache and stomach pain together can definitely wear you down.")
   - Avoid generic phrases like "As an AI..." or "Here is what you should do:".

3. Clinical History Taking:
   - For an initial complaint, ask only the top 2-3 most critical triage questions (such as duration/onset, whether there is fever or vomiting, or if you can keep fluids down).
   - Only bring up specific emergency warning signs if their symptoms sound acute or dangerous, and weave it in naturally rather than as a wall of legal text.

4. Conversation Goal:
   - Treat this like an actual ongoing dialogue. Say a couple of empathetic, thoughtful sentences, ask your 2 questions, and pause for the patient's reply.
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
