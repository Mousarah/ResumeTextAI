from dotenv import load_dotenv
from dao import UserDAO
from ai import ChatAI
import telebot
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_KEY")
ALLOWED_EXTENSIONS = ['.pdf', '.txt', '.docx']

bot = telebot.TeleBot(TOKEN)


def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_docs(message):
    try:
        file_name = message.document.file_name
        if allowed_file(file_name):
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            UserDAO().insert_chat_file(message.chat.id, file_name, downloaded_file)
            bot.send_message(message.chat.id, f"Arquivo {file_name} importado com sucesso!")
        else:
            bot.send_message(message.chat.id, "Somente arquivos .pdf, .txt, ou .docx são permitidos.")
    except AttributeError:
        bot.send_message(message.chat.id, "Somente arquivos .pdf, .txt, ou .docx são permitidos.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao salvar o arquivo: {e}")


@bot.message_handler(commands=['clean'])
def clean(message):
    try:
        file_instance = UserDAO().get_file_by_chat_id(message.chat.id)
        if file_instance is not None:
            UserDAO().delete_chat_file(message.chat.id)
            bot.send_message(message.chat.id, "Arquivo deletado com sucesso!")
        else:
            bot.send_message(message.chat.id, "Nenhum arquivo encontrado.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao deletar arquivo: {e}")

    start(message)


@bot.message_handler(commands=['start'])
def start(message):
    reply = """
    Por favor importe um arquivo para iniciar!
    """

    has_file = UserDAO().get_file_by_chat_id(message.chat.id) is not None
    if has_file:
        reply = """
        O que deseja saber sobre o arquivo?
        """

    bot.send_message(message.chat.id, reply)


def verify(message):
    return True


@bot.message_handler(func=verify)
def general_chat(message):
    try:
        file_instance = UserDAO().get_file_by_chat_id(message.chat.id)
        if file_instance is not None and message.text != "":
            bot.send_message(message.chat.id, ChatAI().run(file_instance.name, file_instance.data, message.text))
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar resposta: {e}")


bot.polling()
