import os
import openai
import repository
from datetime import datetime

# Set up your API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Choose an API endpoint
model_engine = "text-davinci-003"

file_separation = "Inclose code with ``` and include file name after first ``` block on the same line as a block."
file_update = "if you doing update to file return whole updated file."
# file_delete = "If you move all code from the file or file no longer need say $$$$Action: Delete file 'file name' at the end."

cwd = os.getcwd()
repo = repository.Repository(cwd + "/src")

previousPrompt = ""

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    if user_input.lower() == "clear":
        repo.clear()
        repo.init_git_repo()
        continue

    project_files = repo.get_all_files()
    conversation = "\n\n".join([project_files, user_input, file_separation, file_update])

    print(conversation)

    response = openai.Completion.create(
        engine=model_engine,
        prompt=conversation,
        max_tokens=2000,
    )

    print(response.choices[0].text)
    if (repo.has_changes_to_commit()):
        repo.commit_all_files(datetime.now())

    repo.update(response.choices[0].text)

    previousPrompt = conversation