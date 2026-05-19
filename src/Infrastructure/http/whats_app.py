import os
import random
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)
    
    @staticmethod
    def generate_code():
        token_codigo = str(random.randint(1000, 9999))
        return token_codigo
    
    def send_activation_message(self, to_number, code):
        message = self.client.messages.create(
            body=f'Seu código de ativação é: {code}',
            from_=f'whatsapp:{self.from_number}',
            to=f'whatsapp:{to_number}'
        )
        print(f'Mensagem enviada: SID {message.sid}')