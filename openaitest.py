import openai
import os
import re

def save_history(text):
    with open("history.txt", "w") as file:
        # Write the string to the file
        file.write(text)

def read_history():
    with open("history.txt", "r") as file:
        # Write the string to the file
        return file.read()
    


def extract_and_save(text):
    # Regex pattern to find the block with file name and content
    pattern = r'```(.*?)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        file_name, content = match
        file_name = file_name.strip()
        content = content.strip()

        # Save the content to a file with the provided file name
        with open("./src/" + file_name, 'w') as file:
            file.write(content)

def read_and_concatenate_files(directory):
    result = ""
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                result += f"```{file_name}\n{content}\n```\n\n"
                
    return result



# Set up your API key
#openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = ""

# Choose an API endpoint
model_engine = "text-davinci-003"

conversation = read_history()
print(conversation)

file_separation = "Inclose code with ``` and specify file name after first ``` block on the same line as a block."
file_update = "if you doing update to file return whole updated file."

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    conversation = "\n\n".join([conversation, user_input, file_separation, file_update])

    response = openai.Completion.create(
        engine=model_engine,
        prompt=conversation,
        max_tokens=2000,
    )

    conversation = conversation + response.choices[0].text
    
    extract_and_save(response.choices[0].text)

    # Send your API request and print the response
    print(response.choices[0].text)
    save_history(conversation)


quit()

# Build your API request
prompt = "Can you generate code for queue in c++?"
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=2000,
)

# Send your API request and print the response
print(response.choices[0].text)

with open("history.txt", "w") as file:
    # Write the string to the file
    file.write(response.choices[0].text)
