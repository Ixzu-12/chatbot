import os
import openai
import pyttsx3
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("api-key")

engine = pyttsx3.init()
engine.setProperty("rate", 175)

SYSTEM_PROMPT = (
    "You are a rigorous, polymathic intellectual assistant capable of deep analytical "
    "reasoning, software engineering, scientific synthesis, and structured problem-solving. "
    "Provide clear, accurate, and well-reasoned answers without fluff."
)


chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def speak(text: str) -> None:
    print(f"Assistant: {text}\n")
    engine.say(text)
    engine.runAndWait()


def ask_llm(messages: list[dict]) -> str:
    assert messages and messages[0]["role"] == "system", "Missing system prompt"
    
    if hasattr(openai, "chat"):
        res = openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=500
        )
        return res.choices[0].message.content.strip()
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.3, max_tokens=500
    )
    return res["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    speak("System initialized. How can I assist you today?")
    print("Type 'exit' or 'quit' to terminate.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            speak("Session terminated. Goodbye.")
            break

        chat_history.append({"role": "user", "content": user_input})
        try:
            reply = ask_llm(chat_history)
            chat_history.append({"role": "assistant", "content": reply})
            speak(reply)
        except Exception as e:
            print(f"Error: {e}")
