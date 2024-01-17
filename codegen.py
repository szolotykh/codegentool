import os
import argparse
import repository
import aiprompt
import aigenerator
import json
from datetime import datetime

def delete_file(file_name):
    print(f"DELETING_FILE ({file_name})")
    # os.remove(fileName)
    return "File deleted"

def read_static_template(file_name):
    with open("./templates/" + file_name, "r") as f:
        return f.read()
    

def firmulate_user_input(conversation, user_input):
    conversation.append({"role": "system", "content": read_static_template("main.txt")})
    conversation.append({"role": "user", "content": user_input})
    return conversation
    

def add_relative_information(conversation, repo):
    project_files = repo.get_all_files()
    conversation.append({"role": "system", "content": project_files})
    return conversation

def create_plan(conversation, generator: aigenerator.AIGenerator):
    conversation.append({"role": "system", "content": "Analizing provicded code created list of changes which need to be done"})
    message = generator.generate_analisys(conversation)
    conversation.append({"role": "assistant", "content": message.content})
    print("ANALISYS:")
    print (message.content)
    print("\n")
    return conversation

def update_repository(conversation, generator: aigenerator.AIGenerator, repo: repository.Repository):
    conversation.append({"role": "system", "content": "Updating repository. Use provided tools. Make sure you passing correctly formatted arguments."})
    conversation.append({"role": "system", "content": "Make sure that paremeters of functions are correctly formatted."})
    message = generator.generate_repository_update(conversation)

    max_iterations = 5
    iterations = 0
    while(message.tool_calls and iterations < max_iterations):
        iterations += 1
        print(f"ITERATION {iterations}:")

        tool_calls = message.tool_calls
        if tool_calls:
            available_functions = {
                "delete_file": delete_file,
                "create_or_update_file": repo.create_or_update_file,
            }
            for tool_call in tool_calls:
                print("TOOL CALLS:")
                print(tool_call)
                conversation.append({"role": "assistant", "content": str(tool_call)})
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                conversation.append({"role": "user", "content": function_response})
                print(f"FUNCTION RETURN: {function_response}")

            message = generator.generate_repository_update(conversation)
        else:
            print(f"ASSISTANT: {message.content}")
            conversation.append({"role": "assistant", "content": message.content})
            break
    return conversation

def main():
    # Create an argument parser to parse the command line arguments
    parser = argparse.ArgumentParser(description='Code generator')
    parser.add_argument('--path', help='Path to repository', required=True)
    args = parser.parse_args()

    cwd = args.path

    # Check if the folder path is an absolute path
    if not os.path.isabs(cwd):
        cwd = os.path.abspath(cwd)

    generator = aigenerator.AIGenerator("gpt-4")

    repo = repository.Repository(cwd)

    history = ""

    previousPrompt = ""

    conversation=[
        
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "#exit":
            break

        if user_input.lower() == "#clear":
            repo.clear()
            repo.init_git_repo()
            continue

        conversation = []
        conversation = firmulate_user_input(conversation, user_input)
        conversation = add_relative_information(conversation, repo)
        conversation = create_plan(conversation, generator)
        conversation = update_repository(conversation, generator, repo)

        # print(conversation)

        #repo.update(message.content)
        previousPrompt = user_input

if __name__ == '__main__':
    main()



        #if (repo.has_changes_to_commit()):
        #    print("Committing changes...")
        #    repo.commit_all_files(datetime.now())