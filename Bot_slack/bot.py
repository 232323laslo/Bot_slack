import slack
import os
from dotenv import load_dotenv

# Завантаження змінних з .env файлу
load_dotenv()

# Отримання значення SLACK_BOT_TOKEN з середовищних змінних
slack_bot_token = os.environ["SLACK_TOKEN"]

# Ініціалізація клієнта Slack з авторизаційним токеном бота
client = slack.WebClient(token=slack_bot_token)

email_string = """
vladyslav_hryshchenko@proton.me
"""

message = """
---
"""

emails = email_string.strip().split()

success_users = []  # Список користувачів, кому вдалося надіслати повідомлення
failed_users = []  # Список користувачів, кому не вдалося надіслати повідомлення

for email in emails:
    response = client.users_lookupByEmail(email=email.strip())
    if response["ok"]:
        user_id = response["user"]["id"]
        response = client.conversations_open(users=user_id)
        if response["ok"]:
            channel_id = response["channel"]["id"]
            message_response = client.chat_postMessage(
                channel=channel_id,
                text=message,
                username="bot",
                icon_emoji=":robot_face:",
            )
            if message_response["ok"]:
                success_users.append(email)
                print(f"Повідомлення успішно надіслано користувачу з поштою {email}")
            else:
                failed_users.append(email)
                print(
                    f"Не вдалося надіслати повідомлення користувачу з поштою {email}: {message_response['error']}"
                )
        else:
            failed_users.append(email)
            print(
                f"Не вдалося відкрити приватний канал для користувача з поштою {email}: {response['error']}"
            )
    else:
        failed_users.append(email)
        print(f"Не вдалося знайти користувача за поштою {email}: {response['error']}")

# Вивід результатів в закриту групу "bot"
group_channel = "bot"
success_count = len(success_users)
failed_count = len(failed_users)

message = (
    f"Успішно надіслано повідомлення {success_count} користувачам:\n"
    f"{', '.join(success_users)}\n\n"
    f"Не вдалося надіслати повідомлення {failed_count} користувачам:\n"
    f"{', '.join(failed_users)}\n\n"
    f"Відправлено повідомлення:\n"
    f"{message}"
)

client.chat_postMessage(
    channel=group_channel, text=message, username="bot", icon_emoji=":robot_face:"
)
