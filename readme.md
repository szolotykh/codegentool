# Code Generator Tool
## Requirements
Get OpenAI API Key from here: https://platform.openai.com/account/api-keys

Put the key in environment variable OPENAI_API_KEY

Install OpenAI python library: pip install openai

## Run tool
Run: python codegen.py

While you are running tool you can execute in tool commands:
- exit
- clean

First question should have file name in it.

### Example:

Can you generate C# hello word program. Main file name is Program.cs \
Can you add class Client with method Connect? \
Can you add new class Database with method Connect in new file?

Can you genetate base C# code for azure function with eventhub trigger?
Azure function should forward message received from event hub to http server in json format.
Can you add startup file with dependency injection for this project
Can you add polly to retry http request up to 3 times?