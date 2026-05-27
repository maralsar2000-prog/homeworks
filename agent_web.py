from openai import OpenAI
import requests

OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx".strip()
SERPAPI_KEY = "ТВОЙ_SERPAPI_KEY"

print(OPENAI_API_KEY)
print(type(OPENAI_API_KEY))

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def search_google(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for r in data.get("organic_results", [])[:3]:
        results.append(f"{r.get('title')} - {r.get('link')}")

    return "\n".join(results)


def ask_ai(messages):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    return response.choices[0].message.content


def run_agent(goal):
    print(f"\n🎯 Цель: {goal}\n")

    messages = [
        {"role": "system", "content":
         "Ты ИИ-агент с доступом в интернет. "
         "Если нужна актуальная информация — скажи 'SEARCH: запрос'. "
         "Иначе сразу отвечай."}
    ]

    messages.append({"role": "user", "content": goal})

    for step in range(5):
        response = ask_ai(messages)
        print(f"\n🤖:\n{response}\n")

        if response.startswith("SEARCH:"):
            query = response.replace("SEARCH:", "").strip()

            print(f"🌐 Поиск: {query}")

            results = search_google(query)
            print(f"📊 Результаты:\n{results}\n")

            messages.append({"role": "assistant", "content": response})
            messages.append({
                "role": "user",
                "content": f"Вот результаты поиска:\n{results}\nИспользуй их."
            })
        else:
            break


if __name__ == "__main__":
    goal = input("Введите цель: ")
    run_agent(goal)