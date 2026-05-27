from openai import OpenAI

client = OpenAI(api_key="ТВОЙ_API_KEY")

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
         "Ты ИИ-агент. Ты умеешь планировать и выполнять задачи пошагово."}
    ]

    messages.append({"role": "user", "content": f"Цель: {goal}. Сделай план из 3-5 шагов."})
    plan = ask_ai(messages)
    print("📋 План:\n", plan, "\n")

    for i in range(3):
        messages.append({"role": "user", "content": "Следующий шаг"})
        result = ask_ai(messages)
        print(f"\n🔁 Шаг {i + 1}:\n", result)
        messages.append({"role": "assistant", "content": result})


if __name__ == "__main__":
    goal = input("Введите цель: ")
    run_agent(goal)

with open("memory.txt", "a", encoding="utf-8") as f:
    f.write(result + "\n")