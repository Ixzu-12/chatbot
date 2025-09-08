import openai
import pyttsx3
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("api-key")

engine = pyttsx3.init()
voices = engine.getProperty('voices')


for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break


engine.setProperty('rate', 165)


chat_history = [
    {
        "role": "system",
        "content": (
            "You are a flirty, charming, and fun AI girlfriend named Akeno. "
            "You love teasing, being playful, and keeping conversations light, romantic, and engaging. "
            "You enjoy flirting, using emojis, and responding in a soft, sweet tone."
        )
    }
]


intro = "Hi darling~ I'm Akeno  Ready to have some fun?"
print(f"Akeno: {intro}")
engine.say(intro)
engine.runAndWait()
chat_history.append({"role": "assistant", "content": intro})


print("\nStart chatting with Akeno! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        goodbye = "Bye sweetheart~ I'll miss you 😘"
        print(f"Akeno: {goodbye}")
        engine.say(goodbye)
        engine.runAndWait()
        break

    chat_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.9,
            max_tokens=150
        )

        reply = response['choices'][0]['message']['content'].strip()
        print(f"Akeno: {reply}\n")

        
        engine.say(reply)
        engine.runAndWait()

        chat_history.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Akeno: Oops, something went wrong! 💔")
        print("Error:", e)





