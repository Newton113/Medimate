---

# Medimate - Your Personalized Health Assistant

Medimate is an AI-powered health assistant designed to offer personalized healthcare guidance at your fingertips. With the power of language models, Medimate helps users understand their health better, provides symptom checks, health education, and offers empathetic support. It empowers individuals to make proactive decisions about their health and well-being.

---

## Features

- **Symptom Checker**: Helps users assess their symptoms by asking relevant questions and provides guidance based on the input.
- **Health Education**: Offers concise and easy-to-understand information about medical conditions, treatments, and preventive measures.
- **Empathetic Support**: Provides a warm, conversational, and non-judgmental tone to ensure users feel comfortable while seeking healthcare advice.
- **Customizable Model Selection**: Choose from multiple AI models to interact with the assistant based on user preferences.

---

## Installation

To set up Medimate locally or on your server, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medimate.git
cd medimate
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the necessary Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Medimate relies on an API to interact with an AI model. Set up your API key in the `secrets.toml` file or using environment variables.

**Example `secrets.toml`**:

```toml
[general]
API_KEY = "your_api_key_here"
```

### 5. Run the Application

After installation, run the Streamlit app:

```bash
streamlit run app.py
```

Visit the app in your browser (usually `http://localhost:8501`) to start interacting with Medimate.

---

## How It Works

1. **User Input**: The user enters a symptom description or health query into the input field.
2. **Conversation History**: The user's messages are stored and form the conversation history.
3. **Assistant Response**: The model processes the user's input and provides a personalized response based on the context and pre-defined system message guiding health-related interactions.
4. **Symptom Check and Education**: Medimate can perform a preliminary health check by asking relevant questions and offer health tips or explanations about symptoms and conditions.
   
---

## Technologies Used

- **Streamlit**: For building the interactive web app.
- **Langchain + Groq**: The AI model integration for generating personalized healthcare responses.
- **Bootstrap 4**: For styling the app and making it responsive.
- **Python**: The backend language for processing user input and generating responses.
  
---

## Future Improvements

- **Multi-Language Support**: Adding support for multiple languages to make Medimate accessible globally.
- **Voice Integration**: Allowing users to interact with Medimate using voice commands.
- **Advanced Diagnostics**: Offering more in-depth diagnostic advice based on the user's symptoms (in partnership with health professionals).
  
---

## Contributing

We welcome contributions! If you want to improve or extend the functionality of Medimate, feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to your branch (`git push origin feature-name`)
5. Create a new pull request

---

## Acknowledgements

- Thanks to **Langchain** and **Groq** for their powerful AI model integration.
- Inspired by the need for accessible health assistance for everyone.
- Thanks to my machine learning facilitators Eyram Dela & Jeremiah Ayensu
- Thanks to the entire team at Trestle Academy Ghana

---
