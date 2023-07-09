from google.oauth2 import service_account
from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import ChatModel

class ChatBot:
    def __init__(self, acc_info: dict):
        my_credentials = service_account.Credentials.from_service_account_info(acc_info)
        aiplatform.init(credentials=my_credentials)
        vertexai.init(project=acc_info['project_id'], location="us-central1")
        chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.parameters = {
            "temperature": 0.8,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40,
        }
        self.chat = chat_model.start_chat()
    
    def send_msg(self, message: str):
        response = self.chat.send_message(message, **self.parameters)
        return response.text
