from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)  # Создать новое приложение

DB_FILE = "db.json"


def load_messages():
    with open(DB_FILE, "r") as json_file:
        data = json.load(json_file)
    return data["messages"]


all_messages = load_messages()  # Список всех сообщений в мессенджере


def save_messages():
    data = {
        "messages": all_messages
    }
    with open(DB_FILE, "w") as json_file:
        json.dump(data, json_file)

@app.route("/")
def index_page():
    return "Hello <b>Skillbox</b>!"


# Получить список всех сообщений
# Библиотека Фласк сама кодирует все данные в JSON если фун-ю возвращает словарь
@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


# Функция для вывода сообщений
def print_message(message):
    print(f"— [{message['sender']}] {message['text']} / {message['time']}")


@app.route("/chat")
def display_chat():
    return render_template("form.html")


@app.route("/send_message")
def send_message():
    # получить из запроса имя отправителя и текст
    sender = request.args["name"]
    text = request.args["text"]
    add_message(sender, text)
    save_messages()
    return "OK"


# Функция для добавления новых сообщений
def add_message(sender, text):
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    # .append = добавление в список
    all_messages.append(new_message)


# Для каждого сообщения в списке all_messages
for message in all_messages:
    print_message(message)

app.run()
