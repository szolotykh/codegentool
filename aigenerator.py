import os
from openai import OpenAI

class AIGenerator:
    def __init__(self, model_engine):
        self.model_engine = model_engine
        self.client = OpenAI()

    def generate_code(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model_engine,
            messages=messages,
            max_tokens=3000,
            tools=[
                {
                    "type":"function",
                    "function":{
                        "description":"Delete file from repository",
                        "name":"delete_file",
                        "parameters":{
                            "type": "object",
                            "properties": {
                                "fileName": {"type": "string", "description": "Name of the file that should be deleted"},
                            },
                            "required": ["fileName"]
                        }
                    }
                }
            ]
        )
        return completion.choices[0].message