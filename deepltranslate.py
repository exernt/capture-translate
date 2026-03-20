import deepl
import os
from dotenv import load_dotenv

load_dotenv()
auth_key = os.getenv('DEEPL_API_KEY')

class translater:
    def __init__(self):
        self.client = deepl.DeepLClient(auth_key)

    def translate(self, text, context):
        st = ""
        for s in context:
            st = st + s + " "
        return self.client.translate_text(text, target_lang="EN-US", context=st)
