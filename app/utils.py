import openai
import os
from dotenv import load_dotenv
from .crud import create_message, get_history_by_username

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_openai(username: str, question: str, role: str, session):
    try:
        history = get_history_by_username(session, username)

        messages = [{"role": "system",
                     "content": f"You are a highly knowledgeable {role}. "
                                f"You are strictly prohibited from providing information outside of this role. "
                                f"Always respond as an expert in this field and avoid unrelated topics."}]

        for msg in history:
            messages.append({"role": "user", "content": msg.question})
            messages.append({"role": "assistant", "content": msg.response})

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )

        bot_response = response.choices[0].message['content']

        create_message(session, username, question, bot_response)

        return bot_response
    except Exception as e:
        return f"Error with OpenAI API: {e}"
