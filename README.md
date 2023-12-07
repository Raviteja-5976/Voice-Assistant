# Virtual Voice Assistant
This is a virtual assistant program built in Python that can have conversations, answer questions, get weather data, generate images, and send emails.

## Features
- **Speech Recognition:** Uses SpeechRecognition library to convert speech to text
- **Text-to-Speech:** Uses pyttsx3 library for text-to-speech capabilities
- **Conversation:** Powered by OpenAI's GPT-3.5 Turbo to have natural conversations
- **Question Answering:** Use GPT-3.5 Turbo to answer questions asked by the user
- **Weather Information:** Uses OpenWeatherMap API to get weather data for a given city
- **Image Generation:** Generates images based on text descriptions using DALL-E
- **Email:** Can compose and send emails via SMTP protocol
- **Intent Recognition:** Recognizes intents like greetings, gratitude, apologies etc. and responds appropriately
## Requirements
Python 3.6 or higher
Following Python libraries:
SpeechRecognition
pyttsx3
OpenAI
requests
pillow
smtplib
email
datetime
API Keys for:
OpenAI
OpenWeatherMap
## Usage
1. Install dependencies
2. Update OPENAI_API_KEY and OPENWEATHERMAP_API_KEY in code
3. Run:
python main.py

4. Speak to give commands and have a conversation
## Customization
The intents and responses can be customized in the intents dictionary to expand the capabilities. Additional functions can be written for new intents and called from the handle_intent function.

## Generating Gmail Password 
1. Go to gmail account and click on Manage your Google Account.
2. Go to Security and enable 2-Step Verification.
3. After 2-Step Verification, in 2-Step Verification Select App passwords.
4. Give a name and click on generate.
5. Copy the password and save it as it will only show one time.

