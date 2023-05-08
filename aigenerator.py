import os
import openai

class AIGenerator:
    def __init__(self, model_engine):
        self.model_engine = model_engine
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        openai.api_key = self.openai_api_key

    def generate_code(self, conversation):
        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=conversation,
            max_tokens=3000,
        )
        return response.choices[0].text