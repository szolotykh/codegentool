import os
from openai import OpenAI

class AIGenerator:
    def __init__(self, model_engine):
        self.model_engine = model_engine
        self.client = OpenAI()

    def generate_analisys(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model_engine,
            messages=messages,
            max_tokens=5000,
        )
        return completion.choices[0].message

    def generate_repository_update(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model_engine,
            messages=messages,
            max_tokens=5000,
            tools=[
                {
                    "type":"function",
                    "function":{
                        "description":"Create or update file in repository",
                        "name":"create_or_update_file",
                        "parameters":{
                            "type": "object",
                            "properties": {
                                "file_name": {"type": "string", "description": "Name of the file that should be created or updated"},
                                "file_content": {"type": "string", "description": "Content of the file that should be created or updated"},
                            },
                            "required": ["file_name", "file_content"]
                        }
                    }
                },
                {
                    "type":"function",
                    "function":{
                        "description":"Delete file from repository",
                        "name":"delete_file",
                        "parameters":{
                            "type": "object",
                            "properties": {
                                "file_name": {"type": "string", "description": "Name of the file that should be deleted"},
                            },
                            "required": ["file_name"]
                        }
                    }
                }
            ]
        )
        return completion.choices[0].message