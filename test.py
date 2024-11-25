import openai
import os
import time

# Установка API-ключа
openai.api_key = os.getenv("OPENAI_API_KEY")

# Создание клиента
client = openai.OpenAI(api_key=openai.api_key)

# Создание нового потока
thread = client.beta.threads.create()
print("Thread создан:", thread)

# Добавление сообщения пользователя
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Привет! Как тебя зовут?"
)
print("Сообщение добавлено:", message)

# Создание выполнения с использованием ассистента
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="id ассистента"
)
print("Run создан:", run)

# Ожидание завершения выполнения
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Статус выполнения: {run_status.status}")

    if run_status.status == "completed":
        break
    elif run_status.status == "failed":
        print("Выполнение завершилось с ошибкой.")
        exit()
    else:
        time.sleep(2)  # Ожидание 2 секунды перед повторной проверкой

# Получение сообщений из потока
messages = client.beta.threads.messages.list(thread_id=thread.id)
print("Сообщения:")
for msg in messages:
    print(f"{msg.role}: {msg.content[0].text.value}")