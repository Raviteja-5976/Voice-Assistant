import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage
import datetime
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import random
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()
api_key = 'YOUR_OPENAI_API_KEY'
client = OpenAI(api_key=api_key)

wh_api_key = "YOUR_OPENWEATHER_API_KEY"

def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def send_email(email_address, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Replace with your email and password
        sender_email = 'raviteja.gdsc@gmail.com'
        sender_password = 'Password'
        server.login(sender_email, sender_password)
        email = EmailMessage()
        email['From'] = sender_email
        email['To'] = email_address
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)
        server.quit()
        talk("Email sent successfully.")
    except Exception as e:
        talk(f"An error occurred: {e}")



def get_email_info():
    try:
        talk('Please tell me the email address of the recipient.')
        email_address = input()  # Use get_info to get the email address
        talk('What is the subject of your email?')
        subject = get_info()
        talk('Tell me the text in your email')
        text = get_info()
        message = text_message_email(text)
        send_email(email_address, subject, message)
        talk('Hey. Your email is sent.')
        talk('Do you want to send more email?')
        send_more = get_info()
        if 'yes' in send_more:
            get_email_info()
    except Exception as e:
        talk(f"An error occurred: {e}")


def text_message_email(email_info):
    talk('Please tell me the name of the recipient')
    to_name = input()
    send_name = 'Raviteja Karnati'
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an email writer. You only write short emails with only 100 words"},
        {"role": "user", "content": f'You have to write the email to this person called {to_name} with the subject of {email_info}. The sender name is {send_name}'}
    ]
    )

    response = completion.choices[0].message
    result = response.content
    talk(result)
    return result



def simple_gpt():
    talk('Hello! I am your assistant. How can I help you today?')

    # Initialize an empty list to store the conversation
    conversation = []

    while True:
        # Get user input
        user_input = get_info()

        # Check if the user wants to end the conversation
        if 'end the conversation' in user_input:
            talk('Ending the conversation. How can I help you in the next conversation?')
            # Clear the conversation to start a new one
            conversation = []
            continue

        # Add user input to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Get GPT-3.5 Turbo response based on the entire conversation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Get assistant's reply
        assistant_reply = response["choices"][0]["message"]["content"]

        # Print and speak the assistant's reply
        talk(assistant_reply)

        # Add assistant's reply to the conversation
        conversation.append({"role": "assistant", "content": assistant_reply})

def text_message(user_input):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]
    )

    response = completion.choices[0].message
    result = response.content
    return result

def dumb_bot():

    talk('What is your question, Sir!')
    user_input = get_info()
    response = text_message(user_input= user_input)
    talk(response)


def gen_photo():
    talk('Sir, Please tell me what I have to create')
    prompt = input() # Use get_info() to get the user input

    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    # gen_url = response["data"][0]["url"]
    rep = requests.get(image_url)
    img_data = BytesIO(rep.content)

    img = Image.open(img_data)
    img.show()
    talk('Here is the generated photo for the provided prompt.')
def get_weather(api_key, city=None):
    if not city:
        talk("Please tell me the name of the city.")
        city = get_info()

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            main_weather = data['weather'][0]['main']
            description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']

            weather_report = f"The weather in {city} is {main_weather}, {description}. "
            weather_report += f"The temperature is {temperature} degrees Celsius, and humidity is {humidity}%."

            talk(weather_report)
        else:
            error_message = f"Error: {data['message']}"
            talk(error_message)

    except requests.RequestException as e:
        error_message = f"Error: {e}"
        talk(error_message)

def youtube_open(query):
    youtube_url = "https://www.youtube.com/results?search_query="
    search_query = query.replace(' ', '+')
    search_url = f"{youtube_url}{search_query}"

    webbrowser.open(search_url)

intents = {
    # ... (Your intents dictionary here)
    "greetings": {
        "patterns": ["hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening", "hi there", "hey there", "what's up", "hello there"],
        "responses": ["Hello! How can I assist you?", "Hi there!", "Hey! What can I do for you?", "Howdy! What brings you here?", "Greetings! How may I help you?", "Good morning! How can I be of service?", "Good afternoon! What do you need assistance with?", "Good evening! How may I assist you?", "Hey there! How can I help?", "Hi! What's on your mind?", "Hello there! How can I assist you today?"]
    },
    "goodbye": {
        "patterns": ["bye", "see you later", "goodbye", "farewell", "take care", "until next time", "bye bye", "catch you later", "have a good one", "so long"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!", "Farewell! Take care.", "Goodbye! Until next time.", "Take care! Have a wonderful day.", "Bye bye!", "Catch you later!", "Have a good one!", "So long!"]
    },
    "gratitude": {
        "patterns": ["thank you", "thanks", "appreciate it", "thank you so much", "thanks a lot", "much appreciated"],
        "responses": ["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!", "You're welcome! Have a great day.", "No problem!"]
    },
    "apologies": {
        "patterns": ["sorry", "my apologies", "apologize", "I'm sorry"],
        "responses": ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay.", "Don't worry about it.", "Apology accepted."]
    },
    "positive_feedback": {
        "patterns": ["great job", "well done", "awesome", "fantastic", "amazing work", "excellent"],
        "responses": ["Thank you! I appreciate your feedback.", "Glad to hear that!", "Thank you for the compliment!", "I'm glad I could meet your expectations.", "Your words motivate me!", "Thank you for your kind words."]
    },
    "negative_feedback": {
        "patterns": ["not good", "disappointed", "unsatisfied", "poor service", "needs improvement", "could be better"],
        "responses": ["I'm sorry to hear that. Can you please provide more details so I can assist you better?", "I apologize for the inconvenience. Let me help resolve the issue.", "I'm sorry you're not satisfied. Please let me know how I can improve.", "Your feedback is valuable. I'll work on improving."]
    },
    "weather": {
        "patterns": ["what's the weather like?", "weather","weather forecast", "is it going to rain today?", "temperature today", "weather report"],
        # "responses": [f"The weather today is [weather_description].", "Currently, it's [temperature] degrees with [weather_description].", "The forecast predicts [weather_forecast].", "It might rain today. Don't forget your umbrella!", "The temperature today is [temperature] degrees."]
        "responses": [""]
    },
    "help": {
        "patterns": ["help", "can you help me?", "I need assistance", "support","I want to talk to you"],
        "responses": ["Sure, I'll do my best to assist you.", "Of course, I'm here to help!", "How can I assist you?", "I'll help you with your query."]
    },
    "time": {
        "patterns": ["what's the time?", "current time", "time please", "what time is it?","What's the time now", "what is the time now"],
        "responses": [""]
    },
    "email":{
        "patterns": ["mail","send email", "email someone", "compose an email", "write an email", "email"],
        "responses": [
            "Sure, I can help you compose and send an email. Who is the recipient?",
            "Sending emails is my specialty. Who would you like to email?",
            "Certainly! Please provide the details for the email. Who are you emailing?"
    ]
    },
    "image_creation":{
            "patterns": ["create image", "generate a photo", "make an image", "generate picture", "image creation","create an image"],
            "responses": [
                "Absolutely! I can help you generate an image. What should be the subject of the image?",
                "Creating images is something I'm good at. What kind of image would you like?",
                "Sure, I can generate an image for you. What should be in the picture?"
            ]
            },
    "youtube":{
            "patterns": [
        "YouTube",
        "watch videos",
        "find YouTube",
        "search YouTube",
        "YouTube channel",
        "YouTube videos",
        "watch YouTube",
        "YouTube tutorials",
        "YouTube recommendations",
        "YouTube entertainment",
        "YouTube content",
        "YouTube music",
        "YouTube news",
        "YouTube sports",
        "YouTube gaming"
    ],
    "responses": [
        "YouTube is a popular platform for watching a wide range of videos.",
        "You can find a variety of content on YouTube, from tutorials to entertainment.",
        "YouTube is a great source for videos on various topics.",
        "You can search for specific videos or channels on YouTube.",
        "If you have a specific YouTube channel in mind, you can search for it.",
        "YouTube offers a vast collection of videos for your enjoyment.",
        "Whether you're interested in music, news, sports, or gaming, YouTube has it all.",
        "Feel free to ask if you have any specific questions about YouTube."
    ]
    }
}

def process_input(user_input):
    # ... (Your process_input function here)
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            if pattern.lower() in user_input:
                response = random.choice(data["responses"])
                talk(response)
                # Call the specific function associated with the intent
                handle_intent(intent)
                return
    talk('Sir, do you want to ask a question or want to talk with me?')
    option = get_info()
    if 'ask a question' in option:
        dumb_bot()
    elif 'No' in option:
        main()

    else:
        dumb_bot()       

def handle_intent(intent):
    # ... (Your handle_intent function here)

        if intent == "greetings":
            main()


        elif intent == "goodbye":
            exit()


        elif intent == "gratitude":
            main()


        elif intent == "apologies":
            main()


        elif intent == "positive_feedback":
            main()


        elif intent == "negative_feedback":
            main()


        elif intent == "weather":
            get_weather(api_key=wh_api_key)


        elif intent == "help":
            dumb_bot()


        elif intent == "time":
            date = datetime.datetime.now()
            talk(f'Today date and time is {date}')


        elif intent == "email":
            get_email_info()


        elif intent == "image_creation":
            gen_photo()

        elif intent == "youtube":
            question = get_info()
            youtube_open(query= question)



        else:
            talk('Sir, do you want to ask a question or want to talk with me?')
            option = get_info()
            if 'ask a question' in option:
                dumb_bot()

            elif 'Talk with you' in option:
                dumb_bot()

            elif 'No' in option:
                main()

            else :
                main()

def main():
    while True:
        intent = get_info()
        process_input(intent)

if __name__ == "__main__":
    main()
