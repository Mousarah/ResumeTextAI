from dotenv import load_dotenv
import openai
import PyPDF2
import docx
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_content = """
Você é um chatbot para telegram que recebe um arquivo de texto pelo 
contexto e deve responder perguntas exclusivamente sobre esse 
contexto.
"""


class ChatAI:
    @staticmethod
    def process_txt(file_data):
        return file_data.decode('utf-8')

    @staticmethod
    def process_docx(file_data):
        from io import BytesIO
        doc = docx.Document(BytesIO(file_data))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    @staticmethod
    def process_pdf(file_data):
        from io import BytesIO
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_data))
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

    @staticmethod
    def answer_question_with_context(context, question):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Contexto: {context}"},
                {"role": "user", "content": f"Pergunta: {question}"}
            ],
        )
        return response.choices[0].message.content

    def run(self, file_name, file_data, question):
        if file_name.endswith('.txt'):
            context = self.process_txt(file_data)
        elif file_name.endswith('.docx'):
            context = self.process_docx(file_data)
        elif file_name.endswith('.pdf'):
            context = self.process_pdf(file_data)
        else:
            context = "Formato de arquivo não suportado."

        if context:
            return self.answer_question_with_context(context, question)

        return "Erro ao processar resposta."
