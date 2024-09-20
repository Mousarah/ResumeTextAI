from beans import file
import sqlite3


class UserDAO:
    def __init__(self):
        self.conn = sqlite3.connect("resume_text_ai.db")
        self.cursor = self.conn.cursor()

    def __close(self):
        if self.conn:
            self.conn.close()

    def insert_chat_file(self, chat_id, file_name, file_data):
        try:
            self.cursor.execute("DELETE FROM chats WHERE CHAT_ID = ?", (chat_id,))
            self.cursor.execute("INSERT INTO chats (CHAT_ID, FILE_NAME, FILE) VALUES (?, ?, ?)", (chat_id, file_name, file_data))
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        self.conn.commit()
        self.__close()

    def get_file_by_chat_id(self, chat_id):
        file_instance = None
        try:
            self.cursor.execute("SELECT FILE_NAME, FILE FROM chats WHERE CHAT_ID = ?", (chat_id,))
            result = self.cursor.fetchone()
            if result:
                file_instance = file.File(result[0], result[1])
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        self.__close()
        return file_instance

    def delete_chat_file(self, chat_id):
        try:
            self.cursor.execute("DELETE FROM chats WHERE CHAT_ID = ?", (chat_id,))
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        self.conn.commit()
        self.__close()
